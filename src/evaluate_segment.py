""" Official evaluation script for v1.1 of the SQuAD dataset. """
from collections import Counter
import string
import re
import argparse
import json
import sys
import statistics


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def f1_score(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def exact_match_score(prediction, ground_truth):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))


def metric_max_over_ground_truths(metric_fn, prediction, ground_truths):
    scores_for_ground_truths = []
    for ground_truth in ground_truths:
        score = metric_fn(prediction, ground_truth)
        scores_for_ground_truths.append(score)
    return max(scores_for_ground_truths)

def get_prediction(predictions, id):
    """Given original id, extract all predictions."""
    prediction = ""
    sent_id = 0
    pred_id = id + "=" + str(sent_id)
    while pred_id in predictions:
        if predictions[pred_id] != "":
            prediction = predictions[pred_id]
            break       #Get the first answer
        sent_id += 1
        pred_id = id + "=" + str(sent_id)
    return prediction
def evaluate(dataset, predictions, analysis):
    f1 = {}
    exact_match = {}
    total = {}
    for article in dataset:
        for paragraph in article['paragraphs']:
            for qa in paragraph['qas']:
                ans_position = 0 if analysis[qa['id']] == 0 else 1              #Bias or not
                total[ans_position] = 1 if ans_position not in total else total[ans_position] + 1
                # if qa['id'] not in predictions:
                #     message = 'Unanswered question ' + qa['id'] + \
                #               ' will receive score 0.'
                #     print(message, file=sys.stderr)
                #     continue
                ground_truths = list(map(lambda x: x['text'], qa['answers']))
                ##############
                prediction = get_prediction(predictions, qa['id'])
                #############
                new_exact_match = metric_max_over_ground_truths(
                    exact_match_score, prediction, ground_truths)
                if ans_position not in exact_match:
                    exact_match[ans_position] = [new_exact_match] 
                else:
                    exact_match[ans_position].append(new_exact_match)

                new_f1 = metric_max_over_ground_truths(
                    f1_score, prediction, ground_truths)
                if ans_position not in f1:
                    f1[ans_position] = [new_f1]
                else:
                    f1[ans_position].append(new_f1)
    for key in total:
        em_mean = statistics.mean(exact_match[key])
        exact_match[key] = em_mean
        f1_mean = statistics.mean(f1[key])
        f1[key] = f1_mean

    return {'exact_match': exact_match, 'f1': f1, 'total': total}


if __name__ == '__main__':
    expected_version = '1.1'
    parser = argparse.ArgumentParser(
        description='Evaluation for SQuAD ' + expected_version)
    parser.add_argument('dataset_file', help='Dataset file')
    parser.add_argument('prediction_file', help='Prediction File')
    parser.add_argument('analysis_file', help='Analysis file')

    args = parser.parse_args()
    with open(args.dataset_file) as dataset_file:
        dataset_json = json.load(dataset_file)
        dataset = dataset_json['data']

    with open(args.prediction_file) as prediction_file:
        predictions = json.load(prediction_file)

    with open(args.analysis_file) as analysis_file:
        analysis = json.load(analysis_file)

    print(json.dumps(evaluate(dataset, predictions, analysis)))

if __name__ == '__main__':
    expected_version = '1.1'
    parser = argparse.ArgumentParser(
        description='Evaluation for SQuAD ' + expected_version)
    parser.add_argument('dataset_file', help='Dataset file')
    parser.add_argument('prediction_file', help='Prediction File')
    parser.add_argument('analysis_file', help='Analysis file')

    args = parser.parse_args()
    with open(args.dataset_file) as dataset_file:
        dataset_json = json.load(dataset_file)
        dataset = dataset_json['data']

    with open(args.prediction_file) as prediction_file:
        predictions = json.load(prediction_file)

    with open(args.analysis_file) as analysis_file:
        analysis = json.load(analysis_file)

    print(json.dumps(evaluate(dataset, predictions, analysis)))