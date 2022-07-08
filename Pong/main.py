
import pygame
from pygame.locals import *
import os
import sys 

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
IMG_DIR = "imagenes"
SONIDO_DIR = "sonidos"
def load_image(nombre, dir_imagen, alpha=False): 
    ruta = os.path.join(dir_imagen, nombre)
    print(ruta)
    try: 
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + nombre) 
        sys.exit(1) 
    if alpha is True: 
        image = image.convert_alpha()
    else: 
        image = image.convert()
    return image
def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    try: 
        sonido = pygame.mixer.Sound(ruta)
    except (pygame.error) as message:
        print("no se pudo cargar el sonido: " + nombre)
        sonido = None 
    return sonido 
class Pelota(pygame.sprite.Sprite):
    "la bola y su comportamiento en pantalla"

    def __init__(self, sonido_tenis, sonido_aplausos):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bola.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx =SCREEN_WIDTH / 2 
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = [3, 3] 
        self.sonido_golpe = sonido_tenis
        self.sonido_punto = sonido_aplausos
    def update(self):
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed[0] = -self.speed[0] 
            self.sonido_punto.play()
            self.rect.centerx = SCREEN_WIDTH / 2
            self.rect.centery = SCREEN_HEIGHT / 2
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT: 
            self.speed[1] = -self.speed[1]
        self.rect.move_ip((self.speed[0], self.speed[1])) 
    def colision(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            self.speed[0] = -self.speed[0] 
            self.sonido_golpe.play() 
     
class Paleta(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("paleta.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.centery = SCREEN_HEIGHT / 2
        
    def humano(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0
    def cpu(self, Pelota):
        self.speed = [0, 2.5]
        if Pelota.speed[0] >= 0 and Pelota.rect.centerx >= SCREEN_WIDTH / 2: 
            if self.rect.centery > Pelota.rect.centery:
                self.rect.centery -= self.speed[1]
        if self.rect.centery < Pelota.rect.centery: 
            self.rect.centery += self.speed[1]

        
    


def main(): 
    pygame.init() 
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("El mismisimo Pong") 
    
    fondo = load_image("fondo.jpg", IMG_DIR, alpha=False) 
    fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))
    sonido_golpe = load_sound("sonido_tenis.ogg", SONIDO_DIR)
    sonido_punto = load_sound("sonido_aplausos.ogg", SONIDO_DIR) 
    bola = Pelota(sonido_golpe, sonido_punto) 
    jugador1 = Paleta(40)
    jugador2 = Paleta (SCREEN_WIDTH - 40)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25) 
    pygame.mouse.set_visible(False)

    while 1:
        pos_mouse = pygame.mouse.get_pos()
        mov_mouse = pygame.mouse.get_rel()



        clock.tick(60)

        jugador1.humano()
        jugador2.cpu(bola)
        bola.update()
        bola.colision(jugador1)
        bola.colision(jugador2)
       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    jugador1.rect.centery -= 5
                elif event.key == K_s:
                    jugador1.rect.centery += 5 
                elif event.key == K_UP:
                    jugador1.rect.centery -= 5
                elif event.key == K_DOWN:
                    jugador1.rect.centery += 5
                elif event.key == K_ESCAPE:
                    sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    jugador1 .rect.centery += 0
                elif event.key == K_DOWN:
                    jugador1.rect.centery += 0
            elif mov_mouse[1] != 0:
                jugador1.rect.centery = pos_mouse[1]

        screen.blit(fondo, (0, 0)) 
        todos = pygame.sprite.RenderPlain(bola, jugador1, jugador2)
        todos.draw(screen)
        pygame.display.flip() 

if __name__ == "__main__":
    main()
