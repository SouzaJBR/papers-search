import csv
import argparse
import ngram
import re

allPapers = []
foundPapers = []
notfoundPapers = []

def normalizeString(string):

    return re.sub('[\"\'.\-\:!?$%#]', '', string.strip().lower())

def loadPapers():
    with open('papers.csv') as papersfile:
        papers = csv.reader(papersfile)

        for paper in papers:
            if len(paper) >= 2:
                if paper[1].strip() == '1':
                    paperTitle = normalizeString(paper[0])

                    allPapers.append(paperTitle)


def loadScopus():
    with open(args.scopus) as csvfile:
        scopusFile = csv.reader(csvfile)
        for paper in scopusFile:
            G.add(normalizeString(paper[1]))


def loadScienceDirect():
    with open(args.sciencedirect) as txtfile:

        isEnded = False
        while not isEnded:
            author = txtfile.readline()
            title = txtfile.readline()
            G.add(normalizeString(title))
            line = txtfile.readline()
            while line != '\n':
                if line == '':
                    isEnded = True
                    break;

                line = txtfile.readline()


def main():


    loadPapers()

    if len(allPapers) == 0:
        print("None to load. Exiting.")
        return

    if args.scopus:
        loadScopus()

    if args.sciencedirect:
        loadScienceDirect()

    for paper in allPapers:
        sim = G.find(paper)
        if sim:
            foundPapers.append([paper, sim])
        else:
            notfoundPapers.append(paper)

    print "\n\nPAPERS FOUND:"
    for paper in foundPapers:
        print paper[0] + ' => ' + paper[1]

    print "\n\nPAPERS NOT FOUND:"
    for paper in notfoundPapers:
        print paper

    ratio = len(foundPapers) / float(len(allPapers))
    print("\n\n%.1f%% papers found" % (ratio * 100))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('papersFile', metavar='file', type=str, help='CSV file with papers to search')
    parser.add_argument('--scopus', help='CSV file with Scorpus exported search results')
    parser.add_argument('--sciencedirect', help='Text file with ScienceDirect exported results')
    parser.add_argument('--ngrams', dest='ngrams', default=5, help="N-grams to split text to search")
    parser.add_argument('--similatiry', dest='similarity', default=0.85, help="Minimun similarity to compare papers")

    args = parser.parse_args()
    G = ngram.NGram(N=args.ngrams, threshold=args.similarity)

    main()
