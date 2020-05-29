"""File: conversations.py

Authors: Mattijs Blankesteijn & András Csirik

Computational Dialogue Modelling 2020 (UvA)
April 2020
"""

import os
import pickle
from collections import Counter

from bs4 import BeautifulSoup
import tqdm
import regex as re


class EmptyAge():
    """Class as placeholder for unknown age."""

    def __init__(self, age):
        """Just store the input."""
        self.age = age

    def __hash__(self):
        """Needed for Counter. Actually don't understand this in depth."""
        return hash(self.age)

    def __repr__(self):
        """Representation equals string representation."""
        return str(self)

    def __str__(self):
        """An EmptyAge object with its original input."""
        return f'EmptyAge(age={self.age})'

    def __add__(self, other):
        """Undefined so return inf to calculate things."""
        return float('inf')

    def __sub__(self, other):
        """Undefined so return inf to calculate things."""
        return self + other

    def __mul__(self, other):
        """Undefined so return inf to calculate things."""
        return self + other

    def __eq__(self, other):
        """Empty ages satisfies no equalities."""
        return False

    def __ne__(self, other):
        """Empty ages satisfies no inequalities."""
        return self.__eq__(other)

    def __lt__(self, other):
        """Empty ages satisfies no equalities."""
        return self.__eq__(other)

    def __gt__(self, other):
        """Empty ages satisfies no equalities."""
        return self.__eq__(other)

    def __le__(self, other):
        """Empty ages satisfies no equalities."""
        return self.__eq__(other)

    def __ge__(self, other):
        """Empty ages satisfies no equalities."""
        return self.__eq__(other)


class Person():
    """Person class with properties."""

    def __init__(self, xml):
        """Initialize a Person based on information from xml."""
        self.id = xml.get('id')
        self.xml = xml
        self.age = Person.str_to_age(self._get_demographic('exactage'))
        self.gender = self._get_demographic('gender')
        self.first_language = self._get_demographic('l1')
        self.nationality = self._get_demographic('nat')

        self.xml = str(self.xml)
        # ...

    @staticmethod
    def str_to_age(age):
        """Try converting string with int() else return None."""
        try:
            age = int(age)
        except:
            age = EmptyAge(age)
        return age

    def _get_demographic(self, demographic):
        """Shortcut for bs4 syntax."""
        if isinstance(self.xml, str):
            self.xml = BeautifulSoup(self.xml, "html5lib")
        return self.xml.find(demographic).get_text()

    def __repr__(self):
        """Representation is string Person."""
        return str(self)

    def __str__(self):
        """Returns representation of Person and important features as str."""
        return f'Person(id={self.id}, age={self.age}, gender={self.gender})'

class Conversation():
    """Conversation in BNC2014."""

    def __init__(self, id, speakers, loc='data/spoken/'):
        """ """
        self.id = id.strip()
        self.path = loc + 'tagged/' + self.id
        self.path_untagged = loc + 'untagged/' + self.id[:-8] + '.xml'
        self.speakers = speakers
        self.conversation = []

        self.n_male = None
        self.n_female = None
        self.ages = None
        self.age_lower_bound = None
        self.age_upper_bound = None
        self.age_range = None

        self.lines = None
        self.soup = None

        self.syntax_alignment = None
        self.lexical_alignment = None

        self.calculate_statistics()

    def _read_file(self, quick=True, soup=False):
        """Internal to read in file. Not called in init to prevent overload."""
        if not self.lines:
            path = self.path_untagged if quick else self.path
            with open(path, 'r') as f:
                if soup:
                    self.soup = BeautifulSoup(f, "html5lib")
                self.lines = f.readlines()

    def get_raw(self):
        """Get text of the file."""
        self._read_file()
        return self.lines

    def get_soup(self):
        """ """
        self._read_file()
        return self.soup

    def _parse_line(self, line):
        """Returns tuple (who, text)."""
        parts = line.split('>', 1)
        speaker = parts[0].split('who')[1].split('"')[1]
        # Remove all xml tags from text
        text = re.sub("<.*/> ?|<.*>.*</.*> ?", "", parts[1][:-5])
        return speaker, text

    def get_conversation(self, soup=False):
        """ """
        if self.conversation:
            return self.conversation

        self._read_file(soup=soup)
        conversation = []

        # Parse as xml or as raw line.
        if self.soup is not None:
            utters = self.soup.find_all('u')
            for utterance in utters:
                conversation.append((utterance.get('who'),
                                     utterance.text.split('\n')[1:-1]))

        else:
            # ignore empty lines afters _parse_line, check if it needs to be
            # appended to last speaker
            nextcheck = False
            for utter in self.lines:
                if '<u ' in utter:
                    speaker, text = self._parse_line(utter)
                    if text:
                        if nextcheck and conversation and \
                           speaker == conversation[-1][0]:
                            conversation[-1] = (speaker, conversation[-1][1] \
                                                      + ' ' + text)
                        else:
                            conversation.append((speaker, text))
                        nextcheck = False
                    else:
                        nextcheck = True

        self.conversation = conversation
        return conversation

    def n_speakers(self):
        """Returns number of speakers."""
        return len(self.speakers)

    def get_speakers(self):
        """Returns list of speaker metadata."""
        return self.speakers

    def calculate_statistics(self):
        """Calculate speaker statistics in this Converstation."""
        gender, age = [], []
        for speaker in self.speakers:
            gender.append(speaker.gender)
            age.append(speaker.age)

        # Gender, positive: more female, negative: more male.
        genders = Counter(gender)
        assert len(genders) < 3
        self.n_female = genders['F']
        self.n_male = genders['M']
        self.gender = self.n_female - self.n_male

        self.ages = Counter(age)
        self.age_lower_bound = min(self.ages)
        self.age_upper_bound = max(self.ages)
        self.age_range = self.age_upper_bound - self.age_lower_bound

    def __repr__(self):
        """Representation is string Conversation."""
        return str(self)

    def __str__(self):
        """Returns representation of Conversation as str."""
        return f'ConversationClass(id={self.id}, ' \
                          + f'n_male={self.n_male}, ' \
                          + f'n_female={self.n_female}, ' \
                          + f'min_age={self.age_lower_bound}, ' \
                          + f'max_age={self.age_upper_bound}, ' \
                          + f'age_range={self.age_range})'
        # return 'hi'


def create_persons(store='persons.txt', dt="data/spoken/tagged"):
    """Investigate tagged dataset on persons."""
    multi, total = 0, 0
    print(f'Reading from {dt}, writing to {store}...')

    with open(store, 'w') as f:
        for file in os.listdir(dt):
            print(f'-- {file}')
            soup = BeautifulSoup(open(dt + "/" + file), "html5lib")
            utters = soup.find_all('u')

            # Discard unknown persons.
            people = set([w.get('who') for w in utters if 'UNK' not in
                          w.get('who')])

            f.write(f'{file}, {people}\n')
            if len(people) > 2:
                multi += 1
            total += 1

        f.write('\n')
        f.write(f'{multi}, {total}\n')
        print(f'Done {multi}/{total}\n')

def investigate(file, dt="data/spoken/metadata"):
    """Investigate actual demographics."""
    with open(file, 'r') as f:
        lines = f.readlines()

    soup = BeautifulSoup(open(dt + "/speakerInfo.xml"), "html5lib")
    speakers = {s.get('id'): s for s in soup.find_all('speaker')}

    conversations = []
    for line in lines[:-2]:
        file, persons = line.split('{')
        people = persons.split('}')[0].replace("'", "").split(', ')
        props = [Person(speakers[person]) for person in people]
        conversations.append(Conversation(file, props))

    return conversations

if __name__ == '__main__':
    store = 'persons.txt'

    if not os.path.exists(store):
        create_persons(store)
    conversations = investigate(store)
    print(len(conversations))
    print(len(set([s.id for c in conversations for s in c.speakers])))

    for conversation in tqdm.tqdm(conversations):
        conversation.get_conversation()
    with open('pickles.p', 'wb') as f:
        pickle.dump(conversations, f)

    with open('pickles.p', 'rb') as f:
        c = pickle.load(f)

    # print(c[0].get_conversation())
    print(c[0].gender)
    print(c[0].id)
