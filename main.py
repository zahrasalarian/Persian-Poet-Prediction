import sys,os,sys
import regex
from regex.regex import escape

FILE_MATCHES = 1
SENTENCE_MATCHES = 1
total_words_num_ferdowsi = 0
total_words_num_hafez = 0
total_words_num_molavi = 0

try:
    # Fix UTF8 output issues on Windows console.
    # Does nothing if package is not installed
    from win_unicode_console import enable
    enable()
except ImportError:
    pass

train_files = []

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename], filename)
        for filename in files
    }
    lambda_epsilon = [0.001, 0.05, 0.475, 0.475]

    # test
    accuracy = evaluate_accuracy(file_words, lambda_epsilon)
    print("Accuracy: ")
    print(accuracy)

def load_files(directory):
    global train_files
    inf = {}
    os.chdir(r"{}".format(directory))
    files = os.listdir()
    train_files = files
    for file in files:
        f = open(file, encoding="utf8")
        data = f.read()
        inf[file] = data
    os.chdir(r"..")
    return inf

def tokenize(document, filename):
    global total_words_num_molavi
    global total_words_num_ferdowsi
    global total_words_num_hafez

    uni_count_doc_temp = {}
    bi_count_doc_temp = {}

    document = document.lower()
    tokens = regex.findall(r'\p{L}+', document.replace('\u200c', ''))
    for word in tokens:
        if word not in uni_count_doc_temp:
            count = tokens.count(word)
            uni_count_doc_temp[word] = count

            if filename == "ferdowsi_train.txt":
                total_words_num_ferdowsi += count
            elif filename == "hafez_train.txt":
                total_words_num_hafez += count
            else:
                total_words_num_molavi += count
        
    for i in range(len(tokens) - 1):
        bi = tokens[i] + ' ' + tokens[i+1]
        if bi not in bi_count_doc_temp:
            bi_count_doc_temp[bi] = 1
        else:
            bi_count_doc_temp[bi] += 1

    return [uni_count_doc_temp, bi_count_doc_temp]

def probability(sentence, file_counts, lambda_epsilon):
    tokens = regex.findall(r'\p{L}+', sentence.replace('\u200c', ''))
    tokens.reverse()

    probs = {}

    for filename in train_files:
        if filename == "ferdowsi_train.txt":
            M = total_words_num_ferdowsi
        elif filename == "hafez_train.txt":
            M = total_words_num_hafez
        else:
            M = total_words_num_molavi

        prob = 1  
        for i in range(1, len(tokens)):
            uni = tokens[i]
            bi = tokens[i] + ' ' + tokens[i-1]
            if uni in file_counts[filename][0]:
                Pci = float(file_counts[filename][0][uni])/float(M)
            else:
                Pci = 0
            if bi in file_counts[filename][1] and tokens[i-1] in file_counts[filename][0]:
                Pcici_1 = float(file_counts[filename][1][bi])/float(file_counts[filename][0][tokens[i-1]])
            else:
                Pcici_1 = 0
            sum = lambda_epsilon[3]*Pcici_1 + lambda_epsilon[2]*Pci + lambda_epsilon[1]*lambda_epsilon[0]
            prob *= sum
        probs[filename] = prob
    
    key_max = max(probs.keys(), key=(lambda k: probs[k]))
    if key_max == "ferdowsi_train.txt":
        return 1
    elif key_max == "hafez_train.txt":
        return 2
    else:
        return 3

def evaluate_accuracy(file_words, lambda_epsilon):
    file = 'test_file.txt'
    true = 0
    total = 0
    f = open(file, encoding="utf8")
    lines = f.readlines()
    for line in lines:
        l = line.split('\t')
        l[1] = l[1].replace('\u200c', '').replace('\n', '')
        ans = probability(l[1], file_words, lambda_epsilon)
        if ans == int(l[0]):
            true += 1
        total += 1
    accuracy = true/total
    return accuracy

if __name__=="__main__":
    main()