import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 700

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Latin")

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED =   (211,   0,   0)
GREEN = (  0, 150,   0)
DGREEN = ( 0, 100,   0)
BLUE =  (  0,   0, 211)
LBLUE = (137, 207, 240)
GREY =  (201, 201, 201)
LGREY = (231, 231, 231)
LBROWN  = (185, 122, 87)
DBROWN = (159, 100, 64)

DURATION = 200 #ms
PADDING = 20

FONT = pygame.font.SysFont("consolas.ttf", 20)
TABLEFONT = pygame.font.SysFont("consolas.ttf", 25)
BIGFONT = pygame.font.SysFont("consolas.ttf", 60)
SMALLFONT = pygame.font.SysFont("consolas.ttf", 15)
MINIFONT = pygame.font.SysFont("consolas.ttf", 10)

#frames per second
FPS = 30

PERSONS = {
  1 : "1st sg",
  2 : "2nd sg",
  3 : "3rd sg",
  4 : "1st pl",
  5 : "2nd pl",
  6 : "3rd pl",
}

INDICATIVE = {
  "act": {
    "pres": {
      "portare": ["porto", "portas", "portat", "portamus", "portatis", "portant"],
      "monere": ["moneo", "mones", "monet", "monemus", "monetis", "monent"],
      "trahere": ["traho", "trahis", "trahit", "trahimus", "trahitis", "trahunt"],
      "audire": ["audio", "audis", "audit", "audimus", "auditis", "audiunt"],
      "capere": ["capio", "capis", "capit", "capimus", "capitis", "capiunt"],
    },
    "fut": {
      "portare": ["portabo", "portabis", "portabit", "portabimus", "portabitis", "portabunt"],
      "monere": ["monebo", "monebis", "monebit", "monebimus", "monebitis", "monebunt"],
      "trahere": ["traham", "trahes", "trahet", "trahemus", "trahetis", "trahent"],
      "audire": ["audiam", "audies", "audiet", "audiemus", "audietis", "audient"],
      "capere": ["capiam", "capies", "capiet", "capiemus", "capietis", "capient"],
    },
    "perf": {
      "portare": ["portavi", "portavisti", "portavit", "portavimus", "portavistis", "portaverunt"],
      "monere": ["monui", "monuisti", "monuit", "monuimus", "monuistis", "monuerunt"],
      "trahere": ["traxi", "traxisti", "traxit", "traximus", "traxistis", "traxerunt"],
      "audire": ["audivi", "audivisti", "audivit", "audivimus", "audivistis", "audiverunt"],
      "capere": ["cepi", "cepisti", "cepit", "cepimus", "cepistis", "ceperunt"],
    },
    "imp": {
      "portare": ["portabam", "portabas", "portabat", "portabamus", "portabatis", "portabant"],
      "monere": ["monebam", "monebas", "monebat", "monebamus", "monebatis", "monebant"],
      "trahere": ["trahebam", "trahebas", "trahebat", "trahebamus", "trahebatis", "trahebant"],
      "audire": ["audiebam", "audiebas", "audiebat", "audiebamus", "audiebatis", "audiebant"],
      "capere": ["capiebam", "capiebas", "capiebat", "capiebamus", "capiebatis", "capiebant"],
    },
    "plupf": {
      "portare": ["portaveram", "portaveras", "portaverat", "portaveramus", "portaveratis", "portaverant"],
      "monere": ["monueram", "monueras", "monuerat", "monueramus", "monueratis", "monuerant"],
      "trahere": ["traxeram", "traxeras", "traxerat", "traxeramus", "traxeratis", "traxerant"],
      "audire": ["audiveram", "audiveras", "audiverat", "audiveramus", "audiveratis", "audiverant"],
      "capere": ["ceperam", "ceperas", "ceperat", "ceperamus", "ceperatis", "ceperant"],
    },
  }
}

SUBJUNCTIVE = {
  "active": {
    "imperfect": {
      "portare": ["portare", "bam", "bas", "bat", "bamus", "batis", "bant"],
      "monere": ["monere", "bam", "bas", "bat", "bamus", "batis", "bant"],
      "trahere": ["trahere", "bam", "bas", "bat", "bamus", "batis", "bant"],
      "audire": ["audire", "bam", "bas", "bat", "bamus", "batis", "bant"],
      "capere": ["capere", "bam", "bas", "bat", "bamus", "batis", "bant"],
    },
    "pluperfect": {
      "portare": ["porta", "veram", "veras", "verat", "veramus", "veratis", "verant"],
      "monere": ["mon", "ueram", "ueras", "uerat", "ueramus", "ueratis", "uerant"],
      "trahere": ["tra", "xeram", "xeras", "xerat", "xeramus", "xeratis", "xerant"],
      "audire": ["audi", "veram", "veras", "verat", "veramus", "veratis", "verant"],
      "capere": ["cep", "eram", "eras", "erat", "eramus", "eratis", "erant"],
    },
  }
}

VERBS = {
  "indic": INDICATIVE,
  "subj": SUBJUNCTIVE,
}

opsW, opsH = WIDTH - PADDING*8,75
opsX, opsY = PADDING*4, HEIGHT/2
headerY = PADDING*2

def product(*args, repeat=1):
  # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
  # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
  pools = [tuple(pool) for pool in args] * repeat
  temp = []
  result = [[]]
  for pool in pools:
    result = [x+[y] for x in result for y in pool]
  for prod in result:
    temp.append(tuple(prod))
    
  return temp

VERBOPTIONS = [["pres", "fut", "imp", "perf", "plupf"], ["act", "pass"], ["indic", "subj", "imper", "infin", "ptcpl"], ["portare", "monere", "trahere", "audire", "capere"]]
VERBCOMBOS = product(*VERBOPTIONS)


OPTIONS = [VERBS]
OPTIONSSTRINGS = ["Verbs"]
OPTIONSRECTS = [pygame.Rect(opsX, opsY + (opsH + PADDING)*(x-1), opsW, opsH) for x in range(len(OPTIONS))]

class Menu:
  class header:
    def draw():
      pygame.draw.rect(WIN, LGREY, pygame.Rect(0, 0, WIDTH, headerY))
      pygame.draw.line(WIN, BLACK, (0, headerY), (WIDTH, headerY))
    def headings(headings, current):
      totalLen = 5
      for heading in headings:
        text = FONT.render(heading.upper(), 1, BLACK)
        if heading == current:
          pygame.draw.rect(WIN, BLACK, pygame.Rect(totalLen, 0, text.get_width()+PADDING, headerY+1), 1)
          pygame.draw.rect(WIN, WHITE, pygame.Rect(totalLen + 1, 1, text.get_width()+PADDING - 2, headerY+2))
        else:
          pygame.draw.rect(WIN, BLACK, pygame.Rect(totalLen, PADDING/5, text.get_width()+PADDING, headerY+1-PADDING/5), 1)
        WIN.blit(text, (totalLen + PADDING/2, (headerY-text.get_height())/2))
        totalLen += text.get_width()+PADDING-1
        
      text = FONT.render("Use LEFT and RIGHT to change mode", 1, BLACK)
      WIN.blit(text, ((WIDTH - PADDING - text.get_width(), (headerY-text.get_height())/2)))
  
  class table:
    def verbs(x, y, values = [], returnRects = False, parse = False):
      text = TABLEFONT.render("---------", 1, BLACK)
      rects = []
      cellH = text.get_height()+PADDING
      cell1W = text.get_width() + PADDING
      for row in PERSONS.values():
        indx = list(PERSONS.values()).index(row)
        rect = pygame.Rect(x, y + (cellH-1)*(indx), cell1W, cellH)
        pygame.draw.rect(WIN, BLACK, rect, 1)
        
        text = TABLEFONT.render(row, 1, BLACK)
        WIN.blit(text, (x + PADDING/2, y + (cellH-1)*(indx) + (cellH-text.get_height())/2))
        
        rect2 = pygame.Rect(x + cell1W - 1, y + (cellH-1)*(indx), cell1W*4, cellH)
        pygame.draw.rect(WIN, BLACK, rect2, 1)
        
        if len(values) == 6:
          text = TABLEFONT.render(values[indx], 1, BLACK)
          if parse == True:
            text = TABLEFONT.render("???", 1, RED)
          WIN.blit(text, (x + cell1W - 1 + PADDING/2, y + (cellH-1)*(indx) + (cellH-text.get_height())/2))
          rects.append([rect2, values[indx]])
          
      if returnRects == True:
        return rects
          
  class selectors:
    def verbs(x, y, selected):
      rects = [[] for _ in range(4)]
      options = VERBOPTIONS
      
      cellH = FONT.render("portare  ", 1, BLACK).get_height() + PADDING
      cellW = FONT.render("portare  ", 1, BLACK).get_width() + PADDING
      
      for row in options:
        for cell in row:
          indxR = options.index(row)
          indxC = row.index(cell)
          rect = pygame.Rect(x + (cellW + 3)*indxC, y + (cellH + 3)*indxR, cellW, cellH)
          if [indxR, indxC] in selected:
            pygame.draw.rect(WIN, LBLUE, rect)
          pygame.draw.rect(WIN, BLACK, rect, 1)
          
          text = FONT.render(cell, 1, BLACK)
          WIN.blit(text, (x + (cellW + 3)*indxC + PADDING/2, y + (cellH + 3)*indxR + PADDING/2))
          rects[indxR].append(rect)
      
      return rects
    
class Words:
  class verbs:
    def __init__(self, items, paths):
      self.selection = items # [a, b, c, d]
      self.paths = paths # [["pres", "fut", "imp", "perf", "plupf"], ["act", "pass"], ["indic", "subj", "imper", "infin", "ptcpl"], ["portare", "monere", "trahere", "audire", "capere"]]
      
    def generate(self):
      rand = random.randrange(0, len(self.selection))
      term = self.selection[rand]
      potentials = []
      for p in self.paths:
        initial = VERBS[p[2]][p[1]][p[0]][p[3]]
        for item in initial:
          if item == term:
            p.append(PERSONS[initial.index(item)+1])
            if p not in potentials:
              potentials.append(p)
      return term, potentials

class Verbpage:
  def __init__(self):
    self.page = "setup"
    self.pages = ["setup", "review", "parse", "type", "results"]
    
    self.items = None
    self.paths = None
    
    self.verbRects = None
    self.selected = []
    self.selectedPaths = [[] for _ in range(4)]
    self.words = None
    
    self.reviewRects = []
    self.reviewing = [[] for _ in range(4)]
    self.reviewingPaths = [[] for _ in range(4)]
    
    self.parseRects = []
    self.parsing = [[] for _ in range(4)]
    self.parsingPaths = [[] for _ in range(4)]
    self.parseGuess = ""
    
  def setItems(self, items, paths):
    self.items = items
    self.paths = paths
    self.words = Words.verbs(self.items, self.paths)
    
  def changePage(self, page):
    self.page = page
    
  def draw(self):
    Menu.header.draw()
    Menu.header.headings(self.pages, self.page)
    #Menu.table.verbs(PADDING*2, PADDING*5, ["moneo", "mones", "monet", "monemus", "monetis", "monent"])
    
    if self.page != "setup":
      if self.items == None:
        text = BIGFONT.render("Please set up the verbs", 1, RED)
        pygame.draw.rect(WIN, WHITE, pygame.Rect(0, headerY+4, WIDTH, HEIGHT-headerY-4))
        WIN.blit(text, ((WIDTH-text.get_width())/2, HEIGHT/6))
        
      elif self.page == "review":
        self.reviewRects = Menu.selectors.verbs(PADDING*5, PADDING*5, self.reviewing)
        if [] not in self.reviewing:
          try:
            temp = VERBS[self.reviewingPaths[2]][self.reviewingPaths[1]][self.reviewingPaths[0]][self.reviewingPaths[3]]
          except:
            temp = []
          Menu.table.verbs(PADDING*5, HEIGHT/2, temp)
        else:
          Menu.table.verbs(PADDING*5, HEIGHT/2)
          
      elif self.page == "parse":
        self.parseRects = Menu.selectors.verbs(PADDING*5, PADDING*5, self.parsing)
        if [] not in self.parsing:
          try:
            temp = VERBS[self.parsingPaths[2]][self.parsingPaths[1]][self.parsingPaths[0]][self.parsingPaths[3]]
          except:
            temp = []
          print(temp)
          Menu.table.verbs(PADDING*5, HEIGHT/2, temp, parse = True)
        else:
          Menu.table.verbs(PADDING*5, HEIGHT/2, parse = True)
      
      elif self.page == "type":
        pass
      
      elif self.page == "results":
        pass
        
    elif self.page == "setup":
      self.verbRects = Menu.selectors.verbs(PADDING*5, PADDING*5, self.selected)

def drawWin(state, mouse, verbpage):
  pygame.draw.rect(WIN, WHITE, pygame.Rect(0, 0, WIDTH, HEIGHT))
  if state == "menu":
    text = BIGFONT.render("Hampton Latin", 1, BLACK)
    WIN.blit(text, ((WIDTH - text.get_width())/2, PADDING*5))
    text = BIGFONT.render("Software Project", 1, BLACK)
    WIN.blit(text, ((WIDTH - text.get_width())/2, PADDING*8))
    
    for option in range(0, len(OPTIONSRECTS)):
      
      if OPTIONSRECTS[option].collidepoint(mouse):
        pygame.draw.rect(WIN, GREY, OPTIONSRECTS[option])
        
      pygame.draw.rect(WIN, BLACK, OPTIONSRECTS[option], 3)
      
      text = BIGFONT.render(OPTIONSSTRINGS[option], 1, BLACK)
      WIN.blit(text, ((WIDTH - text.get_width())/2, OPTIONSRECTS[option].centery - text.get_height()/2))

  if state == "verbs":
    verbpage.draw()
    
  pygame.display.flip()

def main():
  
  verbpage = Verbpage()
  
  state = "menu"

  #initiates the clock
  clock = pygame.time.Clock()

  #initiates game loop
  run = True
  while run:

    #ticks the clock
    clock.tick(FPS)

    #gets mouse position
    mouse = pygame.mouse.get_pos()

    #for everything that the user has inputted ...
    for event in pygame.event.get():

      #if the "x" button is pressed ...
      if event.type == pygame.QUIT:

        #ends game loop
        run = False

        #terminates pygame
        pygame.quit()

        #terminates system
        sys.exit()
        
      if event.type == pygame.MOUSEBUTTONDOWN:
        
        if state == "menu":
          for option in range(0, len(OPTIONSRECTS)):
      
            if OPTIONSRECTS[option].collidepoint(mouse):
              state = OPTIONSSTRINGS[option].lower()
              
        if state == "verbs":
          if verbpage.page == "setup" and verbpage.verbRects != None:
            for row in verbpage.verbRects:
              for rect in row:
                indxR = verbpage.verbRects.index(row)
                indxC = row.index(rect)
                if rect.collidepoint(mouse):
                  if [indxR, indxC] not in verbpage.selected:
                    verbpage.selected.append([indxR, indxC])
                    verbpage.selectedPaths[indxR].append(VERBOPTIONS[indxR][indxC])
                  else:
                    verbpage.selected.remove([indxR, indxC])
                    verbpage.selectedPaths[indxR].remove(VERBOPTIONS[indxR][indxC])
                    
                  verbpage.reviewRects = []
                  verbpage.reviewing = [[] for _ in range(4)]
                  verbpage.reviewingPaths = [[] for _ in range(4)]
                  
            verbpage.setItems(None, None)

            temp = []
            possiblePaths = product(*verbpage.selectedPaths)
            
            for combo in possiblePaths:
              if combo in VERBCOMBOS:
                combo = list(combo)
                if combo not in temp:
                  temp.append(combo)
            
            if temp != []:
              temp2 = []
              for path in temp:
                try:
                  temp2.extend(VERBS[path[2]][path[1]][path[0]][path[3]])
                except:
                  pass
              verbpage.setItems(temp2, temp)
              
          elif verbpage.page == "review" and verbpage.reviewRects != []:
            for row in verbpage.reviewRects:
              for rect in row:
                if rect.collidepoint(mouse):
                  indxR = verbpage.reviewRects.index(row)
                  indxC = row.index(rect)
                  print(indxR, indxC, verbpage.reviewing, VERBOPTIONS[indxR][indxC])
                  if [indxR, indxC] not in verbpage.reviewing:
                    if VERBOPTIONS[indxR][indxC] in verbpage.selectedPaths[indxR]:
                      verbpage.reviewing[indxR] = [indxR, indxC]
                      verbpage.reviewingPaths[indxR] = VERBOPTIONS[indxR][indxC]
                  else:
                    verbpage.reviewing[indxR] = []
                    verbpage.reviewingPaths[indxR] = []
                    
          elif verbpage.page == "parse":
            for row in verbpage.parseRects:
              for rect in row:
                if rect.collidepoint(mouse):
                  indxR = verbpage.parseRects.index(row)
                  indxC = row.index(rect)
                  print(indxR, indxC, verbpage.parsing, VERBOPTIONS[indxR][indxC], verbpage.parsingPaths[indxR])
                  if [indxR, indxC] not in verbpage.parsing:
                    if VERBOPTIONS[indxR][indxC] in verbpage.selectedPaths[indxR]:
                      verbpage.parsing[indxR] = [indxR, indxC]
                      verbpage.parsingPaths[indxR] = VERBOPTIONS[indxR][indxC]
                  else:
                    verbpage.parsing[indxR] = []
                    verbpage.parsingPaths[indxR] = []
            
          
      if event.type == pygame.KEYDOWN:
        
        if event.key == pygame.K_LEFT:
          if state == "verbs":
            new = verbpage.pages.index(verbpage.page) - 1
            if new == -1:
              verbpage.page = verbpage.pages[len(verbpage.pages) - 1]
            else:
              verbpage.page = verbpage.pages[new]
              
        if event.key == pygame.K_RIGHT:
          
          if state == "verbs":
            new = verbpage.pages.index(verbpage.page) + 1
            if new == len(verbpage.pages):
              verbpage.page = verbpage.pages[0]
            else:
              verbpage.page = verbpage.pages[new]
        
    drawWin(state, mouse, verbpage)

main()