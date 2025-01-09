# SureSpot-Elite
This project is a simple control system for a bar lift using distance sensors, motors, and a button. The system monitors the position of the bar and ensures it lifts correctly by controlling motors based on sensor inputs. If a failure occurs (e.g., the bar is stuck or imbalanced), the system takes corrective actions and alerts the user via a buzzer.

## Features
- **Threshold Detection**: Continuously measures the distance traveled by the bar and calculates a threshold average for movement.
- **Rolling Average**: Smooths out sensor data to provide a stable current position of the bar.
- **Stuck Detection**: Detects if the bar has stopped moving for a certain period and triggers a failure response.
- **Balance Control**: Ensures that both sides of the bar remain balanced, activating motors as necessary.
- **Failure Response**: Sounds a buzzer and reverses motors to correct the bar's position if failure is detected.
- **User Interaction**: A button allows users to reset or continue the lifting process.

## Hardware Requirements
- **Distance Sensors**: Two distance sensors (one for each side of the bar).
- **Motors**: Two motors (to lift the bar and correct imbalance).
- **LEDs**: Two LEDs to indicate system status (red for warning and green for ready).
- **Buzzer**: A buzzer for failure alerts.
- **Button**: A button to reset the bar.

## Libraries Used
- `gpiozero`: A library for controlling GPIO devices on Raspberry Pi (e.g., motors, LEDs, buzzer, button).
- `sensor_library`: A custom library for handling distance sensors.

## Functions

### `check_distance()`
This function continuously takes distance readings from the first sensor and breaks the loop when the second reading is greater than the first, indicating the bar is no longer moving down.

### `threshold_average()`
Calculates the threshold average by taking five distance readings and using them to determine the average distance for comparison during operation.

### `rolling_average()`
Calculates the rolling average of five distance readings to smooth out the bar’s movement data and compare it to the threshold.

### `stuck()`
Checks if the bar is stuck by measuring five distance readings and determining if they are within 10mm of each other. If so, the system activates the failure response.

### `balance()`
Balances the bar by comparing the distance readings from the two sensors. If one side is higher than the other, the corresponding motor is activated to bring the bar to an even level.

### `failure()`
Triggers when a failure is detected. The system sounds a buzzer, reverses the motors to bring the bar down, and waits for a button press to reset the system.

### `main()`
The main function that coordinates all other functions:
1. Waits for a button press to start the process.
2. Takes a threshold average during the warm-up phase.
3. Starts the lift, comparing the current average to the threshold.
4. Monitors if the bar is stuck and activates failure if necessary.

## Setup Instructions

1. Install the required libraries:
   - `gpiozero`: `pip install gpiozero`
   - `sensor_library`: Ensure that the custom sensor library is available in your project directory.

2. Connect the hardware components to your Raspberry Pi:
   - **Distance Sensors**: Connect to the appropriate GPIO pins as per your setup.
   - **LEDs**: Connect the LEDs to GPIO pins 5 (red) and 6 (green).
   - **Motors**: Connect motors to GPIO pins 12, 21 (motor 1) and 8, 7 (motor 2).
   - **Buzzer**: Connect to GPIO pin 22.
   - **Button**: Connect to GPIO pin 13.

3. Run the code (SureSpotElite.py)
4. The system will wait for a button press to begin the lifting process. It will automatically monitor the bar's movement and handle any imbalances or failures.
