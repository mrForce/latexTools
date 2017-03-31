import sys
from statistics import mean
import argparse
import re
parser = argparse.ArgumentParser(description="We are trying to find where the missing $ is. Notice an observation: after a missing $, the length of the inline math sections increases dramatically.")
parser.add_argument('latex_file', nargs=1)
newline_weight = 19
args = parser.parse_args()
#print(args.latex_file[0])
with open(args.latex_file[0], 'r') as f:
    text = f.read()
    m = re.compile('(\$[^\$]+\$)+', re.MULTILINE)
    matches = m.findall(text)
    num_matches = len(matches)
    differences = list()
    stop_index = num_matches + 1
    #There shouldn't be a newline between $ and $. If there is, then we know that the missing $ is before i. Don't score the matches with index >  i.
    for i in range(0, num_matches):
        if '\n' in matches[i]:
            stop_index = i + 1
    if i <= 5:
        print('Stopping, the missing $ is in the first five matches')
        sys.exit()
        
    for i in range(5, stop_index):
        mean_length_after = mean([1.0*len(matches[j]) + newline_weight*matches[j].count('\n') for j in range(i, num_matches)])
        mean_length_before = mean([1.0*len(matches[j]) for j in range(0, i)])
        difference = mean_length_after - mean_length_before

        differences.append((difference, matches[i]))

        

    for difference, string in sorted(differences, key=lambda x: x[0], reverse=True):
        print('Start of never-ending section: ')
        print(string)
        print('\n\n\n')
    
        
