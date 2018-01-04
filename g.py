from ECG import *
import matplotlib.pyplot as plt
from scipy import signal

model=ECG(256.0,25,'DataN.txt')
model.run()

model.process()
