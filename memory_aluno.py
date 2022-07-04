import pygame, sys
import random, math
from pygame.locals import *
from pygame import mixer
#Classe Botão criada
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

mixer.init()
mixer.music.load('sons-musicas/retro-90s-arcade-machine.mp3')
mixer.music.set_volume(0.7)
mixer.music.play(-1)
'''
ATENCAO: procure pelas marcações 'TODO', pois elas indicam 
onde deverá ser codificado. Leia os comentarios ao longo do 
código. Leia a documentação do pygame para os métodos que você
tiver dúvida.
'''

# Constantes
FPS = 60
W_SIZE = [800, 100]
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CLOCK = pygame.time.Clock()

NUMBER_CARDS = 16
CARD_SIZE = [W_SIZE[0]/NUMBER_CARDS, W_SIZE[1]]
# setup inicial da biblioteca e da janela - DISPLAYSURF é onde desenham-se os elementos
pygame.init()
DISPLAYSURF = pygame.display.set_mode((W_SIZE[0], W_SIZE[1]))

pygame.time.set_timer(pygame.USEREVENT, 1000) # veja na doc. do pygame

# Função de Menu
def main_menu():

   SCREEN = pygame.display.set_mode((1280, 720))
   pygame.display.set_caption("Menu")

   BG = pygame.image.load("assets/wallhaven-rd989q_1280x720.png")

   def get_font(size):  # Returns Press-Start-2P in the desired size
      return pygame.font.Font("assets/font.ttf", size)

   while True:
      SCREEN.blit(BG, (0, 0))

      MENU_MOUSE_POS = pygame.mouse.get_pos()

      MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
      MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

      PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                           text_input="JOGAR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
      OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                              text_input="SOBRE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
      QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                           text_input="SAIR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

      SCREEN.blit(MENU_TEXT, MENU_RECT)

      for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
         button.changeColor(MENU_MOUSE_POS)
         button.update(SCREEN)

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
               main()
            if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
               options()
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
               pygame.quit()
               sys.exit()
      pygame.display.update()


#Função tela Opções
def options():
   SCREEN = pygame.display.set_mode((1280, 720))
   pygame.display.set_caption('Sobre')
   texto = ("Cada jogador deverá levantar duas cartas de uma vez,tentando encontrar o par."
            "Se a segunda carta virada for diferente da primeira,passa um tempo,com o desenho para baixo, e passar a vez.")

   print(texto)
   def get_font(size):  # Returns Press-Start-2P in the desired size
      fonte = pygame.font.Font("assets/font.ttf", size)
      return fonte


   while True:
      OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
      SCREEN.fill("white")
      OPTIONS_TEXT = get_font(10).render(texto, True, "Black")
      OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
      SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

      OPTIONS_BACK = Button(image=None, pos=(640, 460),
                            text_input="SAIR", font=get_font(75), base_color="Black", hovering_color="Green")

      OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
      OPTIONS_BACK.update(SCREEN)

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         if event.type == pygame.MOUSEBUTTONDOWN:
            if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
               main_menu()

      pygame.display.update()

def sound():
   paired_sound = mixer.Sound('sons-musicas/game-notification.wav')
   paired_sound.play()

# Helpers
def init():
   """ Inicializa variaveis globais """
   global deck_cards, exposed, cards_clicked, cards_paired
   global state, number_turns, t_count, font_surf, font_messg, surf_messg


   define_message("")
   t_count = 0 # conta os segundos
   state = 0 # estado do jogo: relativo as cartas viradas pelo usuario (uma ou duas)
   number_turns = 0 # numero de turnos (duas cartas viradas = 1 turno)
   cards_clicked = [] # salva o par de cartas clicadas, pelos seus indices
   cards_paired = 0 # quantidade de pares de cartas descobertas
   # cartas do jogo
   deck_cards = [(str(i) if i < NUMBER_CARDS/2 else str(NUMBER_CARDS%i)) for i in range(NUMBER_CARDS)]
   random.shuffle(deck_cards)
   exposed = [False] * NUMBER_CARDS # guarda os indices relativos ao deck de cartas

   # texto para as cartas: repare que ele é relativo ao deck de cartas
   font_obj = pygame.font.Font('freesansbold.ttf', 50)
   font_surf = []
   for c in deck_cards:
      surf = pygame.font.Font.render(font_obj, c, True, WHITE)
      rect = surf.get_rect()
      font_surf.append([surf, rect])

   # texto para a mensagem no fim do jogo
   font_messg = pygame.font.Font('freesansbold.ttf', 20)
   surf_messg = pygame.font.Font.render(font_messg, msg_intro, True, YELLOW)


def define_message(msg):
   global msg_intro
   msg_intro = msg
   

# Event handlers
def timer_handler():
   """ Contador do tempo (seg.):
   O comando pygame.time.set_timer(pygame.USEREVENT, 1000) customiza
   um evento (USEREVENT) que sera disparado a cada segundo. Esse evento 
   sera capturado (no loop principal) e esta funcao sera chamada.
   """
   global t_count
   t_count += 1
    

def draw():
   """ Desenha """
   global font_surf

   i = 0

 #Posição
   j = CARD_SIZE[0] / 2
   for x in range(NUMBER_CARDS):
      ''' 
      Se uma carta estiver exposta, entao o vetor 'font_surf' 
      deve ser usado para centralizar a sua posicao. Caso contrario,
      um poligono deve ser desenhado. A variável 'j' irá auxiliar para
      definir posicao central do texto da carta, enquanto a variavel 'i' 
      irá te auxiliar a definir a posicao do poligono. Pense em como
      você também pode usar a variavel 'CARD_SIZE' para definir os pontos
      do polígono.
      '''
      if exposed[x]:
         font_surf[x][1] = j,0

      else:
         pygame.draw.rect(DISPLAYSURF, RED, pygame.Rect(i, 0, CARD_SIZE[0], CARD_SIZE[1]), 2)
      i += CARD_SIZE[0]
      j += CARD_SIZE[0]
   pass


def mouse_click(pos):
   """ 
   Recupera o indice da carta clicada e
   atualiza o numero de turnos 
   """
   global state, number_turns, cards_clicked, cards_paired
   global msg_intro, exposed, surf_messg
   # indice da carta
   if(pos[0]<=W_SIZE[0]):
      index = math.floor(pos[0]/50)

   if not exposed[index]:
      if state == 0:
         state = 1
      elif state == 1:
         state = 2
         number_turns += 1 # fim de um turno

         if (cards_paired == 7) :
            define_message("Otimo! Voce terminou em " + str(t_count//60) + "min" + str(t_count%60) + "segs.")
            surf_messg = pygame.font.Font.render(font_messg, msg_intro, True, YELLOW)
            #Função para tocar som ao acertar os pares
            mixer.music.load('sons-musicas/game-over.wav')
            mixer.music.play()
      else:
         state = 1

         if (deck_cards[cards_clicked[0]] != deck_cards[cards_clicked[1]] ):
            exposed[cards_clicked[0]] = False
            exposed[cards_clicked[1]] = False
         else:
            sound()
            cards_paired += 1

         cards_clicked = []


      cards_clicked.append(index)

      exposed[index] = True

def main():
   pygame.display.set_caption('Memory')
   global font_surf, surf_messg

   init()
   while True:
      DISPLAYSURF.fill(GREEN)

      for event in pygame.event.get():
         if event.type == QUIT:
            pygame.quit()
            sys.exit()
         if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            mouse_click(pos)
         if event.type == pygame.USEREVENT:
            timer_handler()

      # desenha
      draw()
      for x in range(NUMBER_CARDS):
         if exposed[x]:
            DISPLAYSURF.blit(font_surf[x][0], font_surf[x][1])

      DISPLAYSURF.blit(surf_messg, [5, W_SIZE[1]-20])

      pygame.display.update()
      CLOCK.tick(FPS)

main_menu()