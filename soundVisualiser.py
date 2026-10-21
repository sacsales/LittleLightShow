import pyaudio
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK) #take mic input

plt.ion()
fig, (ax, ax2) = plt.subplots(2, figsize=(15, 8)) #plots

x = np.arange(CHUNK) #make list of numbers. how many? chunk. 
freqs = np.fft.rfftfreq(CHUNK, 1 / RATE) #analysis's wave's x - all the different frequency buckets 
freq_bins = freqs[1:]
window = np.hanning(CHUNK) #smooth. 

line, = ax.plot(x, np.zeros(CHUNK)) #make flat line. changes in loop
ax.set_ylim(-32768, 32767)
ax.set_xlim(0, CHUNK)
#set scales and stuff 

line_fft, = ax2.semilogx(freqs[1:], np.zeros(len(freqs) - 1), lw=2)
#semi log to fit the scale. remove 0hz (no log). xs at the freq buckets, ys at 0s

ax2.set_xlim(20, RATE / 2)
ax2.set_ylim(0, 0.1)  
#more scales!

bands = {
    "bass":   (20, 150),
    "lowmid": (150, 400),
    "vocals": (300, 3500),
    "highs":  (3500, 12000),
}



plt.show(block=False)

try:
    while plt.fignum_exists(fig.number):
        data = stream.read(CHUNK, exception_on_overflow=False)
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) #turn bytes to ints 
        line.set_ydata(samples) #update the heights 

        samples -= samples.mean() #remove offset from bg noise
        mag = np.abs(np.fft.rfft(samples * window)) #funky fft stuff. how much of each frequency is in each sample? 

        newMag = mag[1:] * 4 / (CHUNK * 32768)
        
        bass = newMag[(freq_bins >= 20) & (freq_bins < 250)]
        bass_strength = np.mean(bass) if len(bass) else 0
        print("Bass:", bass_strength)

        line_fft.set_ydata(newMag) #fft adds up everything! divide by no. of samples * 32768 - convert from very very number to something on scale 

        fig.canvas.draw() 
        fig.canvas.flush_events()

    
        



        

        
        
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()