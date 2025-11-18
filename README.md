# Padiddle-Car-Game

A physical two-player reaction game built with a Raspberry Pi, arcade buttons, and a 1602 LCD display.


**Overview**

Padiddle is a real-world, in-car reaction game based on the classic Padiddle tradition. The entire system is housed inside a small box that sits in the center console of a car. A Raspberry Pi inside runs the game logic, reads button inputs, and updates the score on a 1602 LCD display.

Two large arcade buttons, one blue for the passenger and one red for the driver, sit on the top of the box. When a player spots a car with one working headlight, both players race to hit their button first. The Raspberry Pi detects the winner and updates the score immediately on the display.

Everything is powered by a portable charger inside the box, which means there are no external wires running through the car.


**Features**

1. Two-player real-time reaction gameplay
2. Large arcade-style push buttons wired to Raspberry Pi GPIO pins
3. 1602 LCD display that shows both scores
4. Self-contained, portable design
5. No external wiring
6. Simple and reliable game logic that works during long car rides


**Hardware Components**

This project uses the following parts:
1. Raspberry Pi Zero or Pi 3 Model B Plus
2. 1602 LCD screen
3. I2C backpack for the LCD
4. One red arcade button (driver side)
5. One blue arcade button (passenger side)
6. Jumper wires
7. Portable USB battery pack
8. Small project enclosure box


**Gameplay**

1. Players watch the road for cars in real life.

2. When a car with exactly one working headlight is spotted, players race to press their button.

3. The Raspberry Pi detects which button was pressed first.

4. The LCD updates the score.


**Software Behavior**

The Python script does the following:

1. Sets up GPIO pins for both buttons
2. Initializes and writes to the 1602 LCD
3. Tracks and displays both scores
4. Detects the first button press using debouncing
5. Updates the LCD instantly
6. Loops continuously with minimal delay
7. The code is written to be simple, clear, and sturdy enough to run for hours.

**Running the Game**

Clone the repository on your Raspberry Pi:

git clone https://github.com/Eli-Wit/Padiddle.git
cd Padiddle


**Run the script:**

python3 padiddle.py

Make sure I2C is enabled in the Raspberry Pi configuration tool.
License
