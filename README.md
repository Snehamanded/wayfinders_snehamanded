IRDP 1: ROS 2 Virtual Robot Navigation Project (Way_Finders)
This project is a speech-guided autonomous robot navigation system using ROS 2 and Gazebo in a Docker environment. It simulates a virtual robot that receives voice commands, interprets them, and navigates accordingly using speech recognition and natural language processing.

Setup, Installation, and Usage Guide

Prerequisites
Docker: Download and install Docker Desktop for your operating system.
X Server (for GUI support on Windows): Install an X server like VcXsrv or Xming to display the Gazebo GUI in WSL or on Windows.

Installation and Setup

1. Clone the Repository
Clone the project repository and navigate into the project folder:
git clone https://github.com/Hack2Future-IIIT-Dharwad/wayfinders.git
cd ros2-navigation-project

2. Build the Docker Image
Use the provided Dockerfile to create a Docker image that includes ROS 2, Gazebo, Whisper, and LLaMa:
docker build -t ros2_navigation_project .

3. Run the Docker Container
Linux and macOS: Use xhost to allow Docker access to the X server:
xhost +local:docker
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    ros2_navigation_project

Windows (WSL 2):
Start the X server (e.g., VcXsrv) with “Disable access control” enabled.
Run Docker in WSL with the display configured:
docker run -it --rm \
    -e DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    ros2_navigation_project

4. Build the ROS Workspace in Docker
Once inside the Docker container:
source /opt/ros/humble/setup.bash
cd ~/ros2_ws
colcon build

5. Launch Gazebo with TurtleBot3
Run a pre-configured Gazebo world with TurtleBot3:
ros2 launch turtlebot3_gazebo turtlebot3_world.launch
To customize environments, modify .world files in ~/ros2_ws/src/turtlebot3_simulations/turtlebot3_gazebo/worlds/.

6. Set Up Speech Recognition and LLM
Activate the Python virtual environment:
source ~/ros2_ws/venv/bin/activate
Use Whisper for capturing and transcribing speech, and LLaMa for processing commands to generate navigation goals (e.g., "Go to the kitchen").

7. Run the Project Workflow
Simulate Speech-to-Text: Run a Python script to capture and transcribe speech using Whisper and interpret it with LLaMa.
Send Navigation Goals: Use LLaMa's output as navigation goals for ROS's Navigation stack.
To visualize in RViz, run:
ros2 launch turtlebot3_navigation2 navigation_launch.py
rviz2
