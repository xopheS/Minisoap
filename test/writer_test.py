from minisoap.writer import Writer
from minisoap.generators import Silence, Sine
import time, wave, os, tempfile
from functools import reduce
import numpy as np
""" These tests works only locally
def round(t):
    return int(1000*t+.5)/1000.0

def abctest_kill():
    tmpf = tempfile.mktemp('.wav')
    w = Writer(Silence(), tmpf)
    w.start()
    time.sleep(.05)
    w.kill()
    assert True

def test_duration():
    st = Silence(.5)
    tmpf = tempfile.mktemp('.wav')
    w = Writer(st, tmpf)
    w.start()
    while not w.killed():
        time.sleep(0.1)
    wav = wave.open(tmpf, 'r')
    assert .5 == round(wav.getnframes()/float(wav.getframerate())/float(wav.getsampwidth()))

def test_channels():
    st = Silence(.5)
    tmpf = tempfile.mktemp('.wav')
    w = Writer(st, tmpf)
    w.start()
    while not w.killed():
        time.sleep(0.1)
    wav = wave.open(tmpf, 'r')
    assert wav.getnchannels() == Silence(.5).channels
def test_samplerate():

    st = Silence(.5)
    tmpf = tempfile.mktemp('.wav')
    w = Writer(st, tmpf)
    w.start()
    while not w.killed():
        time.sleep(0.1)
    wav = wave.open(tmpf, 'r')
    assert wav.getframerate()== Silence(.5).samplerate

def test__content():
    st = Silence(.5)
    tmpf = tempfile.mktemp('.wav')
    w = Writer(st, tmpf)
    w.start()
    ret = False
    while not w.killed():
        time.sleep(0.1)
    wav = wave.open(tmpf, 'r')
    for _ in range(wav.getnframes()):
        data = wav.readframes(1)
        if  data != b'\x00'*2*st.channels:
            break
    else: ret = True
    assert ret

"""
