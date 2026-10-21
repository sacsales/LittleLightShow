import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import pygame 
from random import choice, randint, uniform




CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()



p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK) #take mic input

#plt.ion()
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



#plt.show(block=False)


particle_group = pygame.sprite.Group()

def spawn_particles(n):
    for _ in range(n):
        pos = pygame.mouse.get_pos()
        color = choice(("red", "green", "blue"))
        direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        direction = direction.normalize()
        speed = randint(50, 400)
        Particle(particle_group, pos, color, direction, speed)


def main():

    running = True 



    try:
        while running: 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Press Esc to quit
                        exit()
                elif event.type == pygame.QUIT:
                    exit()
                #elif event.type == pygame.MOUSEBUTTONDOWN:
                    #spawn_particles(200)

            if not running:
                break
            
            

            data = stream.read(CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) #turn bytes to ints 
            line.set_ydata(samples) #update the heights 

            samples -= samples.mean() #remove offset from bg noise
            mag = np.abs(np.fft.rfft(samples * window)) #funky fft stuff. how much of each frequency is in each sample? 

            newMag = mag[1:] * 4 / (CHUNK * 32768)

            bass = newMag[(freq_bins >= 20) & (freq_bins < 250)]
            bass_strength = np.mean(bass) if len(bass) else 0
            print("Bass:", bass_strength)

            # 5. Convert strength to a 0–1 value
            bass_level = np.clip(bass_strength * 100, 0, 1)

                # 6. Spawn particles according to loudness
            particle_count = int(bass_level * 10)

            if particle_count > 0:
                spawn_particles(particle_count)



            dt = clock.tick() / 1000
            screen.fill((0,0,0))
            particle_group.draw(screen)
            particle_group.update(dt)
            pygame.display.flip() 

            print("Bass:", bass_strength, "Particles:", particle_count)

            
            
            

            #line_fft.set_ydata(newMag) #fft adds up everything! divide by no. of samples * 32768 - convert from very very number to something on scale 

            #fig.canvas.draw() 
            #fig.canvas.flush_events()
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    
    
        

        

class Particle(pygame.sprite.Sprite):
    def __init__(self, groups, pos, color, direction, speed):
        super().__init__(groups)
        self.pos = pygame.math.Vector2(pos) 
        self.color = color 
        self.direction = direction 
        self.speed = speed
        self.alpha = 255 
        self.fade_speed = 500 
        self.create_surf()

    def create_surf(self):
        self.image = pygame.Surface((4,4)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(surface=self.image, color=self.color, center=(2,2), radius=2)
        self.rect = self.image.get_rect(center=self.pos)


    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos 

    

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt 
        self.image.set_alpha(self.alpha)

    def check_alpha(self):
        if self.alpha <= 0:
            self.kill()

    def check_pos(self):
        if (self.pos[0] < -50 or 
            self.pos[0] > SCREEN_WIDTH + 50 or 
            self.pos[1] < -50 or 
            self.pos[1] > SCREEN_HEIGHT + 50):
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.check_pos()
        self.fade(dt)
        self.check_alpha()



       
if __name__ == "__main__":
    main()




        

        
        
