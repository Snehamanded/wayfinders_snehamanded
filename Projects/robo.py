import pygame
import speech_recognition as sr
import time

# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Interactive Robot")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Robot settings
robot_size = 50
robot_pos = [400, 400]  # Starting position
velocity = 20

# Obstacles
obstacles = [
    pygame.Rect(200, 200, 100, 100),
    pygame.Rect(500, 500, 100, 100),
    pygame.Rect(300, 600, 100, 100)
]

# Recognize command to move the robot
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

# Move the robot based on commands
def move_robot(command):
    if "up" in command:
        robot_pos[1] -= velocity
    elif "down" in command:
        robot_pos[1] += velocity
    elif "left" in command:
        robot_pos[0] -= velocity
    elif "right" in command:
        robot_pos[0] += velocity

    # Obstacle avoidance
    for obstacle in obstacles:
        if pygame.Rect(robot_pos[0], robot_pos[1], robot_size, robot_size).colliderect(obstacle):
            print("Obstacle encountered! Moving back.")
            if "up" in command:
                robot_pos[1] += velocity
            elif "down" in command:
                robot_pos[1] -= velocity
            elif "left" in command:
                robot_pos[0] += velocity
            elif "right" in command:
                robot_pos[0] -= velocity

# Draw the robot and environment
def draw_environment():
    screen.fill(WHITE)
    
    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)
    
    # Draw the robot with a more "robotic" look
    robot_rect = pygame.Rect(robot_pos[0], robot_pos[1], robot_size, robot_size)
    pygame.draw.rect(screen, GREEN, robot_rect)
    
    # Add "eyes" and an "antenna" for the robot
    pygame.draw.circle(screen, BLACK, (robot_pos[0] + 15, robot_pos[1] + 15), 5)  # Left eye
    pygame.draw.circle(screen, BLACK, (robot_pos[0] + 35, robot_pos[1] + 15), 5)  # Right eye
    pygame.draw.line(screen, BLACK, (robot_pos[0] + 25, robot_pos[1]), (robot_pos[0] + 25, robot_pos[1] - 15), 2)  # Antenna

    pygame.display.update()

# Main game loop
running = True
while running:
    draw_environment()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Command recognition
    command = recognize_speech()
    if command:
        move_robot(command)
        time.sleep(0.5)  # Delay to observe movement

pygame.quit()
