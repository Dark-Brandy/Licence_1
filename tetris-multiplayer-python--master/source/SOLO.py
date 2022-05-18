from GRILLE import *
from SOLO import *
from MULTJOUEUR import *
from Pieces import *
from pygame.locals import *
import pygame
import sys

import pygame.mixer
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.music.load("Tetris.mp3")
pygame.mixer.music.play(-1)
BLACK = 0, 0, 0
WHITE = 255, 255, 255
CIEL = 0, 200, 255
RED = 255, 0, 0
ORANGE = 255, 100, 0
GREEN = 0, 255, 0


class Button:
    '''Ajout d'un bouton avec un texte sur img
    Astuce: ajouter des espaces dans les textes pour avoir une même largeur
    de boutons
    dx, dy décalage du bouton par rapport au centre
    action si click
    Texte noir
    '''

    def __init__(self, fond, text, color, font, dx, dy):
        self.fond = fond
        self.text = text
        self.color = color
        self.font = font
        self.position = dx, dy
        self.action = False  # enable or not
        self.titre = self.font.render(self.text, True, BLACK)
        textpos = self.titre.get_rect()
        textpos.centerx = self.fond.get_rect().centerx + self.position[0]
        textpos.centery = self.position[1]
        self.textpos = [textpos[0], textpos[1], textpos[2], textpos[3]]
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos)
        self.fond.blit(self.titre, self.textpos)

    def update_button(self, fond, action=None):
        self.fond = fond
        mouse_xy = pygame.mouse.get_pos()
        over = self.rect.collidepoint(mouse_xy)
        if over:
            action()
            if self.color == RED:
                self.color = GREEN
                self.action = True
            elif self.color == GREEN:
                # sauf les + et -, pour que ce soit toujours vert
                if len(self.text) > 5:  # 5 char avec les espaces
                    self.color = RED
                self.action = False
        # à la bonne couleur
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos)
        self.fond.blit(self.titre, self.textpos)

    def dessiner_boutton(self, fond):
        self.fond = fond
        self.rect = pygame.draw.rect(self.fond, self.color, self.textpos)
        self.fond.blit(self.titre, self.textpos)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1400, 1000))
        self.m_gameOver = Solo()
        self.loop = True

        # Définition de la police
        self.big = pygame.font.SysFont('baby_blocks.ttf', 150)
        self.small = pygame.font.SysFont('freesans', 36)
        self.normal = pygame.font.SysFont('upheavtt.ttf', 100)

        self.creer_fond()
        self.creer_boutton()
        pygame.display.update()
    def update_textes(self):
        self.textes = [["TETRIS", VERT, self.big, 0, 90]]

    def creer_fond(self):
        # Image de la taille de la fenêtre
        self.fond = pygame.Surface(self.screen.get_size())
        # En bleu
        self.fond.fill(CIEL)

    def creer_boutton(self):
        self.MULTIJOUEUR_button = Button(self.fond, "   MULTIJOUEUR   ", RED, self.normal, 0, 380)
        self.SOLO_button = Button(self.fond, "   SOLO   ", RED, self.normal, 0, 530)
        self.quit_button = Button(self.fond, "   QUITTER   ", RED, self.normal, 0, 680)

    def son(self):
        pygame.init()
        pygame.mixer.music.load("son_turner_teen.oga")        
        pygame.mixer.music.play(-1)
    def display_text(self, text, color, font, dx, dy):
        '''Ajout d'un texte sur fond. Décalage dx, dy par rapport au centre.
        '''
        mytext = font.render(text, True, color)  # True pour antialiasing
        textpos = mytext.get_rect()
        textpos.centerx = self.fond.get_rect().centerx + dx
        textpos.centery = dy
        self.fond.blit(mytext, textpos)

    def lancement_menu(self):
        while self.loop:
            self.creer_fond()
   
            # Boutons
            self.MULTIJOUEUR_button.dessiner_boutton(self.fond)
            self.SOLO_button.dessiner_boutton(self.fond)
            self.quit_button.dessiner_boutton(self.fond)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.MULTIJOUEUR_button.update_button(self.fond, action=MULTIJOUEUR)
                    self.SOLO_button.update_button(self.fond, action=SOLO)
                    self.quit_button.update_button(self.fond, action=gamequit)

            self.update_textes()
            for text in self.textes:
                self.display_text(text[0], text[1], text[2],
                                  text[3], text[4])

            # Ajout du fond dans la fenêtre
            self.screen.blit(self.fond, (0, 0))
            # Actualisation de l'affichage
            # self.fin_de_partie()
            pygame.display.update()
            # 10 fps


def MULTIJOUEUR():
    print("MULTIJOUEUR")
    v=Multijoueur()
    v.Lancement()

def SOLO():
    print("SOLO")
    c = Solo()
    c.Lancement()


def gamequit():
    print("Quit")
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    game = Game()
    game.lancement_menu()

class Solo(object):
    def __init__(self):
        self.m_GRILLE = GRILLE() # On fait appel ici à la classe GRILLE() créee auparavant qu'on affecte à la variable m_GRILLE()
        self.m_PieceCourante = None    # Initialisation de la variable m_PieceCourante à laquelle définie aucune valeur
        self.m_SuivantePiece = Piece()  # On fait appel ici à la classe Piece() créee auparavant qu'on affecte à la variable m_SuivantePiece()
        self.m_piecechutes = False      # Définition de la variable m_piecechutes contenant des valeurs fausses (false ou 0)
        self.m_gameOver = False         # Définition de la variable m_gameOver contenant des valeurs fausses (false ou 0)
        self.m_direction = {'left' : False, 'right' : False, 'down' : False} # Création d'un dictionnaire m_direction contenant des
        # clés avec des valeurs fausses
        self.m_rotate = False # Définition de la variable m_rotate contenant des valeurs fausses (false ou 0)
        self.m_DernierrechuteTime = time.time() # Définition de la variable m_DernierchuteTime contenant la fonction time du module time
        # qui nous permettra de récupérer le temps actuel écoulé (en seconde) lors de la chute d'une pièce
        self.m_DernierTempsMOuv = time.time()   # Définition de la variable m_DernierTempsMouv contenant la fonction time du module time
        # qui nous permettra de récupérer le temps actuel écoulé (en seconde) lors du mouvement de la d'une pièce
        self.plateau=pygame.Surface((300,553))
        self.m_score = 0    # Initialisation de la variable m_score à 0
        self.image=pygame.image.load("index.jpg").convert()
        self.m_niveau = 1
        pygame.init()   # initialiser tous les modules pygame importés
        self.boite = pygame.display.set_mode((GRILLE_LARGEUR * 6, GRILLE_LONGUEUR*3)) # Initialisation de l'écran pour l'affichage
        # Cette fonction créera une surface d'affichage. Les arguments transmis sont des demandes pour un type d'affichage.
        # L’affichage créé sera la meilleure correspondance possible prise en charge par le système.
        pygame.display.set_caption('Turner Teen') # Obtenir la légende de la fenêtre en cours
       

    def logic(self):


        if time.time() - self.m_DernierTempsMOuv > 0.1:
            if self.m_direction['left'] == True:
            #
            #si la touche gauche est appuyée physiquement la directionde la piece va dans
            #la direction gauche de a grille d'ou l'utilisation du signe (-) négatif
            #qui indique le sens contraire en considerant que sin on part de la gauche vers la droite
            #on part dans le sens positif sinon dans le sens négatif
            #
                self.m_PieceCourante.bouger(-TAILLE_BOITE, 0, self.m_GRILLE)

            elif self.m_direction['right'] == True:

                self.m_PieceCourante.bouger(TAILLE_BOITE, 0, self.m_GRILLE)

            elif self.m_direction['down'] == True:
            #
            #si la touche directiont haut est appuyée physiquement la piece suivante va dans le sens positif (+) de la grille
            #c'est a dire de la gauche vers la droite
            #
                self.m_PieceCourante.bouger(0, TAILLE_BOITE, self.m_GRILLE)

            self.m_DernierTempsMOuv = time.time()

        elif self.m_rotate:
            self.m_PieceCourante.rotation(self.m_GRILLE)
            self.m_rotate = False

    def dessinerLignes(self):
        for i in range(LIGNES + 1): # Boucle dans la on parcours toutes nos lignes initialisées hors des fonctions
            pygame.draw.line(self.boite, NOIR, (i * TAILLE_BOITE, 0), (i * TAILLE_BOITE, GRILLE_LONGUEUR))
        for j in range(COLONNES):    # Boucle dans la on parcours toutes nos colonnes initialisées hors des fonctions
            pygame.draw.line(self.boite, NOIR, (0 , j * TAILLE_BOITE), (GRILLE_LARGEUR, j * TAILLE_BOITE))


    def texte(self, text, font):
        texteSurface = font.render(text, True, ROSE) # On affecte à la variable texteSurface la fonction pygame font.render avec laquelle on pourra
        # créer un nouvel objet à partir d'un fichier.
        return texteSurface, texteSurface.get_rect()    # On retourne ici la variable texteSurface et, on retourne aussi cette variable associée avec
        # la fonction pygame get_rect() qui retourne un nouveau rectangle couvrant toute la surface.
    def texteGO(self, text, font):
        texteSurface = font.render(text, True, BLANC) # On affecte à la variable texteSurface la fonction pygame font.render avec laquelle on pourra
        # créer un nouvel objet à partir d'un fichier.
        return texteSurface, texteSurface.get_rect() 

    def afficheScore(self):
        font = pygame.font.Font('upheavtt.ttf', 40) # On affecte à la variable font la fonction pygame font.Font qui crée un nouvel objet Font
        # à partir d'un fichier. Ce fichier Font se constitue du nom de la police ainsi que de sa taille
        textSurf, textRect = self.texte('SCORE : ' + str(self.m_score), font)
        textRect.center = (GRILLE_LARGEUR + 0.5 * GRILLE_LARGEUR , GRILLE_LONGUEUR / 1.5)

        textSurf3, textRect3 = self.texte('NIVEAU : ' + str(self.m_niveau), font)
        textRect3.center = (GRILLE_LARGEUR + 0.5 * GRILLE_LARGEUR , GRILLE_LONGUEUR - 85 )

        textSurf2, textRect2 = self.texte('Piece suivante :', font)
        textRect2.center = (GRILLE_LARGEUR + 0.5 * GRILLE_LARGEUR, GRILLE_LONGUEUR / 6)
        textSurf10, textRect10 = self.texte('LIGNE EFFACÉE(S) :'+str(int(self.m_score/25)), font)
        textRect10.center = (GRILLE_LARGEUR + 0.5 * GRILLE_LARGEUR, GRILLE_LONGUEUR / 2)
        self.boite.blit(textSurf, textRect)
        self.boite.blit(textSurf2, textRect2)
        self.boite.blit(textSurf3, textRect3)
        self.boite.blit(textSurf10, textRect10)

 

    def dessinelements(self):
#Fonction dessin de la grille de la piece suivante de la grille et de l'interface graphique
        self.plateau.fill((col))
        
        self.boite.fill(BLANC)
#Couleur de fond de la GRILLE en noir

#dessin des lignes  et des colone de la grille
        self.m_GRILLE.dessinergrille(self.plateau)
        self.m_PieceCourante.dessinerpiece(self.plateau)
        self.m_SuivantePiece.dessinerpiece(self.boite)
        self.afficheScore()
        self.boite.blit(self.plateau,(800,20))
        pygame.draw.line(self.boite,ROSE,((804-20),12),(1135-20,12),15)
        pygame.draw.line(self.boite,ROSE,(804-20,580),(1135-20,580),15)
        pygame.draw.line(self.boite,ROSE,(811-20,12),(811-20,580),15)
        pygame.draw.line(self.boite,ROSE,(1128-20,12),(1128-20,580),15)
#raffarichissement du score
        pygame.display.update()
#raffarichissement du score
        pygame.display.update()
#dessin de la grille piece suivante grille et score
#appel de la fonction MiseaJour qui permet de raffraichir la GRILLE a chaque fois
    def entreeDonnees(self):
        for event in pygame.event.get():
#definition de l'evenenment defaite si la grille est remplie la ligne suivante ferme directement le programme
#ainsi game_over =true
            if event.type == pygame.QUIT:
                self.m_gameOver = True
#definition des evenement liés aux Solos du jeu
            #
            #lorsque l'utilisateur appuie sur le touche du bas il est possible pur lui de deplacer la piece avec les touches directionnelles
            #gauche droite bas et espace qui utilise la rotation du coup on assigena ces  vraiables la valeur True
            #
            if event.type == pygame.KEYDOWN:
#Detecte si la touche direction du bas est appuyée physiquement
                if event.key == pygame.K_LEFT:
                    self.m_direction['left'] = True
                elif event.key == pygame.K_RIGHT:
                    self.m_direction['right'] = True
                elif event.key == pygame.K_DOWN:
                    self.m_direction['down'] = True
                elif event.key == pygame.K_RCTRL:
                    self.m_rotate = True
                elif event.key == pygame.K_ESCAPE:
                    self.m_gameOver = True
             #
            #la touche direction du haut n'a aucun role ici
            #
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.m_direction['left'] = False
                elif event.key == pygame.K_RIGHT:
                    self.m_direction['right'] = False
                elif event.key == pygame.K_DOWN:
                    self.m_direction['down'] = False

    def MiseaJour(self):
#le module time.time() permet de mesurer la durée entre deux evenement
#il represente aussi le "EPOCH" explication dans le rapport...
        if time.time() - self.m_DernierrechuteTime > 1:
#on verifie si le nombre de secondes ecoulées
#jusqu'a la chute dela derniere piece est superieure a 1
#
            if self.m_piecechutes:
                if self.m_PieceCourante.bouger(0, TAILLE_BOITE, self.m_GRILLE): # A revoir pygame doc !!!!!!!!!!!!!!!!
                    pass
#
#On teste si la piece est en pleine chute si oui on passe


                else:
                    self.m_piecechutes = False
                    self.m_GRILLE.AjoutELEMENT(self.m_PieceCourante) # On ajoute la pièce à la grille tant qu'elle n'est pas en mouvement
                    self.m_score += (self.m_GRILLE.effaceLigneComplete())*25  # On ajoute 10 au score à chaque fois qu'une ligne est effacée.

                self.m_DernierrechuteTime = time.time()

        if not self.m_piecechutes:
            self.m_PieceCourante = self.m_SuivantePiece # Si il n'y a aucune pièce en chute, on affiche dans la grille la prochaine pièce
            self.m_SuivantePiece = Piece()
            self.m_PieceCourante.setPos(int(GRILLE_LARGEUR / 2) - 50, 0) # Centre la pièce dans la grille par rapport à sa largeur
            self.m_piecechutes = True
            if not self.m_PieceCourante.descenteValide(0, 0, self.m_GRILLE):
                self.m_gameOver = True


    def gameOver(self):

        while self.m_gameOver:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.m_gameOver = True
                    game = Game()
                    game.lancement_menu()
            
            self.boite.fill((NOIR))
        
            self.boite.blit(self.image,(450,210))
            font = pygame.font.Font('upheavtt.ttf', 40) # On affecte à la variable font la fonction pygame font.Font qui crée un nouvel objet Font
        # à partir d'un fichier. Ce fichier Font se constitue du nom de la police ainsi que de sa taille
            textSurf, textRect = self.texteGO('SCORE : ' + str(self.m_score), font)
            textRect.center = (GRILLE_LARGEUR + 1.90 * GRILLE_LARGEUR , 820)

            textSurf3, textRect3 = self.texteGO('NIVEAU : ' + str(self.m_niveau), font)
            textRect3.center = (GRILLE_LARGEUR + 1.90* GRILLE_LARGEUR ,  880)

            
            textSurf10, textRect10 = self.texteGO('LIGNE(S) EFFACÉE(S) : '+str(int(self.m_score/25)), font)
            textRect10.center = (GRILLE_LARGEUR + 1.90 * GRILLE_LARGEUR, 945)
            self.boite.blit(textSurf, textRect)
           
            self.boite.blit(textSurf3, textRect3)
            self.boite.blit(textSurf10, textRect10)
            pygame.display.update()   


    def niveau(self):                    # Niveau de jeu
        """
        NIVEAU
        """

        if self.m_score >= 75:

            self.m_niveau = 2
            
            pygame.display.update()
        if self.m_niveau == 2 and self.m_score >= 175:
            PIECES['OB']=OB3_FORME
            self.m_niveau = 3
            pygame.display.update()
        if self.m_niveau == 3 and self.m_score >= 260:
            PIECES['LLC']=L_C
            self.m_niveau = 4
            pygame.display.update()

        if self.m_niveau == 4 and self.m_score >= 390:
            PIECES['G']=G_C
            self.m_niveau = "BOSS"
            pygame.display.update()

    def changement(self):
        if self.m_niveau==2 and time.time() - self.m_DernierrechuteTime > 0.5 :
            if self.m_piecechutes:
                if self.m_PieceCourante.bouger(0, TAILLE_BOITE, self.m_GRILLE): # A revoir pygame doc !!!!!!!!!!!!!!!!
                    pass
#
#On teste si la piece est en pleine chute si oui on passe


                else:
                    self.m_piecechutes = False
                    self.m_GRILLE.AjoutELEMENT(self.m_PieceCourante) # On ajoute la pièce à la grille tant qu'elle n'est pas en mouvement
                    self.m_score += (self.m_GRILLE.effaceLigneComplete())*25  # On ajoute 10 au score à chaque fois qu'une ligne est effacée.

                self.m_DernierrechuteTime = time.time()

        if not self.m_piecechutes:
            self.m_PieceCourante = self.m_SuivantePiece # Si il n'y a aucune pièce en chute, on affiche dans la grille la prochaine pièce
            self.m_SuivantePiece = Piece()
            self.m_PieceCourante.setPos(int(GRILLE_LARGEUR / 2) - 50, 0) # Centre la pièce dans la grille par rapport à sa largeur
            self.m_piecechutes = True
            if not self.m_PieceCourante.descenteValide(0, 0, self.m_GRILLE):
                self.m_gameOver = True

        if self.m_niveau==3 and time.time() - self.m_DernierrechuteTime > 0.4 :
            if self.m_piecechutes:
                if self.m_PieceCourante.bouger(0, TAILLE_BOITE, self.m_GRILLE): # A revoir pygame doc !!!!!!!!!!!!!!!!
                    pass
#
#On teste si la piece est en pleine chute si oui on passe


                else:
                    self.m_piecechutes = False
                    self.m_GRILLE.AjoutELEMENT(self.m_PieceCourante) # On ajoute la pièce à la grille tant qu'elle n'est pas en mouvement
                    self.m_score += (self.m_GRILLE.effaceLigneComplete())*25  # On ajoute 10 au score à chaque fois qu'une ligne est effacée.

                self.m_DernierrechuteTime = time.time()

        if not self.m_piecechutes:
            self.m_PieceCourante = self.m_SuivantePiece # Si il n'y a aucune pièce en chute, on affiche dans la grille la prochaine pièce
            self.m_SuivantePiece = Piece()
            self.m_PieceCourante.setPos(int(GRILLE_LARGEUR / 2) - 50, 0) # Centre la pièce dans la grille par rapport à sa largeur
            self.m_piecechutes = True
            if not self.m_PieceCourante.descenteValide(0, 0, self.m_GRILLE):
                self.m_gameOver = True
    

        if self.m_niveau==4 and time.time() - self.m_DernierrechuteTime > 0.2 :
            if self.m_piecechutes:
                if self.m_PieceCourante.bouger(0, TAILLE_BOITE, self.m_GRILLE): # A revoir pygame doc !!!!!!!!!!!!!!!!
                    pass
#
#On teste si la piece est en pleine chute si oui on passe


                else:
                    self.m_piecechutes = False
                    self.m_GRILLE.AjoutELEMENT(self.m_PieceCourante) # On ajoute la pièce à la grille tant qu'elle n'est pas en mouvement
                    self.m_score += (self.m_GRILLE.effaceLigneComplete())*25  # On ajoute 10 au score à chaque fois qu'une ligne est effacée.

                self.m_DernierrechuteTime = time.time()

        if not self.m_piecechutes:
            self.m_PieceCourante = self.m_SuivantePiece # Si il n'y a aucune pièce en chute, on affiche dans la grille la prochaine pièce
            self.m_SuivantePiece = Piece()
            self.m_PieceCourante.setPos(int(GRILLE_LARGEUR / 2) - 50, 0) # Centre la pièce dans la grille par rapport à sa largeur
            self.m_piecechutes = True
            if not self.m_PieceCourante.descenteValide(0, 0, self.m_GRILLE):
                self.m_gameOver = True

        if self.m_niveau=="BOSS" and time.time() - self.m_DernierrechuteTime > 0.2 :
            if self.m_piecechutes:
                if self.m_PieceCourante.bouger(0, TAILLE_BOITE, self.m_GRILLE): # A revoir pygame doc !!!!!!!!!!!!!!!!
                    pass
#
#On teste si la piece est en pleine chute si oui on passe


                else:
                    self.m_piecechutes = False
                    self.m_GRILLE.AjoutELEMENT(self.m_PieceCourante) # On ajoute la pièce à la grille tant qu'elle n'est pas en mouvement
                    self.m_score += (self.m_GRILLE.effaceLigneComplete())*25  # On ajoute 10 au score à chaque fois qu'une ligne est effacée.

                self.m_DernierrechuteTime = time.time()

        if not self.m_piecechutes:
            self.m_PieceCourante = self.m_SuivantePiece # Si il n'y a aucune pièce en chute, on affiche dans la grille la prochaine pièce
            self.m_SuivantePiece = Piece()
            self.m_PieceCourante.setPos(int(GRILLE_LARGEUR / 2) - 50, 0) # Centre la pièce dans la grille par rapport à sa largeur
            self.m_piecechutes = True
            if not self.m_PieceCourante.descenteValide(0, 0, self.m_GRILLE):
                self.m_gameOver = True

    def Lancement(self):
        while not self.m_gameOver:
            self.MiseaJour()
            self.entreeDonnees()
            self.logic()
            self.dessinelements()
            self.niveau()
            self.changement()
            self.gameOver()

