"""File: nlp_server.py

Authors: Mattijs Blankesteijn & András Csirik
Computational Dialogue Modelling 2020

This file contains a way of quickly running the CoreNLP server.
Server is hardcoded to run on localhost:9000
"""

import os
import requests

def start():
    """ """
    os.chdir('corenlp')
    c = 'java -mx3g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
            -preload tokenize \
            -status_port 9000 -port 9000 -timeout 30000 &'
    os.system(c)

def stop():
    """Shutdown CoreNLP server."""
    c  = 'wget "localhost:9000/shutdown?key=`cat /tmp/corenlp.shutdown`" -O -'
    os.system(c)

if __name__ == '__main__':
    try:
        requests.head("http://localhost:9000")
        stop()
    except:
        start()
