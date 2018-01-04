import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
class ECG:
    def __init__(self,sampling_rate,window_size,data_path):
        self.fs=sampling_rate
        self.N=window_size
        self.path=data_path
        self.f0=50.0
        self.Q=30.0
        self.f1=0.1
        self.f2=45.0

    def get_data(self):
        data = open(self.path, 'r')

        data = data.readlines()
        x = 0
        t = []
        y = []

        for i in data:
           t.append(x)
           x = x + 0.00390625
           m = float(i.rstrip())
           y.append(m)
        return (y,t)


    def notch_filter(self,data):

        w0 = self.f0 / (self.fs / 2)
        b, a = signal.iirnotch(w0, self.Q)
        return signal.lfilter(b, a, data)

    def bandpass_filter(self,data):
        w1 = self.f1 / (self.fs / 2)
        w2 = self.f2 / (self.fs / 2)
        b, a = signal.butter(4, [w1, w2], 'bandpass')
        return signal.lfilter(b, a, data)


    def differentiate(self,p):
        y=[]
        x0=0
        x1=0
        x2=0
        x3=0
        for i in range(len(p)):
            n0=i-1
            n1=i-2
            n2=i+1
            n3=i+2
            if n0<0:
                x0=0
            else:
                x0=p[n0]
            if n1<0:
                x1=0
            else:
                x1=p[n1]
            if n2>(len(p)-1):
                x2=0
            else:
                x2=p[n2]
            if n3>(len(p)-1):
                x3=0
            else:
                x3=p[n3]
            y.append((256/8)*(-x1-2*x0+2*x2+x3))
        return y
    def square(self,data):
        return [i ** 2 for i in data]


    def smooth(self,p):
        s=0
        N=self.N
        y=[]
        for n in range(len(p)):

            for j in range(N):
                m=n-(N-(j+1))
                if m>=0 and m<len(p):
                    s=s+p[m]


            y.append((1/N)*s)
            s=0

        return y
    def threshold(self,p):
        x=max(p)
        return 0.6*x
    def get_peaks_index(self,data,thr):
        last=0
        l=len(data)
        m=0
        n=self.N
        peaks=[]
        L=0

        while n<=l:
            x=data[m:n]
            t=max(x)
            T=data.index(t)

            if t>=thr and abs(T-last)>self.N :



                peaks.append(data.index(t))
                last = data.index(t)
                L=t
            elif t>=thr and abs(T-last)<=self.N:
                if t>L and n!=0 :
                    if not peaks:
                        print(" ")
                    else:

                        peaks.pop()

                    peaks.append(data.index(t))
                    last = data.index(t)
                    L = t




            m=m+self.N-1
            n=n+self.N-1
        return peaks
    def get_peaks_value(self,data,p):
        j=[]
        for i in p:
            j.append(data[i])
        return j
    def get_RR_interval(self,peaks):
        y=[]
        for i in range(len(peaks)-1):
            y.append(((peaks[i+1]-peaks[i])/256)*1000)
        return y
    def run(self):

        data,time= self.get_data()
        plt.subplot(1,2,1)

        plt.plot(time[:2000],data[:2000])
        plt.subplot(1,2,2)

        h=self.notch_filter(data)
        plt.plot(time[:2000],h[:2000])
        plt.show()
        hh=self.bandpass_filter(h)

        g=self.differentiate(hh)
        e=[i**2 for i in g]
        g=self.smooth(e)
        k=self.threshold(g)
        o=self.get_peaks_index(g,k)
        O=self.get_peaks_index(g[0:2000],k)

        u=[x/256 for x in O]
        c=[i for i in range(len(o))]
        v=self.get_peaks_value(g,O)
        b=self.get_RR_interval(o)

        #v=[i/500 for i in v]






        #plt.subplot(1,2,1)

        plt.plot(time[0:2000],g[0:2000])

        plt.plot(u,v,linestyle='None', marker='*', color='blue', markersize=10)
        plt.show()

        #plt.subplot(1,2,2)

        plt.plot(c[1:],b)
        plt.ylabel('RR')
        plt.xlabel('beat#')
#plt.plot(u,v,linestyle='None', marker='*', color='blue', markersize=10)




        plt.grid(True)
        plt.show()

    def process(self):
        block=[]
        data, time = self.get_data()
        h = self.notch_filter(data)
        hh = self.bandpass_filter(h)
        g = self.differentiate(hh)
        e = [i ** 2 for i in g]
        g = self.smooth(e)
        k = self.threshold(g)
        o = self.get_peaks_index(g, k)
        u = [x / 256 for x in o]
        c = [i for i in range(len(o))]
        v = self.get_peaks_value(g, o)
        b = self.get_RR_interval(o)
        AVG=(sum(b)/len(b))*1.1
        d=open('MissingBeats.txt','w')

        for i in range(len(b)):
            if b[i]>AVG:
                block.append(i+2)
                d.write("beat no " +str((i+2)*256)+"\n")


















