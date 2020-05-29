"""File: LIWC.py

Authors: András Csirik & Mattijs Blankesteijn

Computational Dialogue Modelling 2020 (UvA)
April 2020
"""

import pickle
from conversations import *
from tqdm import tqdm
import convokit
from convokit import Corpus, Speaker, Utterance
from collections import defaultdict


def create_speakers(conversations):
    """Creates a convokit speakers class."""
    speaker_meta = {}

    for conv in conversations:
        for speaker in conv.speakers:
            speaker_meta[speaker.id] = {"age": speaker.age,
                                        "gender": speaker.gender}

    corpus_speakers = {k: Speaker(id=k, meta=v) for k, v in
                       speaker_meta.items()}
    return corpus_speakers


def create_utterances(conversations):
    """Creates a convokit utterances class."""
    utterance_corpus = {}
    ut_id = 1
    for conv in tqdm(conversations):
        root = ut_id
        for ut in conv.get_conversation():
            sp = ut[0]
            if sp != 'UNKFEMALE' and sp != 'UNKMALE' and sp != 'UNKMULTI':
                text = ut[1]
                if root == ut_id:
                    u = Utterance(id='u' + str(ut_id),
                                  speaker=corpus_speakers[sp],
                                  text=text, root='u' + str(root),
                                  reply_to=None)
                    utterance_corpus['u' + str(ut_id)] = u
                else:
                    u = Utterance(id='u' + str(ut_id),
                                  speaker=corpus_speakers[sp],
                                  text=text, root='u' + str(root),
                                  reply_to='u' + str(ut_id - 1))
                    utterance_corpus['u' + str(ut_id)] = u

                ut_id += 1

    utterance_list = utterance_corpus.values()
    return utterance_list


def create_2pers_convs(conversations):
    conv_2pers = []
    for conv in conversations:
        if conv.n_speakers() == 2:
            conv_2pers.append(conv)
    return conv_2pers


if __name__ == "__main__":
    with open('pickles.p', 'rb') as f:
        conversations = pickle.load(f)

    corpus_speakers = create_speakers(conversations)
    utterance_list = create_utterances(conversations)

    # Creating a convokit corpus class
    BCN_corpus = Corpus(utterances=utterance_list)
    # Create a convokit coordination class.
    coord = convokit.Coordination()
    # Fit the underlying model (calculate LIWC scores)
    coord.fit(BCN_corpus)
    # Transform the BCN corpus into a coordination class
    # (this can deal with the LIWC scores)
    coord.transform(BCN_corpus)

    # Example code to create alignment scores from the 40-49 age group to all others
    # Creating the speaker sets based on age groups
    _10_19 = list(BCN_corpus.iter_speakers(lambda speaker: speaker.meta['age'] > 9 and speaker.meta['age'] < 20))
    _20_29 = list(BCN_corpus.iter_speakers(lambda speaker: speaker.meta['age'] > 19 and speaker.meta['age'] < 30))
    _30_39 = list(BCN_corpus.iter_speakers(lambda speaker: speaker.meta['age'] > 29 and speaker.meta['age'] < 40))
    _40_49 = list(BCN_corpus.iter_speakers(lambda speaker: speaker.meta['age'] > 39 and speaker.meta['age'] < 50))
    _50_59 = list(BCN_corpus.iter_speakers(lambda speaker: speaker.meta['age'] > 49 and speaker.meta['age'] < 60))
    _60_69 = list(BCN_corpus.iter_speakers(lambda speaker: speaker.meta['age'] > 59 and speaker.meta['age'] < 70))
    _70_79 = list(BCN_corpus.iter_speakers(lambda speaker: speaker.meta['age'] > 69 and speaker.meta['age'] < 80))
    _80_89 = list(BCN_corpus.iter_speakers(lambda speaker: speaker.meta['age'] > 79 and speaker.meta['age'] < 90))

    # Creating coord.score objects for the 80-89 age group against all other age groups
    _80to10 = coord.score(BCN_corpus, _80_89, _10_19)
    _80to20 = coord.score(BCN_corpus, _80_89, _20_29)
    _80to30 = coord.score(BCN_corpus, _80_89, _30_39)
    _80to40 = coord.score(BCN_corpus, _80_89, _40_49)
    _80to50 = coord.score(BCN_corpus, _80_89, _50_59)
    _80to60 = coord.score(BCN_corpus, _80_89, _60_69)
    _80to70 = coord.score(BCN_corpus, _80_89, _70_79)
    _80to80 = coord.score(BCN_corpus, _80_89, _80_89)

    f = open("80to.txt", 'a')

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, _80to10)
    f.write("80 to 10\n")
    f.write(str(score_by_marker) + '\n')
    f.write(str(agg1) + '\n')
    f.write(str(agg2) + '\n')
    f.write(str(agg3) + '\n')
    f.write("\n")

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, _80to20)
    f.write("80 to 20\n")
    f.write(str(score_by_marker) + '\n')
    f.write(str(agg1) + '\n')
    f.write(str(agg2) + '\n')
    f.write(str(agg3) + '\n')
    f.write("\n")

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, _80to30)
    f.write("80 to 30\n")
    f.write(str(score_by_marker) + '\n')
    f.write(str(agg1) + '\n')
    f.write(str(agg2) + '\n')
    f.write(str(agg3) + '\n')
    f.write("\n")

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, _80to40)
    f.write("80 to 40\n")
    f.write(str(score_by_marker) + '\n')
    f.write(str(agg1) + '\n')
    f.write(str(agg2) + '\n')
    f.write(str(agg3) + '\n')
    f.write("\n")

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, _80to50)
    f.write("80 to 50\n")
    f.write(str(score_by_marker) + '\n')
    f.write(str(agg1) + '\n')
    f.write(str(agg2) + '\n')
    f.write(str(agg3) + '\n')
    f.write("\n")

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, _80to60)
    f.write("80 to 60\n")
    f.write(str(score_by_marker) + '\n')
    f.write(str(agg1) + '\n')
    f.write(str(agg2) + '\n')
    f.write(str(agg3) + '\n')
    f.write("\n")

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, _80to70)
    f.write("80 to 70\n")
    f.write(str(score_by_marker) + '\n')
    f.write(str(agg1) + '\n')
    f.write(str(agg2) + '\n')
    f.write(str(agg3) + '\n')
    f.write("\n")

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, _80to80)
    f.write("80 to 80\n")
    f.write(str(score_by_marker) + '\n')
    f.write(str(agg1) + '\n')
    f.write(str(agg2) + '\n')
    f.write(str(agg3) + '\n')
    f.write("\n")

    f.close()


    # Generating an analogue result to
    # https://github.com/CornellNLP/Cornell-Conversational-Analysis-Toolkit/blob/master/examples/coordination/examples.ipynb
    # Example 1

    """males = list(BCN_corpus.iter_speakers(lambda speaker: speaker.meta['gender'] == 'M'))
    females = list(BCN_corpus.iter_speakers(lambda speaker: speaker.meta['gender'] == 'F'))
    everyone = list(BCN_corpus.iter_speakers())

    everyone_to_everyone = coord.score(BCN_corpus, everyone, everyone)
    for sp, score in sorted(everyone_to_everyone.averages_by_speaker().items(), key=lambda x: x[1], reverse=True):
        print(sp.id, (sp.meta["age"], sp.meta["gender"], round(score,  5))"""
    """males_to_females = coord.score(BCN_corpus, males, females)
    for male, score in sorted(males_to_females.averages_by_speaker().items(), key=lambda x: x[1], reverse=True):
        print(male.id, round(score, 5))"""

    """males_to_females = coord.score(BCN_corpus, males, females, focus="targets")
    females_to_males = coord.score(BCN_corpus, females, males, focus="targets")
    males_to_males = coord.score(BCN_corpus, males, males, focus="targets")
    females_to_females = coord.score(BCN_corpus, females, females, focus="targets")

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, males_to_males)
    print("Males to males\n")
    print(score_by_marker)
    print(agg1, agg2, agg3)

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, males_to_females)
    print("Males to females\n")
    print(score_by_marker)
    print(agg1, agg2, agg3)

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, females_to_females)
    print("Females to females\n")
    print(score_by_marker)
    print(agg1, agg2, agg3)

    _, score_by_marker, agg1, agg2, agg3 = coord.score_report(BCN_corpus, females_to_males)
    print("Females to males\n")
    print(score_by_marker)
    print(agg1, agg2, agg3)"""
