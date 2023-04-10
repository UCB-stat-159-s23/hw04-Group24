import pytest
import numpy as np
import os
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

"""
Really need some clarification from TA on this part. What 'FOUR' test?
"""

def test_read_frame(filename=f'{PROJECT_PATH}/data/H-H1_LOSC_4_V1-1126259446-32.gwf'):
    # TODO: add test for read_frame. But do we have a frame(.gwf) file?
    pass

def test_read_hdf5(filename=f'{PROJECT_PATH}/data/H-H1_LOSC_4_V1-1126259446-32.hdf5'):
    # TODO: add test for read_hdf5
    pass

def test_loaddata(filename=f'{PROJECT_PATH}/data/H-H1_LOSC_4_V1-1126259446-32.hdf5'):
    # TODO: add test for loaddata
    pass

def test_dq2segs():
    # TODO: add test for dq2segs
    pass

def test_dq_channel_to_seglist():
    # TODO: add test for dq_channel_to_seglist
    pass

if __name__ == '__main__':
    test_read_hdf5()


