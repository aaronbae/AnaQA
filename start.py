
from hotpot_evaluate_v1 import  f1_score, normalize_answer
import csv

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import drqa.reader
drqa.reader.set_default('model', './data/reader/single.mdl')
reader = drqa.reader.Predictor()  # Default model loaded for prediction
'''
d = "The Super Bowl is the annual championship game of the National Football League (NFL) played between mid-January and early February. It is the culmination of a regular season that begins in the late summer of the previous year."
q = "What is the name of the championship game of the National Football League?"

answer = reader.predict(d, q, candidates=None, top_n=10)
print(answer)


'''

def best_k_answers(documents, quesetion, k):
    from Queue import Queue as qe
    answers = []
    lowest_score = 1.0
    lowest_score_index = 0
    queue = qe()
    for count, supporting_paragraphs in enumerate(documents):
        a = reader.predict(" ".join(supporting_paragraphs[1]), quesetion, candidates=None, top_n=k)
        for tup in a:
            queue.insert(tup)
    while queue.length() > k:
        queue.delete()
    return queue.toList()


def best_one_hop_answer(documents, q):
    final_answer = ""
    final_score = 0.0
    for count, supporting_paragraphs in enumerate(documents):
        answer = reader.predict(" ".join(supporting_paragraphs[1]), q, candidates=None, top_n=1)
        if answer[0][1] > final_score:
            final_answer = answer[0][0]
            final_score = answer[0][1]
    return final_answer, final_score

def run(json_file_name, answer_file_name, eval_file_name):
    import json
    with open(json_file_name) as f:
        data = json.load(f)

    from qa.my_main import DecompRC
    model = DecompRC(batch_size=50)
    fscores = [0, 0, 0]
    ems = [0, 0, 0]
    precision = [0, 0, 0]
    recall = [0, 0, 0]
    SEETHISID = "5a81b2505542995ce29dcc32"
    FLAG = False
    for d in data:
        id = d['_id']
        if not FLAG:
          if SEETHISID == id:
            FLAG = True
          continue
        a = normalize_answer(d['answer'])
        q = d['question']
        p = d['context']
        if len(p) == 0:
          continue
        (q1_b, q2_b), (q1_i, q2_i) = model.get_output("span-predictor", q, p)
        print("Q  : {}".format(q))
        print("A  : {}".format(a))
        first_answer, _ = best_one_hop_answer(p, q)
        next_question =  q2_b.replace("[ANSWER]", first_answer)
        bridge_answer, bridge_score = best_one_hop_answer(p, next_question)
        bridge_answer = normalize_answer(bridge_answer)
        print("A-B: {}".format(bridge_answer))

        common_answers = []
        k = 10
        while len(common_answers) == 0:
            first_answers = best_k_answers(p, q1_i, k)
            second_answers = best_k_answers(p, q2_i, k)
            second_answers_set = set([tup[0] for tup in second_answers])
            common_answers = [tup for tup in first_answers if tup[0] in second_answers_set]
            k += 10
        intersec_answer = common_answers[0][0]
        intersec_score = common_answers[0][1]
        for ca in common_answers:
            if ca[1] > intersec_score:
                intersec_score = ca[1]
                intersec_answer = ca[0]
        intersec_answer = normalize_answer(intersec_answer)
        print("A-I: {}".format(intersec_answer))
        ultimate_answer = bridge_answer
        if intersec_score > bridge_score:
            ultimate_answer = intersec_answer
        print("A-C: {}".format(ultimate_answer))
        print("========================================")

        f1, prcsn, rcll = f1_score(bridge_answer, a)
        fscores[0]   += f1
        precision[0] += prcsn
        recall[0]    += rcll
        ems[0] += bridge_answer == a

        f1, prcsn, rcll = f1_score(intersec_answer, a)
        fscores[1]   += f1
        precision[1] += prcsn
        recall[1]    += rcll
        ems[1] += bridge_answer == a

        f1, prcsn, rcll = f1_score(ultimate_answer, a)
        fscores[2]   += f1
        precision[2] += prcsn
        recall[2]    += rcll
        ems[2] += bridge_answer == a

        with open(answer_file_name, mode='a') as file:
            row = [id, q, a, bridge_answer, bridge_score, intersec_answer, intersec_score, ultimate_answer]
            writer = csv.writer(file)
            writer.writerow(row)

    N = len(data)
    fscores = [i/N for i in fscores]
    ems = [i/N for i in ems]
    precision = [i/N for i in fscores]
    recall = [i/N for i in ems]
    with open(eval_file_name, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow(fscores)
        writer.writerow(precision)
        writer.writerow(recall)
        writer.writerow(ems)

run('dataset/new-hotpot-dev.json', "dev-answers.csv", "dev-eval.csv")
run('dataset/new-hotpot-train.json', "train-answers.csv", "train-eval.csv")
