from scipy.io import wavfile
import numpy as np

fs, data = wavfile.read('input1.wav')
fs1, data1 = wavfile.read('output1.wav')
fs3, data3 = wavfile.read("D:\\do an\\KalmanFilter\\cough(63)1.wav")
kq = np.linalg.norm(data-data3)
kq1 = np.linalg.norm(data1-data3)
print(str(kq))
print(str(kq1))
