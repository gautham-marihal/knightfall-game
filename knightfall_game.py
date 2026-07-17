import pygame
import random

pygame.init()

screen_pannel = 150
screen_width, screen_height = 800, 400 + screen_pannel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battle")

font = pygame.font.SysFont("Times New Roman", 26)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0,0,0)
gold = (255, 215, 0)

background_img = pygame.image.load(r"img/Background/background.png").convert_alpha()
# background_img = pygame.transform.scale(background_img, (1280, 720))
pannel_img = pygame.image.load(r"img/Icons/panel.png").convert_alpha()
potion_img = pygame.image.load(r"img/Icons/potion1.png").convert_alpha()
potion_img = pygame.transform.scale(potion_img, (40, 40))
defeat_img = pygame.image.load(r"img/Icons/defeat.png").convert_alpha()
victory_img = pygame.image.load(r"img/Icons/victory.png").convert_alpha()

pygame.mixer.init()

attack_sound = pygame.mixer.Sound(r"sounds/22_Slash_04.wav")
impact_sound = pygame.mixer.Sound(r"sounds/15_Impact_flesh_02.wav")
block_sound = pygame.mixer.Sound(r"sounds/39_Block_03.wav")
death_sound = pygame.mixer.Sound(r"sounds/69_Enemy_death_01.wav")


clock = pygame.time.Clock()
FPS = 60

def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))

def bg():
    screen.blit(background_img, (0,0))

def pannel():
    screen.blit(pannel_img, (0, screen_height - screen_pannel))

    draw_text(f'{knight.name} HP: {knight.health} ', font, red, 160, screen_height - screen_pannel + 10)

    screen.blit(potion_img, (100,screen_height - screen_pannel + 40))
    draw_text(f'Wave: {wave}', font, gold, 20, screen_height - screen_pannel + 10)
    draw_text(f': {knight.potions}', font, green, 180, screen_height - screen_pannel + 50)
    draw_text('A/D: Move   SPACE: Attack', font, black, 75, screen_height - screen_pannel + 85)
    draw_text('S: Shield   H: Heal', font, black, 75, screen_height - screen_pannel + 108)
    

    for count, i in enumerate(bandit_list):
        draw_text(f'{i.name} HP: {i.health} ', font, red, 550, (screen_height - screen_pannel + 10) + count * 30)


class Fighter:
    def __init__(self, x, y, name, max_health, strength, potions):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.strength = strength
        self.potions = potions
        self.alive = True
        self.blocking = False
        self.flip = False  
        self.state = "chase"
        self.ai_timer = random.randint(30, 90) 
        self.attack_cooldown = 0
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Adding Idle Images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            # self.animation_list.append(img)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # Adding Attacking Images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            # self.animation_list.append(img)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # Adding Hurt Images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            # self.animation_list.append(img)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        

        # Adding Death Images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            # self.animation_list.append(img)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)        

    def update(self):
        self.animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        #To check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # To create a loop
        if self.frame_index >= len(self.animation_list[self.action]): # Has only 7 indices

            if self.action == 1:
                self.action = 0
                self.frame_index = 0

            elif self.action == 2:
                self.action = 0
                self.frame_index = 0

            elif self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1

            else:
                self.frame_index = 0

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def take_damage(self, amount):
        if not self.alive:
            return
        if self.blocking:
            amount = amount// 3
            knockback = 2.5
            block_sound.play()
        else:
            knockback = 20
            impact_sound.play()
        self.health -= amount

        if self.name == "Knight":
            self.rect.x -= knockback
        else:
            self.rect.x += knockback

        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.action = 3
            self.frame_index = 0
            if self.name != "Knight":
                death_sound.play()

        else:
            self.action = 2
            self.frame_index = 0

    def attack(self, target):
        if not self.alive or not target.alive:
            return
        if self.attack_cooldown == 0:
            attack_sound.play()
            target.take_damage(self.strength)
            self.attack_cooldown = 45
            self.action = 1
            self.frame_index = 0
       

    def draw(self):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(flipped_image, self.rect)


ATTACK_RANGE = 100

def bandit_ai(bandit, knight):
    if not bandit.alive:
        return

    bandit.ai_timer -= 1
    if bandit.ai_timer <= 0:
        bandit.ai_timer = 90
        distance = abs(bandit.rect.centerx - knight.rect.centerx)

        if bandit.health < bandit.max_health * 0.3 and bandit.potions > 0:
            bandit.state = "heal"
        elif bandit.health < bandit.max_health * 0.4:
            bandit.state = "retreat"
        elif distance <= ATTACK_RANGE:
            bandit.state = random.choice(["attack", "block"])
        else:
            bandit.state = "chase"

    if bandit.state == "chase":
        bandit.blocking = False
        distance = abs(bandit.rect.centerx - knight.rect.centerx)
        if distance > ATTACK_RANGE:
            if bandit.rect.centerx < knight.rect.centerx:
                bandit.rect.x += 2
                bandit.flip = False
            else:
                bandit.rect.x -= 2
                bandit.flip = True
        else:
            bandit.flip = bandit.rect.centerx < knight.rect.centerx


    elif bandit.state == "retreat":
        bandit.blocking = False
        if bandit.rect.centerx < knight.rect.centerx:
            bandit.rect.x -= 2
            bandit.flip = True
        else:
            bandit.rect.x += 2
            bandit.flip = False

    elif bandit.state == "block":
        bandit.blocking = True

    elif bandit.state == "heal":
        bandit.blocking = False
        bandit.health = min(bandit.max_health, bandit.health + 15)
        bandit.potions -= 1
        bandit.state = "retreat"

    elif bandit.state == "attack":
        bandit.blocking = False
        distance = abs(bandit.rect.centerx - knight.rect.centerx)
        if distance <= ATTACK_RANGE:
            bandit.attack(knight)
        else:
            bandit.state = "chase"

    bandit.rect.x = max(0, min(screen_width - bandit.rect.width, bandit.rect.x))

class Health_Bar():
    def __init__(self, fighter, offset_y=20):
        self.fighter = fighter
        self.offset_y = offset_y

    def draw_health(self):
        health_ratio = self.fighter.health / self.fighter.max_health
        x = self.fighter.rect.centerx - 40
        y = self.fighter.rect.top - self.offset_y
        pygame.draw.rect(screen, red, (x, y, 80, 10))
        pygame.draw.rect(screen, green, (x, y, 80 * health_ratio, 10))

def draw_bandit_health_bars():
    for b in bandit_list:
        if b.alive:
            health_ratio = b.health / b.max_health
            x = b.rect.centerx - 40
            y = b.rect.top - 20
            pygame.draw.rect(screen, red, (x, y, 80, 10))
            pygame.draw.rect(screen, green, (x, y, 80 * health_ratio, 10))

def load_high_wave():
    try:
        file = open("Highestscore.txt", "r")
        value = int(file.read())
        file.close()
        return value
    except:
        return 1
    
def high_wave_save(value):
    file = open("Highestscore.txt", "w")
    file.write(str(value))
    file.close()
    


def spawn_wave(wave_num):
    count = min(1 + wave_num// 2, 5)

    new_bandit = []
    spacing = screen_width // (count + 1)
    for i in range(count):
        x = spacing *(i + 1)
        health = 50 + (wave_num -1) * 10
        strength = 6 + (wave_num - 1) * 2
        b = Fighter(x, 270, "Bandit", health, strength, 1)
        new_bandit.append(b)
    return new_bandit

def reset_game():
    global knight, bandit_list, wave
    global knight_health_bar

    wave = 1
    knight = Fighter(200, 260, "Knight", 100, 30, 3)
    bandit_list = spawn_wave(wave)

    knight_health_bar = Health_Bar(knight)
        

wave = 1
high_wave = load_high_wave()
knight = Fighter(200, 260, "Knight", 100, 30, 3)
bandit_list = spawn_wave(wave)
knight_health_bar = Health_Bar(knight)
wave_transition_timer = 0


running = True
paused = False

while running:

    clock.tick(FPS)

    bg()

    pannel()

    keys = pygame.key.get_pressed()
    knight.blocking = keys[pygame.K_s]

    if not paused:
        knight.update()
        knight.draw()
        for bandit in bandit_list:
            bandit.update()
            bandit.draw()
            bandit_ai(bandit, knight)

        knight_health_bar.draw_health()
        draw_bandit_health_bars()

        if knight.alive == False:
            screen.blit(defeat_img, (275, 200))

        if all(not b.alive for b in bandit_list) and wave_transition_timer == 0:
            wave_transition_timer = FPS * 2 

        if wave_transition_timer > 0:
            draw_text(f'Wave {wave} Cleared!', font, gold, 300, 200)
            wave_transition_timer -= 1
            if wave_transition_timer == 0:
                wave += 1
                bandit_list = spawn_wave(wave)
                if wave > high_wave:
                    high_wave = wave
                    high_wave_save(high_wave)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not knight.blocking:
                living_bandits = [b for b in bandit_list if b.alive]
                if len(living_bandits) > 0:
                    knight.attack(living_bandits[0])

            if event.key == pygame.K_h and knight.potions >= 1 and knight.alive:
                knight.health += 15
                if knight.health > knight.max_health:
                    knight.health = knight.max_health
                knight.potions -= 1

            if event.key == pygame.K_ESCAPE:
                running = False
            
            if event.key == pygame.K_p:
                paused = not paused
                
    keys = pygame.key.get_pressed()
    if knight.alive and not paused:
        if (keys[pygame.K_a] and knight.rect.left > 0) or (keys[pygame.K_LEFT] and knight.rect.left > 0):
            knight.rect.x -= 4
            knight.flip = True
        if (keys[pygame.K_d] and knight.rect.right < screen_width) or (keys[pygame.K_RIGHT] and knight.rect.right < screen_width):
            knight.rect.x += 4
            knight.flip = False
    
    if paused:
        draw_text('PAUSED', font, gold, 350, 200)
        draw_text("Press 'P' to Resume", font, gold, 320, 250)


    game_over = False

    if knight.alive == False:
        screen.blit(defeat_img, (275, 200))
        draw_text("Press R to Restart", font, gold, 300, 350)
        draw_text(f"Best Wave: {high_wave}", font, gold, 300, 385)
        game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and game_over:
        reset_game()


    pygame.display.flip()
pygame.quit()