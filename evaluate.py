from hotpot_evaluate_v1 import  f1_score, normalize_answer
import csv
def get(filename):
    data = []
    with open(filename, newline='') as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            d = {}
            d['question'] = row[1]
            d['answer'] = row[2]
            d['bridge_answer'] = row[3]
            d['bridge_score'] = row[3]
            d['intersec_answer'] = row[4]
            d['intersec_score'] = row[5]
            d['ultimate_answer'] = row[6]
            data.append(d)
    return data
first = get("dev-answers-old.csv")
second = get("dev-answers.csv")
data = first + second

fscores = [0, 0, 0]
ems = [0, 0, 0]
precision = [0, 0, 0]
recall = [0, 0, 0]
for i, d in enumerate(data):
    a = d['answer']
    bridge_answer = d['bridge_answer']
    intersec_answer = d['intersec_answer']
    ultimate_answer = d['ultimate_answer']

    f1, prcsn, rcll = f1_score(bridge_answer, a)
    fscores[0]   += f1
    precision[0] += prcsn
    recall[0]    += rcll
    ems[0] += bridge_answer == a

    f1, prcsn, rcll = f1_score(intersec_answer, a)
    fscores[1]   += f1
    precision[1] += prcsn
    recall[1]    += rcll
    ems[1] += intersec_answer == a

    f1, prcsn, rcll = f1_score(ultimate_answer, a)
    fscores[2]   += f1
    precision[2] += prcsn
    recall[2]    += rcll
    ems[2] += ultimate_answer == a

    shit1 = bridge_answer == a
    shit2 = intersec_answer == a
    shit3 = ultimate_answer == a
    print("{:5d} : {:5s} : {:5s} : {:5s}".format(i, str(shit1), str(shit2), str(shit3)))

eval_file_name = "dev-eval.csv"
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
