import nltk
import sys,os,cv2,sys,string
import regex

FILE_MATCHES = 1
SENTENCE_MATCHES = 1

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
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)
    print(file_words)
    
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


def tokenize(document):
    #nltk.download()
    document = document.lower()
    tokens = regex.findall(r'\p{L}+', document.replace('\u200c', ''))
    #delete stopwords
    stopwords = nltk.corpus.stopwords.words("english")
    #delete string punctuation
    punctuation = string.punctuation
    to_delete = []
    for t in tokens:
        if t in stopwords:
            to_delete.append(t)
        elif t in punctuation:
            to_delete.append(t)
        #t = t.encode('ascii', 'ignore')
    for td in to_delete:
        tokens.remove(td)
    tokens.sort()
    #print(tokens)
    return tokens

def compute_idfs(documents):
    inverse_doc = {}
    unique_doc =[]
    num_dic = len(documents)
    for k,v in documents.items():
        documents[k] = set(v)
        unique_doc.append(documents[k])
    for k,v in documents.items():
        for word in v:
            count = 0
            for ud in unique_doc:
                if word in ud:
                    count += 1
            if word not in inverse_doc.keys():
                inverse_doc[word] = count
    return inverse_doc
    #print(len(inverse_doc))

if __name__=="__main__":
    main()