""" Test functions in readligo.py """

import json
import os

import numpy as np

import ligotools.readligo as rl

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

fnjson = f"{PROJECT_PATH}/data/BBH_events_v3.json"
events = json.load(open(fnjson, "r"))
eventname = 'GW150914'
event = events[eventname]

fn_H1 = event['fn_H1']
fn_L1 = event['fn_L1']



def test_read_hdf5(filename=f"{PROJECT_PATH}/data/H-H1_LOSC_4_V2-1126259446-32.hdf5"):
    strain, gpsStart, ts, qmask, shortnameList, injmask, injnameList = rl.read_hdf5(filename)
    assert isinstance(strain, np.ndarray)
    assert isinstance(gpsStart, np.int64)
    assert isinstance(ts, np.float64)
    assert isinstance(qmask, np.ndarray)
    assert isinstance(shortnameList, list)
    assert isinstance(injmask, np.ndarray)
    assert isinstance(injnameList, list)


def test_loaddata():
    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(f"{PROJECT_PATH}/data/" + fn_H1, 'H1')
    strain_L1, time_L1, chan_dict_L1 = rl.loaddata(f"{PROJECT_PATH}/data/" + fn_L1, 'L1')
    assert isinstance(strain_H1, np.ndarray)
    assert isinstance(time_H1, np.ndarray)
    assert isinstance(chan_dict_H1, dict)
    assert isinstance(strain_L1, np.ndarray)
    assert isinstance(time_L1, np.ndarray)
    assert isinstance(chan_dict_L1, dict)


def test_dq2segs():
    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(f"{PROJECT_PATH}/data/" + fn_H1, 'H1')
    segs = rl.dq2segs(chan_dict_H1['BURST_CAT3'], time_H1[0])
    assert isinstance(segs, rl.SegmentList)
    for seg in segs:
        assert all(type(x) == int for x in seg)


def test_dq_channel_to_seglist(DQflag = 'CBC_CAT3'):
    _, _, chan_dict = rl.loaddata(f'{PROJECT_PATH}/data/' + fn_L1, 'H1')
    # Test with a dictionary input
    channel_dict = {'DEFAULT': np.array([0, 1, 1, 0, 0, 1, 1, 1])}
    segment_list = rl.dq_channel_to_seglist(channel_dict)
    assert type(segment_list) == list
    assert all(type(seg) == slice for seg in segment_list)

    # Test with a numpy array input
    channel = chan_dict[DQflag]
    segment_list = rl.dq_channel_to_seglist(channel)
    assert type(segment_list) == list
    assert all(type(seg) == slice for seg in segment_list)

