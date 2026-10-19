import pygame
import random

pygame.init()
ScreenWidth = 800
ScreenHeight = 600
window = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("Collision & Score")

#Random Pixels to spawn the Enemy
EnemySpawnX = random.randint(0,800)
EnemySpawnY = random.randint(0,600)

#Enemy movements
MovementCooldown = 600
LastMovement = 0
EnemyWalkSpeed = 12
EnemyRunSpeed = 20

#Colors
BlueColor = (0, 150, 255)
GreenColor = (34, 139, 34)
RedColor = (250,0,0)
WhiteColor = (254, 254, 254)

Player = pygame.Rect(400,520, 50, 50)
Enemy = pygame.Rect(EnemySpawnX, EnemySpawnY, 50, 50)
Speed = 12 #Player Speed
Score = 0
EnemyRange = 300 #pixels range from player to enemy
EnemyRangeSquare = EnemyRange * EnemyRange
Clock = pygame.time.Clock()
TimeStart= pygame.time.get_ticks()
TimeLimit = 30000
GameActive = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Player's movement
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_LEFT]:
        Player.x -= Speed
    if keys[pygame.K_RIGHT]:
        Player.x += Speed
    if keys[pygame.K_UP]:
        Player.y -= Speed
    if keys[pygame.K_DOWN]:
        Player.y += Speed

    #Player Screen Limit Credit
    #Credit: https://realpython.com/lessons/staying-on-the-screen/
    if Player.left < 0:
        Player.left = 0
    if Player.right > ScreenWidth:
        Player.right = ScreenWidth
    if Player.top < 0:
        Player.top = 0
    if Player.bottom >= ScreenHeight:
        Player.bottom = ScreenHeight

    #credit:
    #https://pikuma.com/blog/math-for-game-developers
    #https://www.w3schools.com/python/ref_func_abs.asp
    #https://itch.io/blog/658632/16-bit-vector-normalization-finally-putting-that-math-major-to-work
    DistenceX = Enemy.x - Player.x
    DistenceY = Enemy.y - Player.y
    DistenceSquare = DistenceX * DistenceX + DistenceY * DistenceY

    if DistenceSquare <= EnemyRangeSquare:
        # If DistenceX have more space than DistenceY
        if abs(DistenceX) > abs(DistenceY):
            #Amount and direction the enemy will move
            MoveAmountX = EnemyRunSpeed if DistenceX > 0 else - EnemyRunSpeed 
            UpdatedX = Enemy.x + MoveAmountX
            #left and right
            if UpdatedX < 0 or UpdatedX + Enemy.width > ScreenWidth:
                # if x axis is blocked, move y axis
                if Enemy.y < Player.y:
                    Enemy.y -= EnemyRunSpeed
                else:
                    Enemy.y += EnemyRunSpeed
            else:
                Enemy.x = UpdatedX
        else:

            #Amount and direction the enemy will move
            MoveAmountY = EnemyRunSpeed if DistenceY > 0 else -EnemyRunSpeed
            UpdatedY = Enemy.y + MoveAmountY
            #top and bottom
            if UpdatedY < 0 or UpdatedY + Enemy.height > ScreenHeight:
                #if y axis is blocked, move x axis
                if Enemy.x < Player.x:
                    Enemy.x -= EnemyRunSpeed
                else:
                    Enemy.x += EnemyRunSpeed
            else:
                Enemy.y = UpdatedY
    else:
        #Enemy Random movement with cooldown
        CurrentTime = pygame.time.get_ticks()
        if CurrentTime - LastMovement >= MovementCooldown:
            Direction = random.choice(['left', 'right', 'up', 'down', 'stop'])
            if Direction == 'left':
                Enemy.x -= EnemyWalkSpeed
            elif Direction == 'right':
                Enemy.x += EnemyWalkSpeed
            elif Direction == 'up':
                Enemy.y -= EnemyWalkSpeed
            elif Direction == 'down':
                Enemy.y += EnemyWalkSpeed
            LastMovement = CurrentTime

    # Enemy Screen Limit
    if Enemy.left < 0:
        Enemy.left = 0 + 25
    if Enemy.right > ScreenWidth - 25:
        Enemy.right = ScreenWidth
    if Enemy.top < 0 + 25:
        Enemy.top = 0 + 25
    if Enemy.bottom >= ScreenHeight - 25:
        Enemy.bottom = ScreenHeight - 25


    #change the square’s colour to red when a collision happens
    #Add secore when player touch
    if Player.colliderect(Enemy):
        Score += 1
        Score
        BlueColor = RedColor
      
        #Random Pixels to spawn the Enemy
        EnemySpawnX = random.randint(0,800)
        EnemySpawnY = random.randint(0,600)
        Enemy = pygame.Rect(EnemySpawnX, EnemySpawnY, 50, 50)
    else:
        BlueColor = (0, 150, 255)

    TimeNow = pygame.time.get_ticks()
    TimePasted = TimeNow - TimeStart
    TimeLeft = TimeLimit - TimePasted
    PrintTime = int(TimeLeft // 1000)
  
    #End screen
    if TimeLeft <= 0:
        BigTextFont = pygame.font.SysFont("Comic Sans MS", 60)
        SmallTextFont = pygame.font.SysFont("Comic Sans MS", 20)
        GameOverScreen = BigTextFont.render("GAME OVER", True, RedColor)
        FinalScoreText = BigTextFont.render(f"Score: {Score}", True, WhiteColor)
        #No one can get score 50 in this game within 30 second, so it would be point less to write a else if statement for this. Maybe proof me wrong!
        RageBaitingText = SmallTextFont.render(f"legend says that you will never score 50 since you are bad at this.", True, WhiteColor)
        window.blit(GameOverScreen, (ScreenWidth // 2 - GameOverScreen.get_width() // 2, 200))
        window.blit(FinalScoreText, (ScreenWidth // 2 - FinalScoreText.get_width() // 2, 300))
        window.blit(RageBaitingText, (ScreenWidth // 2 - RageBaitingText.get_width() // 2, 400))
        pygame.display.update()
        pygame.time.wait(10000)
        running = False
        break

    Clock.tick(60)
    window.fill((0, 0, 0))

    #Block Color
    pygame.draw.rect(window, GreenColor, Enemy)
    pygame.draw.rect(window, BlueColor, Player)
    font = pygame.font.SysFont("Comic Sans MS", 20)
    ScoreText = font.render(f"Score: {Score}", True, WhiteColor)
    TimeText = font.render(f"Time: {PrintTime}s", True, WhiteColor)

    window.blit(TimeText, (2,0))
    window.blit(ScoreText, (2,22))
    pygame.display.update()
pygame.quit()
