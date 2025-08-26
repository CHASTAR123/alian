import pygame, os, pyautogui, random

WIDTH, HEIGHT = pyautogui.size()
pygame.font.init()
pygame.mixer.init()

battle_ground = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The space battleground')

bg = pygame.transform.scale(pygame.image.load('shipbgo.png'), (WIDTH, HEIGHT))

w = WIDTH / 40
h = HEIGHT / 20

font1 = pygame.font.SysFont('sans script', 50)
font2 = pygame.font.SysFont('Arial', 30)

start = pygame.time.get_ticks()
print(start)

game_state = 'start'

Lship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Lship.png'), (w, h)), -90)
Rship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Rship.png'), (w, h)), 90)

border = pygame.Rect(WIDTH / 2 - 10,0,20,HEIGHT)

red_hit = pygame.USEREVENT + 1
yellow_hit = pygame.USEREVENT + 2

winner_text = ''


def draw(rd, yw, yelwb, redb, rscore, yscore):
    global game_state, winner_text
    battle_ground.blit(bg, (0, 0))

    if game_state =='start':
        starting =font2.render('PRESS SPACE TO START YOUR PLAYER - ARROWS + RSHIFT TO SHOOT', 1, 'red')
        battle_ground.blit(starting, (50, HEIGHT/ 3))

    elif game_state == 'play':
        battle_ground.blit(Lship, (yw.x,yw.y))
        battle_ground.blit(Rship, (rd.x,rd.y))
        pygame.draw.rect(battle_ground, "black", border)

        for i in yelwb:
            pygame.draw.rect(battle_ground, 'yellow', i)
        for i in redb:
            pygame.draw.rect(battle_ground, 'red', i)

        if rscore >= 10:
            winner_text ='Red wins'
        if yscore >= 10:
            winner_text ='Yellow wins'

        redtext = font1.render('RED ' +str(rscore), 1, 'red')
        yellowtext = font1.render('YELLOW ' +str(yscore), 1, 'yellow')

        battle_ground.blit(redtext, (WIDTH -200,30))
        battle_ground.blit(yellowtext, (30,30))

        if winner_text != "":
            game_state ='end'

    elif game_state =='end':
        winner = font1.render(winner_text, 1,'blue')
        battle_ground.blit(winner, (WIDTH / 3,HEIGHT / 3))

    pygame.display.update()


def handle_rd(rd, keypressed):
    if keypressed[pygame.K_LEFT] and rd.x > border.x + border.width:
        rd.x -= 10
    if keypressed[pygame.K_RIGHT] and rd.x + rd.width < WIDTH:
        rd.x += 10
    if keypressed[pygame.K_UP] and rd.y > 0:
        rd.y -= 10
    if keypressed[pygame.K_DOWN] and rd.y + rd.height < HEIGHT:
        rd.y += 10


def ai_yellow(yw, yelwb, dt):
    wsad = pygame.time.get_ticks()
    #print(wsad - start)
    if wsad % 1000 <10:
        Cside = random.choice(["UP","DOWN","LEFT","RIGHT"])
        if Cside =="UP" and yw.y > 0:
            yw.y -= 10
        elif Cside == "DOWN" and yw.y + yw.height <HEIGHT:
            yw.y += 10
        elif Cside =="LEFT" and yw.x >0:
            yw.x -= 10
        elif Cside =="RIGHT" and yw.x + yw.width <border.x -10:
            yw.x += 10

    if random.randint(0, 190) == 1:
        bullet = pygame.Rect(yw.x +yw.width, yw.y + yw.height / 2,10, 5)
        yelwb.append(bullet)


def control_bullets(rd, yw, redb, yelwb):
    for b in yelwb:
        b.x += 5
        if b.x > WIDTH:
            yelwb.remove(b)
        elif b.colliderect(rd):
            yelwb.remove(b)
            pygame.event.post(pygame.event.Event(red_hit))

    for bt in redb:
        bt.x -=5
        if bt.x < 0:
            redb.remove(bt)
        elif bt.colliderect(yw):
            redb.remove(bt)
            pygame.event.post(pygame.event.Event(yellow_hit))


def maing():
    global game_state, yscore, rscore
    rd = pygame.Rect(WIDTH -50, HEIGHT/ 2, w, h)
    yw = pygame.Rect(50, HEIGHT /2, w, h)
    redb =[]
    yelwb = []
    rscore =0
    yscore =0

    clock = pygame.time.Clock()
    run = True
    while run:
        dt = clock.tick(60)
        print(dt)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

            if e.type ==pygame.KEYDOWN:
                if e.key ==pygame.K_RSHIFT:
                    bullet =pygame.Rect(rd.x, rd.y + rd.height / 2, 10, 5)
                    redb.append(bullet)
                if game_state =='start' and e.key== pygame.K_SPACE:
                    game_state ='play'
                if game_state =='end'and e.key ==pygame.K_SPACE:
                    game_state= 'start'
                    yscore= 0
                    rscore= 0
            if e.type == red_hit:
                yscore +=1
            if e.type == yellow_hit:
                rscore +=1

        keypressed =pygame.key.get_pressed()
        handle_rd(rd, keypressed)
        ai_yellow(yw, yelwb, dt)
        control_bullets(rd,yw, redb, yelwb)
        draw(rd,yw,yelwb,redb, rscore,yscore)


maing()
