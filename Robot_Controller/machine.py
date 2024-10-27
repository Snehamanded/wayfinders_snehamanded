from controller import Robot, DistanceSensor
import speech_recognition as sr  # Import SpeechRecognition library

# Initialize Webots Robot
robot = Robot()
TIME_STEP = int(robot.getBasicTimeStep())

# Motor Initialization
wheel_names = ['front left wheel', 'front right wheel', 'back left wheel', 'back right wheel']
wheel_motors = [robot.getDevice(name) for name in wheel_names]

# Set motors to velocity control mode
for motor in wheel_motors:
    motor.setPosition(float('inf'))
    motor.setVelocity(0.0)

# Obstacle Sensors Initialization
distance_sensor_names = {
    "front": "so0",
    "left": "so7",
    "right": "so15"
}

# Initialize distance sensors
distance_sensors = {}
for name, sensor_name in distance_sensor_names.items():
    sensor = robot.getDevice(sensor_name)
    sensor.enable(TIME_STEP)
    distance_sensors[name] = sensor

# Movement Commands
def move_forward(speed=8.0):
    for motor in wheel_motors:
        motor.setVelocity(speed)

def stop_movement():
    for motor in wheel_motors:
        motor.setVelocity(0.0)

def turn_left(duration=TIME_STEP * 10):  
    wheel_motors[0].setVelocity(2.0)  # Reduced left wheel speed
    wheel_motors[1].setVelocity(5.0)  # Increased right wheel speed
    wheel_motors[2].setVelocity(2.0)  # Reduced left wheel speed
    wheel_motors[3].setVelocity(5.0)  # Increased right wheel speed
    robot.step(duration) 

def turn_right(duration=TIME_STEP * 10):  
    wheel_motors[0].setVelocity(5.0)  # Increased left wheel speed
    wheel_motors[1].setVelocity(2.0)  # Reduced right wheel speed
    wheel_motors[2].setVelocity(5.0)  # Increased left wheel speed
    wheel_motors[3].setVelocity(2.0)  # Reduced right wheel speed
    robot.step(duration)  

def turn_slight_left(duration=TIME_STEP * 5):  
    wheel_motors[0].setVelocity(4.0)  # Reduced left wheel speed
    wheel_motors[1].setVelocity(6.0)  # Increased right wheel speed
    wheel_motors[2].setVelocity(4.0)  # Reduced left wheel speed
    wheel_motors[3].setVelocity(6.0)  # Increased right wheel speed
    robot.step(duration)  

def turn_slight_right(duration=TIME_STEP * 5):  
    wheel_motors[0].setVelocity(6.0)  # Increased left wheel speed
    wheel_motors[1].setVelocity(4.0)  # Reduced right wheel speed
    wheel_motors[2].setVelocity(6.0)  # Increased left wheel speed
    wheel_motors[3].setVelocity(4.0)  # Reduced right wheel speed
    robot.step(duration)  

# Obstacle Avoidance Logic
def avoid_obstacles():
    front = distance_sensors["front"].getValue()
    left = distance_sensors["left"].getValue()
    right = distance_sensors["right"].getValue()

    print(f"Front: {front}, Left: {left}, Right: {right}")  # Add print statement

    # Define thresholds and dead zone
    base_speed = 8.0
    reduced_speed = 5.0
    close_obstacle_threshold = 800
    very_close_threshold = 500
    dead_zone_threshold = 2000  

    # Obstacle avoidance strategy
    if front < very_close_threshold:
        # If very close, immediately turn to the side with more space
        if left > right:
            turn_left(duration=TIME_STEP * 15)  
        else:
            turn_right(duration=TIME_STEP * 15)  
    elif front < close_obstacle_threshold:
        # If within close range, make a slight adjustment and slow down
        move_forward(reduced_speed)
        if left > right:
            turn_slight_left()
        else:
            turn_slight_right()
    elif front > dead_zone_threshold:
        # In dead zone, continue forward at full speed
        move_forward(base_speed)
    else:
        # Continue forward at reduced speed
        move_forward(reduced_speed)

# Function to process voice commands
def process_voice_command(audio_samples):
    r = sr.Recognizer()
    audio_data = sr.AudioData(audio_samples, 44100, 2)  # Assuming 44100 Hz sampling rate and 2 channels
    try:
        command = r.recognize_google(audio_data).lower()
        print("Recognized command:", command)

        if command == "forward":
            move_forward()
        elif command == "stop":
            stop_movement()
        elif command == "left":
            turn_left()
        elif command == "right":
            turn_right()
        else:
            print("Unrecognized command:", command)

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Main Control Loop
while robot.step(TIME_STEP) != -1:
    avoid_obstacles()

    # ... (Add code to listen for voice commands and process them)
    # ... (You'll need to initialize a microphone device and use the 'process_voice_command' function)