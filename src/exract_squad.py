import codecs
import json
import argparse

def main(path_to_squad, analysis_path, question_type, save_path):
    print("Begin")
    extracted_ids = []
    with open(analysis_path) as json_file:
        analysis = json.load(json_file)
    for id in analysis:
        if question_type == "biased":
            if analysis[id] == 0:       # answer in the first sentence
                extracted_ids.append(id)
        else:
            if analysis[id] != 0:
                extracted_ids.append(id)
    print("Analysis Loaded")

    with open(path_to_squad) as json_file:
        squad = json.load(json_file)['data']
    new_dataset = {}
    passage_list = []
    count_sample = 0
    for passage in squad:
        # print(passage['title'])
        new_passage = {}
        new_passage['title'] = passage['title']

        para_list = []
        for para in passage['paragraphs']:
            ques_list = []
            for qas in para['qas']:
                if qas['id'] in extracted_ids:
                    new_question = {}
                    new_question['question'] = qas['question']
                    new_question['id'] = qas['id']
                    new_question['answers'] = qas['answers']
                    ques_list.append(new_question)
                    count_sample += 1

            # if len(ques_list) > 0:
            new_para = {}
            new_para['qas'] = ques_list
            new_para['context'] = para['context']
            para_list.append(new_para)
        # if len(para_list) > 0:
        new_passage['paragraphs'] = para_list
        passage_list.append(new_passage)
    new_dataset['version'] = "SQuAD " + question_type 
    new_dataset['data'] = passage_list
    print(count_sample)

    with codecs.open(save_path, "w", encoding='utf8') as outfile:
        json.dump(new_dataset, outfile, ensure_ascii=False)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--path_to_squad', type=str, default=None, help='path_to_squad')
    parser.add_argument('--analysis_path', type=str, default=None, help='analysis_path')
    parser.add_argument('--question_type', type=str, default="biased", help='question_type')
    parser.add_argument('--save_path', type=str, help='save_path')
    args = parser.parse_args()
    main(args.path_to_squad, args.analysis_path, args.question_type, args.save_path)
    print("Finish!!")