

from dis import dis
import pygame
import pymunk
import random
from pymunk.vec2d import Vec2d
LARGURA=1000
ALTURA=600
pygame.init()
display=pygame.display.set_mode((LARGURA,ALTURA))
pygame.display.set_caption("Hockey")
audio_point=pygame.mixer.Sound("point.ogg")
audio_point.set_volume(0.5)
audio_jogo=pygame.mixer.Sound("audio-editor.mp3")
audio_jogo.set_volume(0.05)
audio_start= pygame.mixer.Sound("air-hockey.ogg")
audio_start.set_volume(0.02)
clock=pygame.time.Clock()
space=pymunk.Space()
fps=100
AMARELO=255,255,0
BRANCO=255,255,255
left=25
mid=282
rigth=975
top=35
bottom=565
middlex=500
middley=300
paused=False
point=4
goalheight = 50
goalwidth = 20
light_blue = (255,255,255)
image = pygame.image.load("disc.png")
image = pygame.transform.scale(image, (30, 30))
image_vermelha= pygame.image.load("redpad.png")
image_vermelha= pygame.transform.scale(image_vermelha, (40, 40))
image_azul = pygame.image.load("bluepad.png")
image_azul = pygame.transform.scale(image_azul, (40, 40))
image_start= pygame.image.load("start_screen.png")
image_start = pygame.transform.scale(image_start, (LARGURA,ALTURA))
image_tutorial= pygame.image.load("tutorial.png")
image_tutorial = pygame.transform.scale(image_tutorial, (LARGURA,ALTURA))

ball_radius=15
def print_text(text,x):
    font= pygame.font.SysFont("Algerian",20,True,False)
    surface=font.render(text,True,(255,255,255))
    display.blit(surface,(x,5))


class Ball():
    def __init__(self):
        self.body=pymunk.Body()
        self.reset(0,0,0)
        self.shape=pymunk.Circle(self.body,8)
        self.shape.density=1
        self.shape.elasticity=1
        space.add(self.body,self.shape)
        self.shape.collision_type=1
        self.velocity=500
    def draw(self):
        x,y=self.body.position
        pygame.draw.circle(display,(255,255,255),(int(x),int(y)),ball_radius)  
        display.blit(image, (int(x)-ball_radius,int(y)-ball_radius))
    def draw2(self):
        x,y=self.body.position
        pygame.draw.circle(display,(0,255,255),(int(x),int(y)),ball_radius)  
        display.blit(image, (int(x)-ball_radius,int(y)-ball_radius))
 
    def reset(self,space=0,arbiter=0,data=0):
        self.body.position=middlex,middley
        self.body.velocity=-400*random.choice([-1,1]),-100*random.choice([-1,1])   
        return False  
    def standardize_velocity(self,space=0,arbiter=0,data=0):
        self.body.velocity=self.body.velocity*(self.velocity/self.body.velocity.length)     
        self.velocity += 10


class Wall():
    def __init__(self,p1,p2,colission_number=None):
        self.body=pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape=pymunk.Segment(self.body,p1,p2,10)
        self.shape.elasticity = 1
        space.add(self.body,self.shape)
        if colission_number:
            self.shape.collision_type=colission_number

    def draw(self):
        pygame.draw.line(display,(255,255,255),self.shape.a,self.shape.b,10)

class Wall2():
    def __init__(self,p1,p2,colission_number=None):
        self.body=pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape=pymunk.Segment(self.body,p1,p2,10)
        self.shape.elasticity = 1
        space.add(self.body,self.shape)
        if colission_number:
            self.shape.collision_type=colission_number

    def draw(self):
        pygame.draw.line(display,(0,0,0),self.shape.a,self.shape.b,10)

class Jogador:
    def __init__(self,x):
        self.body = pymunk.Body()        
        self.body.position = x,middley
        self.shape = pymunk.Circle(self.body,20)
        self.shape.elasticity=1
        self.shape.density=1
        space.add(self.body,self.shape)
        self.shape.collision_type=100
        self.score=0
       
 

    def draw(self):
         x,y=self.body.position
         pygame.draw.circle(display,(255,255,255),(int(x),int(y)),20)
         display.blit(image_vermelha, (int(x)-20,int(y)-20))


    def on_edge(self):
        if self.body.local_to_world([0,-20])[1]<= top:
            self.body.velocity=0,0
            self.body.position= self.body.position[0], top+30
        if self.body.local_to_world([0,20])[1]>=bottom:
            self.body.velocity=0,0
            self.body.position= self.body.position[0],bottom-30
        if self.body.local_to_world([20,0])[1]>=bottom:
            self.body.velocity=0,0
            self.body.position= self.body.position[0],bottom-30
   
        
        
    
   
    def mover(self,up=True):
        if up:
            self.body.velocity=0,-500
        else:
            self.body.velocity=0,500
    
    def parar(self):
        self.body.velocity=0,0  
    def andar(self,left=True):
        if left:
            self.body.velocity=500,0
        else:
            self.body.velocity=-500,0
class Jogador2:
    def __init__(self,x):
        self.body = pymunk.Body()        
        self.body.position = x,middley
        self.shape = pymunk.Circle(self.body,20)
        self.shape.elasticity=1
        self.shape.density=1
        self.shape.collision_type= 2
        space.add(self.body,self.shape)
        self.shape.collision_type=100
        self.score=0
 

    def draw(self):
         x,y=self.body.position
         pygame.draw.circle(display,(255,255,255),(int(x),int(y)),20)
         display.blit(image_azul, (int(x)-20,int(y)-20))


    def on_edge(self):
        if self.body.local_to_world([0,-20])[1]<= top:
            self.body.velocity=0,0
            self.body.position= self.body.position[0], top+30
        if self.body.local_to_world([0,-20])[1]<=top:
            self.body.velocity=0,0
            self.body.position= self.body.position[0], top+30
       
    
        if self.body.local_to_world([0,20])[1]>=bottom:
            self.body.velocity=0,0
            self.body.position= self.body.position[0],bottom-30
        
   
    def mover(self,up=True):
        if up:
            self.body.velocity=0,-800
        else:
            self.body.velocity=0,800
    
    def parar(self):
        self.body.velocity=0,0  
    def andar(self,left=True):
        if left:
            self.body.velocity=800,0
        else:
            self.body.velocity=-800,0


def game():
    ball = Ball()
    wall_left3=Wall([left,bottom/3 +150],[left,bottom])
    wall_left2=Wall([left,top],[left,bottom/3+150])
    wall_left4=Wall2([left,bottom/3 +150],[left,bottom/3+60],102)
    wall_rigth=Wall([rigth,top],[rigth,bottom/3+150])
    wall_rigth2=Wall([rigth,bottom/3 +150],[rigth,bottom])
    wall_rigth3=Wall2([rigth,bottom/3 +150],[rigth,bottom/3+60],101)
    wall_top=Wall([left,top],[rigth,top])
    wall_bottom=Wall([left,bottom],[rigth,bottom])

    player1=Jogador(left+15)
    player2=Jogador2(rigth-15)
    scored_1= space.add_collision_handler(1,101)
    scored_2= space.add_collision_handler(1,102)
   

    def player1_scored(space,arbiter,data):
        player1.score+=1
        audio_jogo.stop()
        audio_point.play()
        ball.reset()
        return False
    scored_1.begin= player1_scored
    def player2_scored(space,arbiter,data):
        player2.score+=1
        audio_jogo.stop()
        audio_point.play()
        ball.reset()
        return False
    scored_2.begin= player2_scored
    contact_with_player= space.add_collision_handler(1,100)
    contact_with_player.post_solve = ball.standardize_velocity




    

    end_it=False
    while(end_it==False):
        display.fill((0,0,0))
        display.blit(image_start,(0,0))
        myfont=pygame.font.SysFont("Britannic Bold", 40)
        nlabel=myfont.render("OLA JOGADOR!CLIQUE NA TELA PARA VISUALIZAR O TUTORIAL.", 1, (255, 0, 0))
        audio_start.play()
        for event in pygame.event.get():
                if event.type== pygame.MOUSEBUTTONDOWN:
                    end_it=True
        display.blit(nlabel,(50,20))
        pygame.display.flip()
    end_its=False
    while(end_its==False):
        pygame.display.update()
        display.fill((0,0,0))
        display.blit(image_tutorial,(0,0))
        myfont=pygame.font.SysFont("Britannic Bold", 40)
        nlabel=myfont.render("", 1, (255, 0, 0))
        for event in pygame.event.get():
                if event.type== pygame.MOUSEBUTTONDOWN:
                    audio_start.stop()
                    end_its=True
        display.blit(nlabel,(300,20))
        pygame.display.flip()

    while True:
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
               return
                   
        if not player2.on_edge():
            if pygame.key.get_pressed()[pygame.K_w]:
                    player2.mover()
            elif pygame.key.get_pressed()[pygame.K_s]:
                    player2.mover(False)
            elif pygame.key.get_pressed()[pygame.K_d]:
                player2.andar()
            elif pygame.key.get_pressed()[pygame.K_a]:
                player2.andar(False)
                    
            else:
                player2.parar()
        if not player1.on_edge():
            if pygame.key.get_pressed()[pygame.K_UP]:
                    player1.mover()
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    player1.mover(False)
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                player1.andar()
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                player1.andar(False)
            
            else:
                player1.parar()  

        

       
                    
              
            
        display.fill((0,0,255))
        ball.draw()
        wall_left2.draw()
        wall_left3.draw()
        wall_left4.draw()
        wall_bottom.draw()
        wall_top.draw()
        wall_rigth.draw()
        wall_rigth2.draw()
        wall_rigth3.draw()
        player1.draw()
        player2.draw()
        print_text(f"Jogador 1 = {player1.score}",left)
        print_text(f"Jogador 2 = {player2.score}",rigth-160)
        pygame.draw.line(display,(255,255,255),[middlex,top],[middlex,bottom],4)
        pygame.display.update()
        clock.tick(fps)
        space.step(1/fps)
        audio_jogo.play()

game()
pygame.quit()
