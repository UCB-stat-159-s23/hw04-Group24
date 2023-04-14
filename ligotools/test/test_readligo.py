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

"""
Really need some clarification from TA on this part. What 'FOUR' test?
"""


def test_read_frame(filename=f'{PROJECT_PATH}/data/H-H1_LOSC_4_V1-1126259446-32.gwf'):
    # TODO: add test for read_frame. But do we have a frame(.gwf) file?
    pass


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
    # TODO: add test for dq2segs
    pass


def test_dq_channel_to_seglist():
    # TODO: add test for dq_channel_to_seglist
    pass
