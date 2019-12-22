import pywt
import numpy as np
import copy
from scipy.io import wavfile

fs, data = wavfile.read('input')
w = pywt.Wavelet('db2')
maxlev = pywt.dwt_max_level(len(data), w.dec_len)
data_orgin = copy.deepcopy(data)
c = []
for level in range(1, maxlev + 1):
    coeffs = pywt.wavedec(data, 'db2', level=level)
    coeff_arr, coeff_slice = pywt.coeffs_to_array(coeffs)
    WTC = copy.deepcopy(coeffs)
    WTR = copy.deepcopy(coeffs)
    coeff_arr_WTC, coeff_slice_WTC = pywt.coeffs_to_array(WTC)
    coeff_arr_WTR, coeff_slice_WTR = pywt.coeffs_to_array(WTR)
    std = np.std(coeff_arr_WTC)
    threshold = 18 * std
    for j in range(len(coeff_arr)):
        if abs(coeff_arr[j]) < threshold:
            coeff_arr_WTC[j] = 0
            count2 = count2 + 1
        else:
            count = count + 1
            coeff_arr_WTR[j] = 0
    WTC1 = pywt.array_to_coeffs(coeff_arr_WTC, coeff_slice_WTC, 'wavedec')
    WTR1 = pywt.array_to_coeffs(coeff_arr_WTR, coeff_slice_WTR, 'wavedec')
    Ck = pywt.waverec(WTC1, 'db2')
    Rk = pywt.waverec(WTR1, 'db2')
    data = Rk
    c.append(Ck)

# DAS = [sum(x) for x in zip(c)]
PVS = Rk
datare = np.asarray(PVS, dtype=np.int16)
# datanoise = np.asarray(DAS, dtype=np.int16)
wavfile.write('output', fs, datare)
# wavfile.write('noise.wav', fs, datanoise)

