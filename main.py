import pygame
import random
import math

# Constants
WIDTH, HEIGHT = 800, 800
ENTITY_SIZE = 50
QUANTITY = 30
DETECTION_RADIUS = 75

# Boolean to switch between game modes
SIMPLE_GAME = False

# Mapping entity types to image files for both game modes
IMAGE_FILES = {
    "rock": "icons/rock.png",
    "paper": "icons/paper.png",
    "scissors": "icons/scissors.png",
    "lizard": "icons/lizard.png",
    "spock": "icons/spock.jpg",
}

IMAGE_FILES_SIMPLE = {
    "rock": "icons/rock.png",
    "paper": "icons/paper.png",
    "scissors": "icons/scissors.png",
}

# Rules for the game
BEATS = {
    "rock": ["scissors", "lizard"],
    "paper": ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "lizard": ["paper", "spock"],
    "spock": ["scissors", "rock"],
}

BEATS_SIMPLE = {
    "rock": ["scissors"],
    "paper": ["rock"],
    "scissors": ["paper"],
}

class Entity:
    def __init__(self, entity_type, x, y, image):
        self.type = entity_type
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (ENTITY_SIZE, ENTITY_SIZE))
        self.speed = random.uniform(1, 3)
        self.direction = random.uniform(0, 2 * math.pi)
        self.size = ENTITY_SIZE

    def move(self):
        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction)

        # Bounce off the walls
        if self.x <= 0 or self.x >= WIDTH - self.size:
            self.direction = math.pi - self.direction
        if self.y <= 0 or self.y >= HEIGHT - self.size:
            self.direction = -self.direction

    def detect_collision(self, other):
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance < self.size + other.size

    def detect_entities(self, entities):
        for entity in entities:
            if entity != self:
                distance = math.hypot(self.x - entity.x, self.y - entity.y)
                if distance < DETECTION_RADIUS:
                    if SIMPLE_GAME:
                        beats = BEATS_SIMPLE
                    else:
                        beats = BEATS
                    if entity.type in beats[self.type]:
                        self.direction = math.atan2(self.y - entity.y, self.x - entity.x)
                    elif self.type in beats[entity.type]:
                        self.direction = math.atan2(entity.y - self.y, entity.x - self.x)

def main():
    global SIMPLE_GAME

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rock Paper Scissors (Lizard Spock)")

    # Load images
    if SIMPLE_GAME:
        images = {etype: pygame.image.load(IMAGE_FILES_SIMPLE[etype]) for etype in IMAGE_FILES_SIMPLE}
    else:
        images = {etype: pygame.image.load(IMAGE_FILES[etype]) for etype in IMAGE_FILES}

    entities = [Entity(random.choice(list(images.keys())), random.randint(0, WIDTH), random.randint(0, HEIGHT), images[random.choice(list(images.keys()))]) for _ in range(QUANTITY)]

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        for entity in entities:
            entity.move()
            entity.detect_entities(entities)

        entity_types = set(entity.type for entity in entities)
        if len(entity_types) == 1:
            running = False
            winner = entity_types.pop()
            print(f"The winner is: {winner}")

        for i in range(len(entities) - 1, -1, -1):
            for j in range(len(entities) - 1, -1, -1):
                if i != j and entities[i].detect_collision(entities[j]):
                    if SIMPLE_GAME:
                        beats = BEATS_SIMPLE
                    else:
                        beats = BEATS
                    if entities[j].type in beats[entities[i].type]:
                        entities[j].type = entities[i].type
                        entities[j].image = pygame.transform.scale(images[entities[i].type], (ENTITY_SIZE, ENTITY_SIZE))
                    elif entities[i].type in beats[entities[j].type]:
                        entities[i].type = entities[j].type
                        entities[i].image = pygame.transform.scale(images[entities[j].type], (ENTITY_SIZE, ENTITY_SIZE))

        for entity in entities:
            # Draw detection radius
            #pygame.draw.circle(screen, (0, 255, 0), (int(entity.x + entity.size // 2), int(entity.y + entity.size // 2)), DETECTION_RADIUS, 1)
            # Draw collision position
            #pygame.draw.circle(screen, (255, 0, 0), (int(entity.x + entity.size // 2), int(entity.y + entity.size // 2)), 5)
            # Draw entity image
            screen.blit(entity.image, (int(entity.x), int(entity.y)))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    # Change the value to True for simple game
    # SIMPLE_GAME = False
    main()
