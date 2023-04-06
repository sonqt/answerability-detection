import json
import sys

def main(path_to_data):
    analysis = json.load(open(path_to_analysis))
    bias, anti_bias = 0, 0
    for id in analysis:
        if analysis[id] == 0:
            bias += 1
        else:
            anti_bias += 1
    print(bias, anti_bias)
    
if __name__ == '__main__':
    path_to_analysis = sys.argv[1]
    main(path_to_analysis)
