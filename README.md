# Face Turret Project

## Overview
The Face Turret project is an interactive hardware and software system that uses computer vision to track human faces and control servo motors accordingly. It's built using OpenCV for face detection and an Arduino for servo control.

## Features
- Real-time face tracking using OpenCV.
- Servo motor control for turret movement.
- Adjustable dead zone for improved tracking accuracy.
- Easy-to-use and modify Python and C++ code.

## Hardware Requirements
- Arduino Uno
- Servo Motors (2x)
- Webcam or Camera Module
- Breadboard and Jumper Wires

## Software Requirements
- Arduino IDE
- Python 3.x
- OpenCV Library
- PySerial Library

## Installation
1. Install Python 3.x and the necessary libraries (OpenCV and PySerial).
2. Upload the C++ code to the Arduino using the Arduino IDE.
3. Connect the webcam and Arduino to your computer.
4. Run the Python script to start face tracking.

## Usage
Run the Python script `face_turret.py` to start the face tracking turret. The servos will move to follow the detected face within the camera's field of view.

## Customization
You can adjust the dead zone parameters and initial servo positions in the Python script to suit your setup.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License
This project is open source and available under the MIT License.

## Acknowledgements
Special thanks to Shubham Santosh for the initial concept and implementation of the Face Tracker using OpenCV and Arduino.

## Contact
For any queries or issues, please open an issue on the GitHub repository or contact the maintainers directly.

