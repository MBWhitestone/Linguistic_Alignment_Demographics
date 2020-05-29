"""File: cassim.py

Authors: Mattijs Blankesteijn & András Csirik
Computational Dialogue Modelling 2020

This file contains the Conversation Level Syntax Similarity Metric (CASSIM)
described by Boghrati et al. (2018).

The original software by 'reihane' is released under GPLv2.
See also: https://github.com/USC-CSSL/CASSIM/

Changes made to the original software:
- Use NLTK CoreNLP parser instead of Standford parser
- Use scipy.optimize.linear_sum_assignment as optimizer [deprecated]
- Make average default behaviour for BNC2014
- Removed unnecessary functions
- Convert Python2 to Python3
- Add tqdm and other code optimizations
- Make code more likely to conform to PEP8
"""

from tqdm import tqdm
import numpy as np
import nltk
from nltk.parse.corenlp import CoreNLPParser
from nltk.tree import ParentedTree
from zss import simple_distance, Node

numnodes = 0


class Cassim():
    """Cassim main class."""

    def __init__(self):
        """ """
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        self.parser = CoreNLPParser(url='http://localhost:9000')

    def convert_mytree(self, nltktree, pnode):
        """ """
        global numnodes
        for node in nltktree:
            numnodes += 1
            if type(node) is nltk.ParentedTree:
                tempnode = Node(node.label())
                pnode.addkid(tempnode)
                self.convert_mytree(node, tempnode)
        return pnode

    def syntax_similarity_conversation(self, documents1):
        """Syntax similarity of each document with its before and after."""
        global numnodes
        documents1parsed = []

        # Detect sentences and parse them
        for d1 in tqdm(range(len(documents1))):
            tempsents = (self.sent_detector.tokenize(documents1[d1].strip()))
            for s in tempsents:
                if len(s.split()) > 70:
                    documents1parsed.append("NA")
                    break
            else:
                temp = list(self.parser.raw_parse_sents((tempsents)))
                for i in range(len(temp)):
                    temp[i] = list(temp[i])[0]
                    temp[i] = ParentedTree.convert(temp[i])
                documents1parsed.append(list(temp))

        results = []
        for d1 in range(len(documents1parsed) - 1):
            d2 = d1 + 1
            if documents1parsed[d1] == "NA" or documents1parsed[d2] == "NA":
                results.append(float('NaN'))
                continue

            costMatrix = []
            for i in range(len(documents1parsed[d1])):
                numnodes = 0
                tempnode = Node(documents1parsed[d1][i].root().label())
                sentencedoc1 = self.convert_mytree(documents1parsed[d1][i],
                                                   tempnode)
                temp_costMatrix = []
                sen1nodes = numnodes
                for j in range(len(documents1parsed[d2])):
                    numnodes = .0
                    tempnode = Node(documents1parsed[d2][j].root().label())
                    sentencedoc2 = self.convert_mytree(documents1parsed[d2][j],
                                                       tempnode)
                    ED = simple_distance(sentencedoc1, sentencedoc2)
                    ED /= (numnodes + sen1nodes)
                    temp_costMatrix.append(ED)
                costMatrix.append(temp_costMatrix)
            costMatrix = np.array(costMatrix)

            results.append(1 - np.mean(costMatrix))

        return np.array(results)


if __name__ == '__main__':
    cs = Cassim()

    d1 = "Colorless green ideas sleep furiously"
    d2 = "Whereof one cannot speak, thereof one must be silent"
    d3 = "Those who cannot remember the past are condemned to compute it. Language disguises thought."
    # sim = cs.syntax_similarity_t/wo_documents(d1, d2, True)
    # print(sim)

    sim1 = cs.syntax_similarity_conversation([d1, d2, d3])
    print(sim1)
