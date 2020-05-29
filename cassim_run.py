"""File: cassim_run.py

Authors: Mattijs Blankesteijn & András Csirik
Computational Dialogue Modelling 2020

This file contains code to run CASSIM on Conversations.
"""

import pickle
from cassim import Cassim


def run(start, end, ignore_longer=1300):
    """Run and example."""
    cs = Cassim()

    with open('pickles_cassim.p', 'rb') as f:
        conversations = pickle.load(f)

    # Case study
    # ln = []
    # for c in conversations:
    #    ln.append(len(c.lines))
    # print(np.mean(ln), np.median(ln))
    # print(len([l for l in ln if l < 1500]))
    # print(max(ln))
    # plt.plot(sorted(ln), 'p')
    # plt.show(

    for i, case in enumerate(conversations[start:end]):
        if len(case.lines) > ignore_longer:
            continue
        # Get conversation text lose BNC2014 information (CASSIM CoreNLP).
        text = case.get_conversation()
        doc = [ut for (_, ut) in text]

        try:
            case.syntax_alignment = cs.syntax_similarity_conversation(doc)
        except Exception as e:
            print(i, e)

    with open('pickles_cassim.p', 'wb') as f:
        pickle.dump(conversations, f)


if __name__ == '__main__':
    # Run:
    # $ python3 conversations.py
    # Rename pickles.p to pickles_cassim.p
    # $ python3 nlp_server.py
    # Separate terminal:
    # $ time python3 run.py

    # run(0, 100)
    # run(100, 200)
    # run(200, 300)
    # run(300, 400)
    # run(400, 500)
    # run(500, 600)
    # run(600, 650)
    # run(650, 700)
    # run(700, 800)
    # run(800, 900)
    # run(900, 1000)
    # run(1000, 1100)
    # run(1100, 1200)
    # run(1200, 1300)
