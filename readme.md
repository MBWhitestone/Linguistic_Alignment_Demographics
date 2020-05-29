## Computational Dialogue Modelling 2020
_On the Influence of Demographics on Linguistic Alignment_
> [MBWhitestone](https://github.com/MBWhitestone), [Csirika](https://github.com/Csirika)

This repository contains code created for our computational dialogue modelling project at the University of Amsterdam. It provides free software to inspect the [British National Corpus 2014](http://corpora.lancs.ac.uk/bnc2014/) with the [ConversAtion level Syntax SImilarity Metric (CASSIM)](https://doi.org/10.3758/s13428-017-0926-2) and [Linguistic Inquiry and Word Count (LIWC)](https://doi.org/10.1177%2F0261927X09351676) conversational alignment metric.

### Files & folders:
- `cassim_inspect.ipynb`: notebook for inspecting the output of `cassim_run.py`.
- `cassim_run.py`: code to run cassim on Conversations.
- `cassim.py`: a modified version of the [CASSIM](https://github.com/USC-CSSL/CASSIM/) metric.
- `conversations.py`: converts the BNC2014 to Conversation classes.
- `LICENSE`: all our software is released under MIT. Software in `cassim.py` is released under the GNU General Public License v2.0.
- `LIWC.py`: code to run the LIWC metric on BNC2014.
- `nlp_server.py`: run this before and after running `cassim_run.py`; it will either start or stop the CoreNLP server.
- `readme.md`: this file containing important information.
- `corenlp`: this _folder_ should contain an unpacked version of [CoreNLP](http://nlp.stanford.edu/software/stanford-corenlp-latest.zip).
- `data`: this _folder_ should contain an unpacked version of the [BNC2014](http://corpora.lancs.ac.uk/bnc2014/).

### Requirements:
- `Python3`
- `Java`
