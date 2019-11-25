import pygame
import sys, time
from pygame.sprite import Group
from joueur import Joueur
from sol import Sol
from projectiles import Projectile, Slash
from plateforme import Plateforme
from enemie import Enemie


class Jeu:

	def __init__(self):

		self.ecran = pygame.display.set_mode((1100, 600))
		pygame.display.set_caption('Jeu De Combat')
		self.jeu_encours = True
		self.joueur_x, self.joueur_y = 600, 100
		self.taille = [32, 64]
		self.joueur_vitesse_x = 0
		self.joueur = Joueur(self.joueur_x, self.joueur_y, self.taille)
		self.enemie_x, self.enemie_y = 100, 400
		self.enemie_taille = [88, 60]
		self.image_enemie = pygame.image.load('knight.png')
		self.enemie = Enemie(self.enemie_x, self.enemie_y, self.enemie_taille)
		self.image_arriere_plan = pygame.image.load('PC Computer - RPG Maker VX Ace - Battle Background Overlays 33.png')
		self.arriere_plan_rect = [34, 34, 574, 214]
		self.image_ciel_bleu = self.image_arriere_plan.subsurface(self.arriere_plan_rect)
		self.image_ciel_bleu = pygame.transform.scale(self.image_ciel_bleu, (1100, 600))
		self.image_sol_plat = pygame.image.load('Game Boy Advance - Sonic Advance - Background Elements 1.gif')
		self.image_sol_rect = [542, 3693, 373, 117]
		self.image_sol = self.image_sol_plat.subsurface(self.image_sol_rect)
		self.image_sol = pygame.transform.scale(self.image_sol, (1100, 170))
		self.image_plat_rect = [535, 3689, 379, 123]
		self.image_plat = self.image_sol_plat.subsurface(self.image_plat_rect)
		self.image_plat = pygame.transform.scale(self.image_plat, (300, 50))
		self.sol = Sol(self.image_sol)
		self.gravite = (0, 10)
		self.resistance = (0, 0)
		self.rect = pygame.Rect(0, 0, 1100, 600)
		self.collision_sol = False
		self.horloge = pygame.time.Clock()
		self.fps = 30
		self.projectile_groupe = Group()
		self.t1, self.t2 = 0, 0
		self.delta_temps = 0
		self.image_joueur = pygame.image.load('WonderSwan WSC - RockmanEXE WS - MegaManEXE Heat Style.png')
		self.image_joueur_rect = pygame.Rect(124, 453, 8, 8)
		self.image_boule_de_feu = self.image_joueur.subsurface(self.image_joueur_rect)
		self.plateforme_groupe = Group()
		self.plateforme_liste_rect = [
			pygame.Rect(0, 300, 300, 50), pygame.Rect(800, 300, 300, 50),
			pygame.Rect(400, 150, 300, 50)
		]
		self.slash_groupe = Group()
		self.slash_image_rect = pygame.Rect(108, 232, 24, 43)
		self.image_slash = self.image_enemie.subsurface(self.slash_image_rect)
		self.image_slash = pygame.transform.scale(self.image_slash, (30, 30))
		self.image_vie_joueur = pygame.image.load('life.png')
		self.image_vie_rect = pygame.Rect(38, 9, 55, 13)
		self.image_vie_joueur = self.image_vie_joueur.subsurface(self.image_vie_rect)
		self.image_barre_de_vie = pygame.transform.scale(self.image_vie_joueur, (285, 40))
		self.rect_tete = pygame.Rect(82, 0, 12, 10)
		self.image_tete = self.image_joueur.subsurface(self.rect_tete)
		self.image_tete = pygame.transform.scale(self.image_tete, (50, 50))
		self.debut_timer = 90000
		self.bouton = pygame.image.load('button.png')
		self.replay_bouton = pygame.image.load('replay.png')
		self.bouton_rect = pygame.Rect(542, 501, 84, 82)
		self.image_bouton = self.bouton.subsurface(self.bouton_rect)
		self.image_bouton = pygame.transform.scale(self.image_bouton, (50, 50))
		self.x_souris, self.y_souris = 0, 0
		self.etat_1 = False
		self.but_du_jeu = False


	def boucle_principale(self):
		"""
		Boucle principale du jeu

		"""
		dictionnaire_vide_joueur = {}
		dictionnaire_images_joueur = self.joueur.convertir_rect_surface(self.image_joueur, dictionnaire_vide_joueur)
		dictionnaire_vide_enemie = {}
		dictionnaire_images_enemie = self.enemie.image_liste(self.image_enemie, dictionnaire_vide_enemie)

		while self.jeu_encours:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
					self.x_souris, self.y_souris = pygame.mouse.get_pos()
					print(self.x_souris, self.y_souris)

					if (self.x_souris < 575 and self.x_souris > 525 and self.y_souris < 70 and self.y_souris > 20):
						self.etat_1 = True

					if (self.x_souris < 59 and self.x_souris > 29 and self.y_souris < 480 and self.y_souris > 450) and self.etat_1:
						self.but_du_jeu = True

					if (self.x_souris < 901 and self.x_souris > 851 and self.y_souris < 572 and self.y_souris > 533) and self.etat_1:
						self.recommencer()
						self.etat_1 = False

					if (self.x_souris < 884 and self.x_souris > 855 and self.y_souris < 477 and self.y_souris > 437) and self.etat_1:
						self.etat_1 = False



				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RIGHT:
						self.joueur_vitesse_x = 10
						self.joueur.direction = 1
						self.joueur.etat = 'bouger'

					if event.key == pygame.K_LEFT:
						self.joueur_vitesse_x = -10
						self.joueur.direction = -1
						self.joueur.etat = 'bouger'


					if event.key == pygame.K_UP:
						self.joueur.a_sauter = True
						self.joueur.nombre_de_saut += 1

					if event.key == pygame.K_p:
						self.t1 = time.time()
						self.joueur.etat = 'attaque'

					if event.key == pygame.K_e:
						self.enemie.a_attaque = True
						self.enemie.etat = 'attaque'

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_RIGHT:
						self.joueur_vitesse_x = 0
						self.joueur.etat = 'debout'

					if event.key == pygame.K_LEFT:

						self.joueur_vitesse_x = 0
						self.joueur.etat = 'debout'


					if event.key == pygame.K_p:
						self.t2 = time.time()
						self.joueur.a_tire = True
						self.joueur.etat = 'debout'

					if event.key == pygame.K_e:
						self.enemie.etat = 'vivant'



			if self.sol.rect.colliderect(self.joueur.rect):
				self.resistance = (0, -10)
				self.collision_sol = True
				self.joueur.nombre_de_saut = 0

			else:
				self.resistance = (0, 0)

			if self.joueur.a_sauter and self.collision_sol:
				if self.joueur.nombre_de_saut < 2:
					self.joueur.sauter()

			if self.joueur.a_tire:
				if len(self.projectile_groupe) < self.joueur.tir_autorise and self.delta_temps > 0.05:
					projectile = Projectile(self.joueur.rect.x + 20, self.joueur.rect.y + 10, [10, 10], self.joueur.direction,
					                            self.image_boule_de_feu)
					self.projectile_groupe.add(projectile)
					self.joueur.a_tire = False

			if self.enemie.a_attaque:

				if len(self.slash_groupe) < self.enemie.tir_autorise:
					slash = Slash(self.enemie.rect.x + 20, self.enemie.rect.y - 5, [30, 30], self.image_slash)
					self.slash_groupe.add(slash)
					self.enemie.a_attaque = False

			secondes = (self.debut_timer - pygame.time.get_ticks()) // 1000

			if secondes == 0:
				break

			for projectile in self.projectile_groupe:
				projectile.mouvement(50)
				if projectile.rect.right >= self.rect.right or projectile.rect.left <= self.rect.left:
					self.projectile_groupe.remove(projectile)

				if self.enemie.rect.colliderect(projectile.rect):
					self.projectile_groupe.remove(projectile)
					self.enemie.degats_recus = 10
					if self.delta_temps > 2:
						self.enemie.degats_recus = 30
					self.enemie.vie -= self.enemie.degats_recus
					self.enemie.degats_recus = 0


			for slash in self.slash_groupe:
				slash.mouvement(50)
				if slash.rect.right >= self.rect.right or slash.rect.left <= self.rect.left:
					self.slash_groupe.remove(slash)

				if self.joueur.rect.colliderect(slash.rect):
					self.slash_groupe.remove(slash)
					self.joueur.rect.x += 3
					self.joueur.degats_recus = 10
					self.joueur.vie -= self.joueur.degats_recus
					self.joueur.degats_recus = 0

			if self.joueur.vie <= 0:
				self.joueur.etat = 'mort'
			if self.enemie.vie <= 0:
				self.enemie.etat = 'mort'

			for rectangle in self.plateforme_liste_rect:
				plateforme = Plateforme(rectangle, self.image_plat)
				self.plateforme_groupe.add(plateforme)
				if self.joueur.rect.midbottom[1] // 10 * 10 == plateforme.rect.top \
						and self.joueur.rect.colliderect(rectangle):
					self.resistance = (0, -10)
					self.joueur.nombre_de_saut = 0

			self.delta_temps = self.t2 - self.t1
			self.joueur.mouvement(self.joueur_vitesse_x)
			self.gravite_jeu()
			self.joueur.rect.clamp_ip(self.rect)
			self.ecran.fill((255, 255, 255))
			self.ecran.blit(self.image_ciel_bleu, self.rect)
			self.sol.afficher(self.ecran)
			self.ecran.blit(self.image_barre_de_vie, (26, 500, 285, 40))
			self.ecran.blit(self.image_tete, (10, 490, 50, 50))
			self.joueur.afficher(self.ecran, dictionnaire_images_joueur)
			self.enemie.afficher(self.ecran, dictionnaire_images_enemie)
			self.ecran.blit(self.image_bouton, (525, 20, 50, 50))
			self.creer_message('grande','{}'.format(secondes), [535, 70, 20, 20], (255, 255, 255))
			for plateforme in self.plateforme_groupe:
				plateforme.afficher(self.ecran)

			for slash in self.slash_groupe:
				slash.afficher(self.ecran)
			for projectile in self.projectile_groupe:
				projectile.afficher(self.ecran, self.delta_temps)

			if self.etat_1:
				pygame.draw.rect(self.ecran, (255, 255, 255), (0, 500, 1100, 100), 2)
				pygame.draw.rect(self.ecran, (0, 0, 0), (0, 400, 1100, 200))
				self.ecran_menu()
				if self.but_du_jeu:
					self.creer_message('petite', f" Le dernier en vie Gagne !!!  ", (100, 450, 80, 80), (255, 255, 255))


			pygame.draw.rect(self.ecran, (255, 0, 0), self.rect, 1)
			self.horloge.tick(self.fps)
			pygame.display.flip()

	def gravite_jeu(self):
		"""
		Gére la gravité pour chaque élément
		"""

		self.joueur.rect.y += self.gravite[1] + self.resistance[1]

	def creer_message(self, font, message, message_rectangle, couleur):

		if font == 'petite':
			font = pygame.font.SysFont('lato', 20, False)

		elif font == 'moyenne':
			font = pygame.font.SysFont('lato', 30, False)

		elif font == 'grande':
			font = pygame.font.SysFont('lato', 40, True)

		message = font.render(message, True, couleur)

		self.ecran.blit(message, message_rectangle)

	def ecran_menu(self):
		"""
		Afficher les boutons
		"""
		image_rect = pygame.Rect(11, 7, 69, 67)
		image_restart = self.replay_bouton.subsurface(image_rect)
		image_restart = pygame.transform.scale(image_restart, (50, 50))
		image_continuer_rect = pygame.Rect(546, 274, 96, 92)
		image_continuer = self.bouton.subsurface(image_continuer_rect)
		image_continuer = pygame.transform.scale(image_continuer, (50, 50))
		imgae_info_rect = pygame.Rect(924, 432, 58, 60)
		image_info = self.bouton.subsurface(imgae_info_rect)
		image_info = pygame.transform.scale(image_info, (50, 50))

		self.ecran.blit(image_restart, (850, 530, 50, 50))
		self.ecran.blit(image_continuer, (850, 430, 50, 50))
		self.ecran.blit(image_info, (20, 440, 50, 50))

	def recommencer(self):

		self.joueur.vie = 100
		self.enemie.vie = 100
		self.joueur.rect.x = 400
		self.joueur.rect.y = 100
		self.joueur.etat = 'debout'
		self.enemie.etat = 'vivant'


if __name__ == '__main__':
	pygame.init()
	Jeu().boucle_principale()
	pygame.quit()
