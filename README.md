# LittleLightShow! 

## Overview ##
A sound-sensitive lightshow! Designed for use as a makeshift background for a band performance. Can be hooked up to a projector, like in demo, or just as a backing screen. 

## Usage ##
- Clone repo, install dependences to your venv
- Run, and place near a source of music. Live or recorded is fine.

## Demo ## 


https://github.com/user-attachments/assets/4e6345dd-1d5d-4445-b6f1-5d892be460a1


https://github.com/user-attachments/assets/8421502b-c8e4-4fcd-b54f-e54b802d9170



## How does it work? ##
- PyAudio takes in stream of input from computer microphone.
- NumPy does a Fast Fourier Transform (FFT) on it in chunks, splitting it into its frequency components (ie, how much 20Hz is in this sample?)
- Frequency components sorted into ranges, or 'buckets'.
    - Bass: 20-150Hz
    - Low Mids: 150-400Hz
    - High Mids: 300-3500Hz
    - Highs/Sparkle: 3500-12000Hz
- Relative 'strength' of each bucket computed and normalized to fit on a 0-1 scale
- Using PyGame, particles of a certain color, size and speed spawn on screen based on strength of bucket. The larger and slower, the lower the frequency. Also, adds a waveform of the current sound (made with Matplotlib)

## Libraries/Dependencies/Versions ##
- python                    3.14.6
- matplotlib                3.11.2
- numpy                     2.5.2
- PyAudio                   0.2.14
- pygame                    2.6.1

## Known Issues ## 
For very very loud sounds (ie, right next to an amplifier or something) tons and tons of particles will spawn and may cause some lag. 


## Tutorials/References 
- https://www.youtube.com/watch?v=O0Y8FChBaFU
- https://www.youtube.com/watch?v=rj9NOiFLxWA&t=207s
- https://www.youtube.com/watch?v=ZqpSb5p1xQo
- https://www.youtube.com/watch?v=AShHJdSIxkY&t=851s
- https://www.youtube.com/watch?v=aQKX3mrDFoY
- https://www.youtube.com/watch?v=ZiPWN39mGM0
 
      
