import pywt
from scipy.io import wavfile
import numpy as np
import pyyawt

fs, data = wavfile.read('input.wav')
maxlev = pywt.dwt_max_level(len(data), pywt.Wavelet('db2').dec_len)
coeffs = pyyawt.dwt1d.wavedec(data, maxlev, 'db2')
datarec = pywt.waverec(coeffs, 'db2')
datare = np.asarray(datarec, dtype=np.int16)
wavfile.write('output.wav', fs, datare)

