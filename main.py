# importy
import pygame
import random

pygame.init()

# Screen
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Harry Potter and Goblet of Fire")

# settings
pumpkin_speed = 5
egg_speed_set = 6
egg_speed_plus = 0.25
score_set = 0
lives_set = 5
egg_station = 100
goblet_speed = 13.41

# Nechceme měnit tynastavené hodnoty, a tak je dáváme do promněných, se kterými budeme moci manipulovat
lives = lives_set
score = score_set
egg_speed = egg_speed_set

# colors
dark_yellow = pygame.Color("#938f0c")

# fonts
big_font = pygame.font.Font("fonts/Harry.ttf", 50)
mid_font = pygame.font.Font("fonts/Harry.ttf", 40)
small_font = pygame.font.Font("fonts/Harry.ttf", 30)
author_font = pygame.font.SysFont("Arial", 13)

# texts
# Nadpis hry
main_text = big_font.render("Harry Potter and Goblet of Fire", True, dark_yellow)
main_text_rect = main_text.get_rect()
main_text_rect.top = 5
main_text_rect.centerx = width//2

# Text- zemřel jsi
first_dead_text = mid_font.render("You died!", True, dark_yellow)
first_dead_text_rect = first_dead_text.get_rect()
first_dead_text_rect.center = (width//2, height//2)

# Text- pro pokračování zmáčkněte nějaké tlačítko
second_dead_text = small_font.render("For continue press a button.", True, dark_yellow)
second_dead_text_rect = second_dead_text.get_rect()
second_dead_text_rect.top = height//2+20
second_dead_text_rect.centerx = width//2

# Pokud pohár dojel a vyhrál jsi
victory_text = mid_font.render("You won! You get Goblet of Fire.", True, dark_yellow)
victory_text_rect = victory_text.get_rect()
victory_text_rect.center = (width//2, height//2)

author_name_text = author_font.render("Šimon Drápal October 2023", True, "white")
author_name_text_rect = author_name_text.get_rect()
author_name_text_rect.bottomright = (width - 5, height - 5)

# images
# Obrázek dýně
pumpkin_image = pygame.image.load("img/harryPotter.png")
pumpkin_image_rect = pumpkin_image.get_rect()
pumpkin_image_rect.left = 10
pumpkin_image_rect.centery = height//2

# Obrázek vajíčka
egg_image = pygame.image.load("img/egg-icon.png")
egg_image_rect = egg_image.get_rect()
egg_image_rect.centerx = width + egg_station
egg_image_rect.top = random.randint(60, height-48)

# Obrázek Poháru
goblet_image = pygame.image.load("img/Goblet_icon.png")
goblet_image_rect = goblet_image.get_rect()
goblet_image_rect.topright = (width + 18.6, 36)

# music and sound
boom_sound = pygame.mixer.Sound("media/boom.wav")
take_egg_sound = pygame.mixer.Sound("media/take_egg.wav")
boom_sound.set_volume(0.1)
take_egg_sound.set_volume(0.1)

pygame.mixer.music.load("media/bg-music-hp.wav")
pygame.mixer.music.play(-1, 0.0)

# fps and clock
fps = 60
clock = pygame.time.Clock()

# cyklus while for game
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        # Pokud chceme hru ukončit
        if event.type == pygame.QUIT:
            lets_continue = False

    # Přeuložení do keys- všechna tlačítka, která jsme zmáčknuli
    keys = pygame.key.get_pressed()
    # Pokud klikáme na tlačítko nahoru a zárověn není dýně úplně nahoře
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and pumpkin_image_rect.top > 60:
        pumpkin_image_rect.y -= pumpkin_speed
    # Pokud klikáme na tlačítko dolů a zároveň není dýně úplně dole
    elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and pumpkin_image_rect.bottom < height-4:
        pumpkin_image_rect.y += pumpkin_speed

    # Pokud vejce nechytíme a vejce se už dotklo levé strany
    if egg_image_rect.x < 0:
        # Mínus jeden život
        lives -= 1
        # Zpátky na začáteční místo, ale jiná y pozice
        egg_image_rect.y = random.randint(60, height-48)
        egg_image_rect.x = width + egg_station
        # Spuštění zvuku "boom"
        boom_sound.play()
    # Pokud vejce nechytíme, ale vejce se ještě nedotklo levé strany obrazovky
    else:
        # Vejce se znovu přiblíží
        egg_image_rect.x -= egg_speed

    # Kontrola pozice, jeslti se už pohár nedotkl konce
    if goblet_image_rect.left <= -5:
        # Vypsání textů
        screen.blit(victory_text, victory_text_rect)
        screen.blit(second_dead_text, second_dead_text_rect)
        # update hry
        pygame.display.update()
        # Hudba se zastaví
        pygame.mixer.music.stop()
        cykle = True
        # Čekání na hráče
        while cykle:
            for event in pygame.event.get():
                # Pokud zmáčkl jakékoliv tlačítko- hraběží od znovu
                if event.type == pygame.KEYDOWN:
                    # Nastavení zpátky proměnných
                    lives = lives_set
                    score = 0
                    egg_speed = egg_speed_set
                    # dýně zpatký na pozici
                    pumpkin_image_rect.y = height // 2
                    # Pohár zpátky na pozici
                    goblet_image_rect.right = width + 18.6
                    cykle = False
                    # Spuštění harry potter písničky
                    pygame.mixer.music.play(-1, 0.0)
                # Pokud klikl na křížek- hra končí
                elif event.type == pygame.QUIT:
                    lets_continue = False
                    cykle = False

    # Vyplnění černou barvou
    screen.fill("black")

    # Čára
    pygame.draw.line(screen, dark_yellow, (0, 60), (width, 60), 2)

    # Pokud dýně chytí vejce
    if pumpkin_image_rect.colliderect(egg_image_rect):
        score += 1
        # Náhodná y část
        egg_image_rect.top = random.randint(60, height - 48)
        egg_image_rect.centerx = width + egg_station
        # Přidání rychlosti vejci
        egg_speed += egg_speed_plus
        # Zvuk
        take_egg_sound.play()
        # Posunutí poháru
        goblet_image_rect.left -= goblet_speed

    # Blitováni textu a změna skóre + vyblitování skóre
    screen.blit(main_text, main_text_rect)
    score_text = mid_font.render(f"Score: {score}/70", True, dark_yellow)
    score_text_rect = score_text.get_rect()
    score_text_rect.top = 10
    score_text_rect.left = 10
    screen.blit(score_text, score_text_rect)

    lives_text = mid_font.render(f"Lives: {lives}", True, dark_yellow)
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.top = 10
    lives_text_rect.right = width-10
    screen.blit(lives_text, lives_text_rect)

    screen.blit(author_name_text, author_name_text_rect)

    # blit obrázků
    screen.blit(pumpkin_image, pumpkin_image_rect)
    screen.blit(egg_image, egg_image_rect)
    screen.blit(goblet_image, goblet_image_rect)

    # Pokud mám 0 životů
    if lives == 0:
        # Vyblitování textů
        screen.blit(first_dead_text, first_dead_text_rect)
        screen.blit(second_dead_text, second_dead_text_rect)
        # Update + pozastavení hudby
        pygame.display.update()
        pygame.mixer.music.stop()
        cykle = True
        # Cyklus pro výběr uživatele
        while cykle:
            for event in pygame.event.get():
                # Pokud chce pokračovat
                if event.type == pygame.KEYDOWN:
                    # Proměnné zpátky do normálu
                    lives = lives_set
                    score = 0
                    egg_speed = egg_speed_set
                    # Vrácení dýně
                    pumpkin_image_rect.y = height//2
                    # Vrácení poháru
                    goblet_image_rect.right = width + 18.6
                    cykle = False
                    # Začátek hudby
                    pygame.mixer.music.play(-1, 0.0)
                # Pokud chce hru ukončit
                elif event.type == pygame.QUIT:
                    lets_continue = False
                    cykle = False

    # update hry
    pygame.display.update()

    # fps
    clock.tick(fps)

# Konec pygame
pygame.quit()
