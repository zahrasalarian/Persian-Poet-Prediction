import nltk
import sys,os,cv2,sys,string
from nltk.featstruct import unify
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

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    #print(files)
    #return 0
    file_words = {
        filename: tokenize(files[filename], filename)
        for filename in files
    }
    #print(file_words["ferdowsi_train.txt"][1])
    #file_counts = compute_counts(file_words)
    #print(file_counts)
    #print("enter")
    #s = input()
    landa_epsilon = [0.5, 0.1, 0.2, 0.7]
    print("whhhhhhaaaaaaaaa")
    print(landa_epsilon)
    #sentence = input()
    ans = probability("هر کسی از ظنّ خود ، شد یار من", file_words, landa_epsilon)

def load_files(directory):
    inf = {}
    os.chdir(r"{}".format(directory))
    files = os.listdir()
    for file in files:
        f = open(file, encoding="utf8")
        data = f.read()
        inf[file] = data
    return inf
    #print(len(inf["python.txt"][0]))


def tokenize(document, filename):
    #nltk.download()
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
    

    #tokens.sort()
    #print(tokens)
    return [tokens, bigram_tokens]



def probability(sentence, file_counts, landa_epsilon):
    tokens = regex.findall(r'\p{L}+', sentence.replace('\u200c', ''))
    tokens.reverse()
    #print("\n")
    print(tokens)

    # ferdowsi_train
    ferdowsi_prob = 1  
    for i in range(1, len(tokens)):
        uni = tokens[i]
        bi = tokens[i] + ' ' + tokens[i-1]
        if uni in file_counts["ferdowsi_train.txt"][0]:
            Pci = float(file_counts["ferdowsi_train.txt"][0][uni])/float(total_words_num_ferdowsi)
            print(float(file_counts["ferdowsi_train.txt"][0][uni]))
            print(float(total_words_num_ferdowsi))
            print(total_words_num_molavi)
            print(total_words_num_hafez)
            print(Pci)
            print("ok")
        else:
            Pci = 0
        if bi in file_counts["ferdowsi_train.txt"][1] and tokens[i-1] in file_counts["ferdowsi_train.txt"][0]:
            Pcici_1 = float(file_counts["ferdowsi_train.txt"][1][bi])/float(file_counts["ferdowsi_train.txt"][0][tokens[i-1]])
            print("ok")
        else:
            Pcici_1 = 0
        sum = landa_epsilon[3]*Pcici_1 + landa_epsilon[2]*Pci + landa_epsilon[1]*landa_epsilon[0]
        print("*************")
        print(sum)
        print(ferdowsi_prob)
        ferdowsi_prob *= sum
        print(ferdowsi_prob)
        print("*************")

    # hafez_train
    hafez_prob = 1  
    for i in range(1, len(tokens)):
        uni = tokens[i]
        bi = tokens[i] + ' ' + tokens[i-1]
        if uni in file_counts["hafez_train.txt"][0]:
            Pci = float(file_counts["hafez_train.txt"][0][uni])/float(total_words_num_hafez)
            print("ok")
        else:
            Pci = 0
        if bi in file_counts["hafez_train.txt"][1] and tokens[i-1] in file_counts["hafez_train.txt"][0]:    
            Pcici_1 = float(file_counts["hafez_train.txt"][1][bi])/float(file_counts["hafez_train.txt"][0][tokens[i-1]])
            print("ok")
        else:
            Pcici_1 = 0
        sum = landa_epsilon[3]*Pcici_1 + landa_epsilon[2]*Pci + landa_epsilon[1]*landa_epsilon[0]
        hafez_prob *= sum

    # molavi_train
    molavi_prob = 1  
    for i in range(1, len(tokens)):
        uni = tokens[i]
        bi = tokens[i] + ' ' + tokens[i-1]
        if uni in file_counts["molavi_train.txt"][0]:
            Pci = float(file_counts["molavi_train.txt"][0][uni])/float(total_words_num_molavi)
            print("ok")
        else:
            Pci = 0
        if bi in file_counts["molavi_train.txt"][1] and tokens[i-1] in file_counts["molavi_train.txt"][0]:    
            Pcici_1 = float(file_counts["molavi_train.txt"][1][bi])/float(file_counts["molavi_train.txt"][0][tokens[i-1]])
            print("ok")
        else:
            Pcici_1 = 0
        sum = landa_epsilon[3]*Pcici_1 + landa_epsilon[2]*Pci + landa_epsilon[1]*landa_epsilon[0]
        molavi_prob *= sum
    
    print(ferdowsi_prob)
    print(hafez_prob)
    print(molavi_prob)
    p_ans = max(ferdowsi_prob, hafez_prob, molavi_prob)
    print(p_ans)
    if p_ans == ferdowsi_prob:
        return 1
    elif p_ans == hafez_prob:
        return 2
    elif p_ans == molavi_prob:
        return 3

if __name__=="__main__":
    main()