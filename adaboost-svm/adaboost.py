import math
import csv
import random


def iterate(matches, sample_weight):
    error = 0
    if sample_weight is None:
        sample_weight = []
        for idx in range(len(matches)):
            sample_weight.append(float(1) / len(matches))
    for idx in range(len(matches)):
        if not matches[idx]:
            error += sample_weight[idx]
    print('error is ' + str(error))
    # if error > 0.5:
    #     return True, None, None
    beta = error / (1 - error)
    clf_weight = math.log(1 / beta)
    new_sample_weight = []
    print('updating sample weights...')
    sum = 0
    for idx in range(len(matches)):
        if matches[idx]:
            new_sample_weight.append(sample_weight[idx] * beta)
            sum += sample_weight[idx] * beta
        else:
            new_sample_weight.append(sample_weight[idx])
            sum += sample_weight[idx]
    for idx in range(len(matches)):
        new_sample_weight[idx] /= sum
    print('done')
    return False, clf_weight, new_sample_weight


def merge(id, candid, weight):
    result = []
    print('merging...')
    for i in range(len(candid[0])):
        result.append(0)
    for i in range(len(weight)):
        for j in range(len(result)):
            result[j] += weight[i] * candid[i][j]
    print('done')
    with open('result/' + str(id) + '-weak.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'label'])
        i = random.randint(0, len(weight) - 1)
        for idx, label in enumerate(candid[i]):
            writer.writerow([idx + 1, 1 if label > 0 else -1 if label < 0 else 0])
    with open('result/' + str(id) + '-standard.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'label'])
        for idx, label in enumerate(result):
            writer.writerow([idx + 1, 1 if label > 0 else -1 if label < 0 else 0])
    with open('result/' + str(id) + '-strict.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'label'])
        for idx, label in enumerate(result):
            writer.writerow([idx + 1, 1 if label > 0.05 else -1 if label < -0.05 else 0])
    with open('result/' + str(id) + '-loose.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'label'])
        for idx, label in enumerate(result):
            writer.writerow([idx + 1, 1 if label > 0.25 else -1 if label < -0.25 else 0])