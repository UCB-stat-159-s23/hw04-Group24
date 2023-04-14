import numpy as np
from scipy.interpolate import interp1d
from ligotools.utils import whiten, write_wavfile, reqshift, draw_plot
from scipy.io import wavfile

# test whiten function
def test_whiten():
    strain = np.random.randn(10000)
    dt = 1/2048
    freqs = np.fft.rfftfreq(len(strain), dt)
    interp_psd = interp1d(freqs, np.ones(len(freqs)))
    white_ht = whiten(strain, interp_psd, dt)
    assert isinstance(white_ht, np.ndarray)
    assert len(white_ht) == len(strain)

# test write_wavfile function
def test_write_wavfile(tmpdir):
    filename = str(tmpdir.join("test.wav"))
    fs = 44100
    data = np.random.randn(2*fs)
    write_wavfile(filename, fs, data)

    rate, read_data = wavfile.read(filename)
    assert rate == fs
    assert np.array_equal(np.int16(data/np.max(np.abs(data)) * 32767 * 0.9), read_data)

# test reqshift function
def test_reqshift():
    data = np.random.randn(10000)
    shifted_data = reqshift(data, fshift=200, sample_rate=2048)
    assert isinstance(shifted_data, np.ndarray)
    assert len(shifted_data) == len(data)



def test_draw_plot():
    # Han: TODO: test draw_plot function. There are undefined variables and unimported packages in the function.
    #
    # make_plots = True
    # dets = ['L1', 'H1']
    # for det in dets:
    #     draw_plot(make_plots, det)
    pass
