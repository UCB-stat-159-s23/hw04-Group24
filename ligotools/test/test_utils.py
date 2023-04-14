import numpy as np
from scipy.interpolate import interp1d
from ligotools.utils import whiten, write_wavfile, reqshift, draw_plot
from ligotools import readligo as rl
from scipy.io import wavfile
import h5py
import json
import os
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
from scipy import signal

import matplotlib.mlab as mlab
from scipy.signal import butter, filtfilt


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



def test_draw_plot(fs = 4096):


    eventname = 'GW150914'
    fnjson = f"{PROJECT_PATH}/data/BBH_events_v3.json"
    events = json.load(open(fnjson, "r"))
    event = events[eventname]
    fn_H1 = event['fn_H1']
    fn_L1 = event['fn_L1']


    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(f'{PROJECT_PATH}/data/'+fn_H1, 'H1')
    strain_L1, time_L1, chan_dict_L1 = rl.loaddata(f'{PROJECT_PATH}/data/'+fn_L1, 'L1')


    NFFT = 4 * fs
    psd_window = np.blackman(NFFT)
    # and a 50% overlap:
    NOVL = int(NFFT / 2)

    # define the complex template, common to both detectors:




    fn_template = event['fn_template']
    f_template = h5py.File(f'{PROJECT_PATH}/data/' + fn_template, "r")
    template_p, template_c = f_template["template"][...]
    template = (template_p + template_c * 1.j)


    # the length and sampling rate of the template MUST match that of the data.
    datafreq = np.fft.fftfreq(template.size) * fs
    df = np.abs(datafreq[1] - datafreq[0])

    # to remove effects at the beginning and end of the data stretch, window the data
    # https://en.wikipedia.org/wiki/Window_function#Tukey_window
    try:
        dwindow = signal.tukey(template.size, alpha=1. / 8)  # Tukey window preferred, but requires recent scipy version
    except:
        dwindow = signal.blackman(template.size)  # Blackman window OK if Tukey is not available

    # prepare the template fft.
    template_fft = np.fft.fft(template * dwindow) / fs

    # loop over the detectors
    dets = ['H1', 'L1']
    for det in dets:

        if det == 'L1':
            data = strain_L1.copy()
        else:
            data = strain_H1.copy()

        # -- Calculate the PSD of the data.  Also use an overlap, and window:
        data_psd, freqs = mlab.psd(data, Fs=fs, NFFT=NFFT, window=psd_window, noverlap=NOVL)

        # Take the Fourier Transform (FFT) of the data and the template (with dwindow)
        data_fft = np.fft.fft(data * dwindow) / fs

        # -- Interpolate to get the PSD values at the needed frequencies
        power_vec = np.interp(np.abs(datafreq), freqs, data_psd)

        # -- Calculate the matched filter output in the time domain:
        # Multiply the Fourier Space template and data, and divide by the noise power in each frequency bin.
        # Taking the Inverse Fourier Transform (IFFT) of the filter output puts it back in the time domain,
        # so the result will be plotted as a function of time off-set between the template and the data:
        optimal = data_fft * template_fft.conjugate() / power_vec
        optimal_time = 2 * np.fft.ifft(optimal) * fs

        # -- Normalize the matched filter output:
        # Normalize the matched filter output so that we expect a value of 1 at times of just noise.
        # Then, the peak of the matched filter output will tell us the signal-to-noise ratio (SNR) of the signal.
        sigmasq = 1 * (template_fft * template_fft.conjugate() / power_vec).sum() * df
        sigma = np.sqrt(np.abs(sigmasq))
        SNR_complex = optimal_time / sigma

        # shift the SNR vector by the template length so that the peak is at the END of the template
        peaksample = int(data.size / 2)  # location of peak in the template
        SNR_complex = np.roll(SNR_complex, peaksample)
        SNR = abs(SNR_complex)

        # find the time and SNR value at maximum:
        indmax = np.argmax(SNR)
        timemax = time_H1[indmax]
        SNRmax = SNR[indmax]

        # Calculate the "effective distance" (see FINDCHIRP paper for definition)
        # d_eff = (8. / SNRmax)*D_thresh
        d_eff = sigma / SNRmax
        # -- Calculate optimal horizon distnace
        horizon = sigma / 8

        # Extract time offset and phase at peak
        phase = np.angle(SNR_complex[indmax])
        offset = (indmax - peaksample)

        # apply time offset, phase, and d_eff to template
        template_phaseshifted = np.real(template * np.exp(1j * phase))  # phase shift the template
        template_rolled = np.roll(template_phaseshifted, offset) / d_eff  # Apply time offset and scale amplitude

        # Whiten and band-pass the template for plotting
        template_whitened = whiten(template_rolled, interp1d(freqs, data_psd), time_H1[1]-time_H1[0])  # whiten the template
        fband = event['fband']
        Pxx_H1, freqs = mlab.psd(strain_H1, Fs=fs, NFFT=NFFT)
        Pxx_L1, freqs = mlab.psd(strain_L1, Fs=fs, NFFT=NFFT)

        # We will use interpolations of the ASDs computed above for whitening:
        psd_H1 = interp1d(freqs, Pxx_H1)
        psd_L1 = interp1d(freqs, Pxx_L1)
        strain_H1_whiten = whiten(strain_H1, psd_H1, time_H1[1]-time_H1[0])
        strain_L1_whiten = whiten(strain_L1, psd_L1, time_H1[1]-time_H1[0])
        bb, ab = butter(4, [fband[0] * 2. / fs, fband[1] * 2. / fs], btype='band')
        normalization = np.sqrt((fband[1] - fband[0]) / (fs / 2))
        template_match = filtfilt(bb, ab, template_whitened) / normalization  # Band-pass the template

        print('For detector {0}, maximum at {1:.4f} with SNR = {2:.1f}, D_eff = {3:.2f}, horizon = {4:0.1f} Mpc'
              .format(det, timemax, SNRmax, d_eff, horizon))
        strain_H1_whitenbp = filtfilt(bb, ab, strain_H1_whiten) / normalization
        strain_L1_whitenbp = filtfilt(bb, ab, strain_L1_whiten) / normalization
        # plotting changes for the detectors:
        if det == 'L1':
            pcolor = 'g'
            strain_whitenbp = strain_L1_whitenbp

        else:
            pcolor = 'r'
            strain_whitenbp = strain_H1_whitenbp

        tevent = event['tevent']
        draw_plot(time_H1, timemax, strain_whitenbp, template_match, SNR, det, eventname, 'png', pcolor, tevent,
                  template_fft, datafreq, d_eff, freqs, data_psd, fs)

