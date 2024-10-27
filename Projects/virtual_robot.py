import pygame
import speech_recognition as sr
import time
import math

# Step 1: Process the speech command and identify the destination
def process_command(command):
    if "hungry" in command or "eat" in command:
        return "kitchen"
    elif "sleep" in command:
        return "bedroom"
    elif "relax" in command or "watch TV" in command:
        return "living room"
    else:
        return "unknown"

# Step 2: A simple pathfinding function (simulates movement)
def move_towards(target, position):
    if position[0] < target[0]:
        position[0] += 1
    elif position[0] > target[0]:
        position[0] -= 1

    if position[1] < target[1]:
        position[1] += 1
    elif position[1] > target[1]:
        position[1] -= 1

    return position

# Step 3: Obstacle avoidance (checks if there's an obstacle)
def avoid_obstacles(position, obstacles):
    if tuple(position) in obstacles:
        print("Obstacle encountered! Finding alternative route...")
        position[0] += 1  # Simple adjustment to avoid obstacle
    return position

# Step 4: Voice recognition using SpeechRecognition
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

# Step 5: Simulate robot movement in the virtual environment
def navigate_to(destination):
    global robot_position
    target = house_map.get(destination)
    if not target:
        print(f"Destination '{destination}' not found!")
        return
    
    while robot_position != list(target):
        robot_position = move_towards(target, robot_position)
        robot_position = avoid_obstacles(robot_position, obstacles)
        print(f"Moving to {destination}: Current position: {robot_position}")
        time.sleep(1)  # Simulate movement delay
    
    print(f"Robot has arrived at the {destination}.")

# Environment Setup
house_map = {
    "kitchen": (7, 2),  # Coordinates of the kitchen
    "bedroom": (1, 8),
    "living room": (4, 5),
}

robot_position = [2, 2]  # Robot's starting position
obstacles = [(3, 3), (5, 4), (6, 6)]  # Simulated obstacles

# Main program loop
if __name__ == "__main__":
    command = recognize_speech()
    destination = process_command(command)
    if destination != "unknown":
        print(f"Destination identified: {destination}")
        navigate_to(destination)
    else:
        print("Sorry, I couldn't understand where you want to go.")
