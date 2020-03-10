
from hotpot_evaluate_v1 import  f1_score, normalize_answer
import csv

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import drqa.reader
drqa.reader.set_default('model', './data/reader/single.mdl')
reader = drqa.reader.Predictor()  # Default model loaded for prediction


def one_hop_answers(documents, q, k):
    super_doc = " ".join([" ".join(d[1]) for d in documents])
    answers = reader.predict(super_doc, q, candidates=None, top_n=k)
    return answers

def run(json_file_name, answer_file_name, eval_file_name):
    import json
    with open(json_file_name) as f:
        data = json.load(f)

    from qa.my_main import DecompRC
    model = DecompRC(batch_size=50)
    for d in data:
        id = d['_id']
        a = normalize_answer(d['answer'])
        q = d['question']
        p = d['context']
        (q1_b, q2_b), (q1_i, q2_i) = model.get_output("span-predictor", q, p)
        print("Q  : {}".format(q))
        print("A  : {}".format(a))
        print("Q1: {}".format(q1_b))
        first_answers = one_hop_answers(p, q1_b, 5)
        print("A1: {}".format([shit[0] for shit in first_answers]))
        next_question =  q2_b.replace("[ANSWER]", first_answers[0][0])
        print("Q2: {}".format(next_question))
        second_answers = one_hop_answers(p, next_question, 5)
        print("A2: {}".format([shit[0] for shit in second_answers]))
        print("========================================")
        input()


run('dataset/new-hotpot-dev.json', "dev-answers.csv", "dev-eval.csv")
run('dataset/new-hotpot-train.json', "train-answers.csv", "train-eval.csv")
