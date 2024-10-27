Way Finders
Way Finders is a 2D robot navigation project using Pygame, allowing the robot to move around a grid and avoid obstacles within various room layouts.

Table of Contents
Prerequisites
Installation
Cloning the Repository
Running the Project
Project Structure
Usage
License
Prerequisites
Ensure you have the following installed:

Python 3.7 or later
Pygame library for creating the 2D environment
SpeechRecognition library for recognizing voice commands (if applicable)
PyAudio (for microphone input)
To install the required Python packages, run:

bash
Copy code
pip install pygame SpeechRecognition pyaudio
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/Way_Finders.git
Navigate into the project directory:

bash
Copy code
cd Way_Finders
Install dependencies (if not installed already):

bash
Copy code
pip install -r requirements.txt
Note: Ensure you have pyaudio installed if using the voice command feature. If installation fails on Windows, use a .whl file from this link.

Running the Project
To run the project, execute the following command in your terminal:

bash
Copy code
python robo.py
This will launch a Pygame window where the robot will navigate according to the obstacle placements and command inputs.

Project Structure
robo.py - Main script that initializes Pygame, sets up robot movement, and handles obstacles.
Room Images - PNG files (bathroom.png, bedroom.png, etc.) representing the various room layouts.
Other Python Files - Supporting code for virtual robot logic, voice recognition, and robot control.
Wall Image - wall.png, which is used to represent obstacles or walls.
Usage
Run robo.py to open the simulation window.
Use voice commands (if implemented) to direct the robot or manually control it through the code.
License
This project is licensed under the MIT License. See the LICENSE file for details.

