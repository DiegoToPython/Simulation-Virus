import random
import pygame

# Initialisation de Pygame
pygame.init()

# Définition des dimensions de la fenêtre
WIDTH = 800
HEIGHT = 600

# Couleurs utilisées dans la simulation
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)


# Définition de la classe représentant un humain
class Human:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.dead = False
        self.immunity = random.randint(10, 100)
        self.color = GREEN
        self.infection_resistance = random.randint(1, 100)

    def update(self, virus):
        # Vérification de si l'humain est vivant ou mort
        if self.alive:
            self.color = GREEN

        # Vérification de si l'humain a été infecté par le virus
        if virus.infect(self):
            self.color = ORANGE

        # Vérification de si l'humain est mort de l'infection
        if self.alive and self.infection_resistance <= virus.mortality_rate:  # Condition pour vérifier si l'humain meurt de l'infection
            self.alive = False
            self.dead = True
            self.color = RED

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5)


# Définition de la classe représentant le virus
class Virus:
    def __init__(self):
        self.virulence = random.randint(1, 100)
        self.resistance = random.randint(1, 15)
        self.contagion_rate = random.randint(1, 100)
        self.mortality_rate = (self.virulence + self.resistance + self.contagion_rate) / 3

    def infect(self, human):
        # Vérification de si l'humain est déjà infecté ou mort
        if not human.alive or human.color == ORANGE or human.color == RED:
            return False

        # Calcul de la probabilité d'infection de l'humain
        if self.contagion_rate > human.infection_resistance:
            human.color = ORANGE
            return True
        else:
            human.color = GREEN
            return False

        if self.mortality_rate >= human.immunity :
            human.color = RED
            return False

    def draw_info(self, screen, font):
        text = font.render(
            f"Virulence: {self.virulence}, Resistance: {self.resistance}, Contagion Rate: {self.contagion_rate} Mortality Rate: {self.mortality_rate}", True,
            WHITE)
        screen.blit(text, (10, 10))


# Initialisation de la simulation
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virus Simulation")
font = pygame.font.SysFont("Arial", 20)
humans = [Human(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(800)]
virus = Virus()
generation = 1
highest_mortality_rate = 0

# Boucle principale de la simulation
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour des éléments de la simulation
    for human in humans:
        human.update(virus)
    virus.draw_info(screen, font)

    # Dessin des éléments de la simulation
    screen.fill(BLACK)
    for human in humans:
        human.draw(screen)
    virus.draw_info(screen, font)
    pygame.display.update()

infected_count = 0
dead_count = 0
alive_count = 0

for human in humans:
    if human.color == ORANGE:
        infected_count += 1
    elif human.color == RED:
        dead_count += 1
    else:
        alive_count += 1

with open("results.txt", "a") as file:
    file.write(f"Virus Simulation Results:\n\n")
    file.write(f"Virulence: {virus.virulence}\n")
    file.write(f"Resistance: {virus.resistance}\n")
    file.write(f"Contagion Rate: {virus.contagion_rate}\n")
    file.write(f"Mortality Rate: {virus.mortality_rate}\n\n")
    human_count = alive_count + infected_count + dead_count
    file.write(f"Number of Humans Not Infected: {human_count}\n")
    file.write(f"Number of Humans Not Infected: {alive_count}\n")
    file.write(f"Number of Humans Infected: {infected_count}\n")
    file.write(f"Number of Humans Dead: {dead_count}\n\n\n\n")
    file.write("\n")