import pyaudio
import numpy as np
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import matplotlib
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

LOWS_LOWER_BOUND = 20
MIDS_LOWER_BOUND = 250
MIDS_UPPER_BOUND = 800


p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK) #take mic input

#plt.ion()
fig, ax = plt.subplots(figsize=(15, 8))

x = np.arange(CHUNK) #make list of numbers. how many? chunk. 
freqs = np.fft.rfftfreq(CHUNK, 1 / RATE) #analysis's wave's x - all the different frequency buckets 
freq_bins = freqs[1:]
window = np.hanning(CHUNK) #smooth. 

line, = ax.plot(x, np.zeros(CHUNK), color="white") #make flat line. changes in loop
ax.set_position([0, 0, 1, 1])
ax.set_ylim(-32768, 32767)
ax.set_xlim(0, CHUNK)

fig.patch.set_facecolor("black")
ax.set_facecolor("black")
#ax2.set_facecolor("black")



#set scales and stuff 

#line_fft, = ax2.semilogx(freqs[1:], np.zeros(len(freqs) - 1), lw=2)
#semi log to fit the scale. remove 0hz (no log). xs at the freq buckets, ys at 0s

#ax2.set_xlim(20, RATE / 2)
#ax2.set_ylim(0, 0.1)  
#more scales!

matplotlib.use("Agg")

canvas = agg.FigureCanvasAgg(fig)

renderer = canvas.get_renderer()
raw_data = renderer.tostring_argb()
size = canvas.get_width_height()
plot_surface = pygame.image.fromstring(raw_data, size, "ARGB")
canvas.draw()

bands = {
    "bass":   (20, 150),
    "lowmid": (150, 400),
    "vocals": (300, 3500),
    "highs":  (3500, 12000),
}



#plt.show(block=False)


particle_group = pygame.sprite.Group()

def spawn_particles(n, color, radius):
    for _ in range(n):
        pos = (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))
        color = color
        direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        direction = direction.normalize()
        speed = randint(50, 400)
        Particle(particle_group, pos, color, direction, speed, radius=radius)


def main():

    running = True 


    try:
        while running: 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # esc to quit
                        exit()
                elif event.type == pygame.QUIT:
                    exit()
                #elif event.type == pygame.MOUSEBUTTONDOWN:
                    #spawn_particles(200)

            if not running:
                break
            
            dt = clock.tick() / 1000

            data = stream.read(CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) #turn bytes to ints 
            line.set_ydata(samples) #update the heights 
            canvas.draw()

            plot_surface = pygame.image.frombuffer(bytes(canvas.buffer_rgba()), canvas.get_width_height(),"RGBA")
            

            samples -= samples.mean() #remove offset from bg noise
            mag = np.abs(np.fft.rfft(samples * window)) #funky fft stuff. how much of each frequency is in each sample? 

            newMag = mag[1:] * 4 / (CHUNK * 32768)

            bass = newMag[(freq_bins >= 20) & (freq_bins < 150)]
            bass_strength = np.mean(bass) if len(bass) else 0
            bass_level = np.clip(bass_strength * 100, 0, 1)
            bass_particle_count = int(bass_level * 5)

            mids = newMag[(freq_bins >= 150) & (freq_bins < 400)]
            mids_strength = np.mean(mids) if len(mids) else 0
            mids_level = np.clip(mids_strength * 100, 0, 1)
            mids_particle_count = int(mids_level * 5)

            highMids = newMag[(freq_bins >= 300) & (freq_bins < 3500)]
            highMids_strength = np.mean(highMids) if len(highMids) else 0
            highMids_level = np.clip(highMids_strength * 100, 0, 1)
            highMids_particle_count = int(highMids_level * 5)

            highs = newMag[(freq_bins >= 3500) & (freq_bins < 12000)]
            highs_strength = np.mean(highs) if len(highs) else 0
            highs_level = np.clip(highs_strength * 100, 0, 1)
            highs_particle_count = int(highs_level * 10)
            
            total_particle_count = bass_particle_count + mids_particle_count + highs_particle_count + highMids_particle_count

            if total_particle_count > 0:
                spawn_particles(bass_particle_count, (0, 242, 193), 40) #cyan
                spawn_particles(mids_particle_count, (255, 44, 223), 20) #pink
                spawn_particles(highs_particle_count, (255, 136, 0), 10) #orange
                spawn_particles(highMids_particle_count, (0, 69, 255), 10) #elec blue


            
            screen.fill((0,0,0))
            plot_width, plot_height = plot_surface.get_size()

            plot_x = (SCREEN_WIDTH - plot_width) // 2
            plot_y = (SCREEN_HEIGHT - plot_height) // 2

            screen.blit(plot_surface, (plot_x, plot_y))
            particle_group.draw(screen)
            particle_group.update(dt)
            pygame.display.flip() 

            #print("Bass:", bass_strength, "Particles:", particle_count)


            #line_fft.set_ydata(newMag) #fft adds up everything! divide by no. of samples * 32768 - convert from very very number to something on scale 

            #fig.canvas.draw() 
            #fig.canvas.flush_events()
            
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    
    
        

#pygame particle stuff...




class Particle(pygame.sprite.Sprite):
    def __init__(self, groups, pos, color, direction, speed, radius):
        super().__init__(groups)
        self.pos = pygame.math.Vector2(pos) 
        self.color = color 
        self.direction = direction 
        self.speed = speed
        self.alpha = 255 
        self.fade_speed = 100 
        self.create_surf(radius)

    def create_surf(self, radius):
        self.image = pygame.Surface((80,80)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(surface=self.image, color=self.color, center=(40,40), radius=radius)
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




        

        
        
