import os, pygame, random
#things to add to game: scoreboard, different sound effects like simpsons theme song for opening, mmmm for eating one, ending is doh, looking up fonts that relate to simpsons, background?, change controls to be arrow keys

os.system("cls") #clears terminal

pygame.init()

width, height = 640, 480

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Homer Donut Dash!")

#RGB
screen_color = (15, 15, 15)
red = (255, 0, 0)
blue = (0,0,255)
green = (0, 255, 0)
white = (255, 255, 255)

app_running = True

cube_color = red
cube_size = 20
cube_x = width//2 #// means int division
cube_y = height//2

# carries a pair (x,y)
cube_body = []

fruit_color = blue
fruit_size = 20
fruit_x = (random.randrange(0, width-fruit_size)//fruit_size)*fruit_size #you divide first to choose an area on the screen then multiply to get the pixel value for the blue cube to show up on screen
fruit_y = (random.randrange(0, height-fruit_size)//fruit_size)*fruit_size

dx = 0
dy = 0 

game_delay = 8000 #ticks

text_content = "Game Over!"
font = pygame.font.Font(None, 50)

text_surface = font.render(text_content, True, white)
text_rect = text_surface.get_rect()
text_rect.center = (window.get_width() //2, window.get_height() //2)

text_content = "(Press R to restart)"
font = pygame.font.Font(None, 30)

text_surface2 = font.render(text_content, True, white)
text_rect2 = text_surface2.get_rect()
text_rect2.center = (window.get_width() //2, window.get_height() //2 + 50)

pygame.mixer.music.load("simpsons-theme.mp3")
sound_effect = pygame.mixer.Sound("homer-woohoo.mp3")

pygame.mixer.music.set_volume(0.1)

pygame.mixer.music.play(-1)

game_over = False
#---------------- main loop begins
while app_running:
    start_time = pygame.time.get_ticks()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -cube_size
                dx = 0
            if event.key == pygame.K_LEFT:
                dx = -cube_size
                dy = 0
            if event.key == pygame.K_DOWN:
                dy = cube_size
                dx = 0
            if event.key == pygame.K_RIGHT:
                dx = cube_size
                dy = 0
            if event.key == pygame.K_r:
                if game_over:
                    game_over = False
                    cube_x = width // 2
                    cube_y = height // 2
                    game_delay = 8000 # ticks
                    cube_body.clear()
                    fruit_x = (random.randrange(0, width-fruit_size)//fruit_size)*fruit_size
                    fruit_y = (random.randrange(0, height-fruit_size)//fruit_size)*fruit_size
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("simpsons-theme.mp3")
                    pygame.mixer.music.play()
                
    #lines make the body of snake and follows after eating fruit
    if not game_over:
        for i in range(len(cube_body)-1, 0, -1):
            cube_body[i] = cube_body[i-1]
            
        if len(cube_body) > 0:
            cube_body[0] = (cube_x, cube_y)
        
        cube_x += dx
        cube_y += dy
        
        #fruit collision check
        if cube_x == fruit_x:
            if cube_y == fruit_y:
                fruit_x = (random.randrange(0, width-fruit_size)//fruit_size)*fruit_size
                fruit_y = (random.randrange(0, height-fruit_size)//fruit_size)*fruit_size
                cube_body.append([cube_x - dx, cube_y - dy])
                sound_effect.play(loops=0)
                if game_delay > 2000:
                    game_delay -= 400
                
                
        if cube_x < 0 or cube_x > width:
            game_over = True
            
        if cube_y < 0 or cube_y > height:
            game_over = True
            
        for part in cube_body:
            if part[0] == cube_x and part[1] == cube_y:
                game_over = True
                
        if game_over:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("homer-doh.mp3")
            pygame.mixer.music.play()
    
    #drawing functions
    window.fill(screen_color)
    #draw snake
    if not game_over:
        pygame.draw.rect(window, cube_color, (cube_x, cube_y, cube_size, cube_size))
        if len(cube_body) > 0:
            for pair in cube_body:
                pygame.draw.rect(window, cube_color, (pair[0], pair[1], cube_size, cube_size))
        
        #draw fruit
        pygame.draw.rect(window, fruit_color, (fruit_x, fruit_y, fruit_size, fruit_size))
    
    #draw game over screen
    if game_over:
        window.blit(text_surface, text_rect)
        window.blit(text_surface2, text_rect2)
    
    #draws to the window
    pygame.display.update()
    
    #drawing functions end
    elapsed_time = pygame.time.get_ticks() - start_time
    delay = (game_delay / 60) - elapsed_time
    
    if delay > 0:
        pygame.time.delay(int(delay))
#---------------- main loop ends

pygame.quit()