import pygame
import speech_recognition as sr
import time
import random

pygame.init()

# Environment settings
cell_size = 80
cols, rows = 10, 10  # Grid size
screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
pygame.display.set_caption("Enhanced Virtual Robot Environment")

# Colors
WHITE = (255, 255, 255)

# Load and resize images
robot_image = pygame.image.load("robot.png")
robot_image = pygame.transform.scale(robot_image, (cell_size, cell_size))

# Room images
kitchen_image = pygame.image.load("kitchen.png")
kitchen_image = pygame.transform.scale(kitchen_image, (cell_size, cell_size))

bedroom_image = pygame.image.load("bedroom.png")
bedroom_image = pygame.transform.scale(bedroom_image, (cell_size, cell_size))

living_room_image = pygame.image.load("living_room.png")
living_room_image = pygame.transform.scale(living_room_image, (cell_size, cell_size))

bathroom_image = pygame.image.load("bathroom.png")
bathroom_image = pygame.transform.scale(bathroom_image, (cell_size, cell_size))

office_image = pygame.image.load("office.png")
office_image = pygame.transform.scale(office_image, (cell_size, cell_size))

garage_image = pygame.image.load("garage.png")
garage_image = pygame.transform.scale(garage_image, (cell_size, cell_size))

# Obstacle image
obstacle_image = pygame.image.load("wall.png")
obstacle_image = pygame.transform.scale(obstacle_image, (cell_size, cell_size))

# Room locations and walls for pathways
house_map = {
    "kitchen": (2, 2),
    "bedroom": (7, 1),
    "living room": (4, 5),
    "bathroom": (1, 8),
    "office": (8, 3),
    "garage": (0, 6),
}

# Define walls and pathways around destinations
obstacles = [
    # Kitchen walls
    (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (3, 2), (3, 3),
    # Bedroom walls
    (6, 1), (6, 2), (7, 2), (8, 1), (8, 2),
    # Living room walls
    (3, 5), (3, 6), (4, 6), (5, 5), (5, 6),
    # Bathroom walls
    (0, 8), (0, 9), (1, 9), (2, 8), (2, 9),
    # Office walls
    (7, 3), (7, 4), (8, 4), (9, 3), (9, 4),
    # Garage walls
    (0, 5), (1, 5), (1, 6), (1, 7), (0, 7),
]

# Initial robot position
robot_position = [1, 1]

# Define keywords for each destination
keywords = {
    "kitchen": ["hungry", "eat", "kitchen"],
    "bedroom": ["sleep", "tired", "bedroom"],
    "living room": ["relax", "watch tv", "living room"],
    "bathroom": ["bathroom", "washroom", "freshen up"],
    "office": ["office", "work", "study"],
    "garage": ["garage", "car", "park"]
}

def process_command(command):
    """Map spoken command to a destination."""
    for room, words in keywords.items():
        if any(word in command for word in words):
            return room
    return "unknown"

def find_path(target, position):
    """Move robot toward the target while following a pathway."""
    if position[0] < target[0] and (position[0] + 1, position[1]) not in obstacles:
        position[0] += 1
    elif position[0] > target[0] and (position[0] - 1, position[1]) not in obstacles:
        position[0] -= 1
    elif position[1] < target[1] and (position[0], position[1] + 1) not in obstacles:
        position[1] += 1
    elif position[1] > target[1] and (position[0], position[1] - 1) not in obstacles:
        position[1] -= 1
    else:
        # Adjust to avoid obstacle if directly in the way
        position[0] += random.choice([-1, 1])
    return position

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand that.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
    return ""

def navigate_to(destination):
    global robot_position
    target = house_map.get(destination)
    if not target:
        print(f"Destination '{destination}' not found!")
        return

    while robot_position != list(target):
        robot_position = find_path(target, robot_position)
        draw_environment()
        pygame.display.update()
        print(f"Moving to {destination}: Current position: {robot_position}")
        time.sleep(0.3)

    print(f"Robot has arrived at the {destination}.")

def draw_environment():
    screen.fill(WHITE)
    
    # Draw grid with room images
    for room_name, room_coords in house_map.items():
        x, y = room_coords[0] * cell_size, room_coords[1] * cell_size
        if room_name == "kitchen":
            screen.blit(kitchen_image, (x, y))
        elif room_name == "bedroom":
            screen.blit(bedroom_image, (x, y))
        elif room_name == "living room":
            screen.blit(living_room_image, (x, y))
        elif room_name == "bathroom":
            screen.blit(bathroom_image, (x, y))
        elif room_name == "office":
            screen.blit(office_image, (x, y))
        elif room_name == "garage":
            screen.blit(garage_image, (x, y))
    
    # Draw obstacles as walls
    for obstacle in obstacles:
        x, y = obstacle[0] * cell_size, obstacle[1] * cell_size
        screen.blit(obstacle_image, (x, y))

    # Draw robot
    robot_x, robot_y = robot_position[0] * cell_size, robot_position[1] * cell_size
    screen.blit(robot_image, (robot_x, robot_y))

if __name__ == "__main__":
    running = True
    draw_environment()
    pygame.display.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        command = recognize_speech()
        destination = process_command(command)
        if destination != "unknown":
            print(f"Destination identified: {destination}")
            navigate_to(destination)
        else:
            print("Sorry, I couldn't understand where you want to go.")
        
    pygame.quit()
