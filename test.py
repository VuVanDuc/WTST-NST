import pywt
import numpy as np
import copy
from scipy.io import wavfile

fs, data = wavfile.read('input.wav')

w = pywt.Wavelet('db2')
maxlev = pywt.dwt_max_level(len(data), w.dec_len)
print("maximum level is " + str(maxlev))

L = 1
c = []
count = 0
count2 = 0

for level in range(1, maxlev + 1):
    coeffs = pywt.wavedec(data, 'db2', level=level)
    # cA = coeffs[0]
    # cD = coeffs[1:]
    coeff_arr, coeff_slice = pywt.coeffs_to_array(coeffs)
    WTC = copy.deepcopy(coeffs)
    WTR = copy.deepcopy(coeffs)
    # cdC = WTC[1:]
    # cdR = WTR[1:]
    coeff_arr_WTC, coeff_slice_WTC = pywt.coeffs_to_array(WTC)
    coeff_arr_WTR, coeff_slice_WTR = pywt.coeffs_to_array(WTR)
    # WTC.tolist()
    # WTR.tolist()
    std = np.std(coeff_arr_WTC)
    threshold = 18 * std
    # pywt.threshold(coeff_arr_WTR, threshold, 'less')
    for j in range(len(coeff_arr)):
        if abs(coeff_arr[j]) < threshold:
            coeff_arr_WTC[j] = 0
            count2 = count2 + 1
        else:
            count = count + 1
            coeff_arr_WTR[j] = 0
    # WTkC = WTC[1:]
    # WTkR = WTR[1:]
    # for j in range(len(cD)):
    #     cD_std = np.std(cD[j])
    #     threshold = 2.5 * cD_std
    #     for k in range(len(cD[j])):
    #         if cD[j][k] < threshold:
    #             WTkC[j][k] = 0
    #         else:
    #             WTkR[j][k] = 0
    WTC1 = pywt.array_to_coeffs(coeff_arr_WTC, coeff_slice_WTC, 'wavedec')
    WTR1 = pywt.array_to_coeffs(coeff_arr_WTR, coeff_slice_WTR, 'wavedec')
    # WTC[1:] = WTC1
    # WTR[1:] = WTR1
    Ck = pywt.waverec(WTC1, 'db2')
    Rk = pywt.waverec(WTR1, 'db2')
    L = L + 1
    data = Rk
    c.append(Ck)

DAS = [sum(x) for x in zip(c)]
PVS = Rk
# print(count)
# print(count2)
datare = np.asarray(PVS, dtype=np.int16)
datanoise = np.asarray(DAS, dtype=np.int16)
wavfile.write('output.wav', fs, datare)
wavfile.write('noise.wav', fs, datanoise)

