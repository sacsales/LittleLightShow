import pygame 
from random import choice, randint, uniform


clock = pygame.time.Clock()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()

running = True 


particle_group = pygame.sprite.Group()

def spawn_particles(n):
    for i in range(n):
        pos = pygame.mouse.get_pos()
        color = choice(("red", "green", "blue"))
        direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        direction = direction.normalize()
        speed = randint(50, 400)
        Particle(particle_group, pos, color, direction, speed)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press Esc to quit
                    exit()
            elif event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                spawn_particles(200)

        dt = clock.tick() / 1000
        screen.fill((0,0,0))
        particle_group.draw(screen)
        particle_group.update(dt)
        pygame.display.flip() 
       
    


class Particle(pygame.sprite.Sprite):
    def __init__(self, groups, pos, color, direction, speed):
        super().__init__(groups)
        self.pos = pos 
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
            self.pos[1] > SCREEN_WIDTH + 50):
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.check_pos()
        self.fade(dt)
        self.check_alpha()



       
if __name__ == "__main__":
    pygame.init()
    main()


