import time
import sys

#importing all required classes for input and output devices
from sensor_library import *
from gpiozero import Motor
from gpiozero import LED
from gpiozero import Buzzer
from gpiozero import Button

#initializing all input and output devices
sensor1 = Distance_Sensor()
sensor2 = Distance_Sensor() #couldn't implement a second distance sensor into our physical prototype but would be used ideally
led_red = LED(5)
led_green = LED(6)
motor1 = Motor(forward = 12, backward=21)
motor2 = Motor(forward = 8, backward = 7)
sound = Buzzer(22)
push = Button(13)

#initializing instance variables
threshold = 0
current_average = 0
max_distances = [0,0,0,0,0]
space = 0

'''
Check distance function: 
This function will continuously take data in from the sensors 
and if the second data point is greater than the first one the 
loop will break otherwise sensor data will continue to be called. 
This is used with the threshold average function to stop it from 
taking values when the bar is moving up. 
'''
def check_distance():
    while True:
        d1 = sensor1.distance()
        time.sleep(0.2)
        d2 = sensor1.distance()
        print("current distance: ", d2)
        if d2>d1:
            break
        
'''
Threshold average function: This function will calculate the average
of the max distance the bar travels for 5 data points. This value is
used as the threshold average distance which is what all averages
calculated later in the program will be compared to.
'''
def threshold_average():
    counter = 0
    #runs until five data points have been entered into the list for the distances
    while counter<5:
        d1 = sensor1.distance()
        print("current distance: ", d1)
        time.sleep(0.2)
        d2 = sensor1.distance()
        print("current distance : ", d2)
        #checking if the bar is still moving down (second distance is further from sensor than first)
        if d2 > d1: 
            #space declared a global variable used so that it can be accessed and changed within the function
            global space
            space = d2
        #if bar is no longer moving down lowest point will be added to list to be used to calculate the threshold average
        else:
            max_distances.insert(counter,space)
            max_distances.pop()
            print("last five distances: ", max_distances)
            d2 = 0
            d1 = 0
            counter += 1
            check_distance()
    print("current distance: ", d2)
    threshold = sum(max_distances)/5
    return threshold #returns the calculated average

'''
Rolling average function: This function will calculate the average
of the distance the bar travels for 5 data points, smoothing the values out. 
This value is used to compare to the threshold to detect if failure happens.
'''
def rolling_average():
    d1 = sensor1.distance()
    time.sleep(0.1)
    d2 = sensor1.distance()
    #checking if the bar is still moving down (second distance is further from sensor than first) 
    if d2 > d1:
        #space declared a global variable used so that it can be accessed and changed within the function
        global space
        space = d2
    #if bar is no longer moving down lowest point will be added to list to be used to calculate the rolling average
    else:
        max_distances.insert(0,space)
        max_distances.pop()
        print ("last five distances: ", max_distances) 
    current_average = sum(max_distances)/5
    print("current distance: ", d2, "\t current average: ", current_average)
    return current_average 

'''
Stuck function: This function will check if 5 distances that were calculated
are all within 10mm of each other (above or below). If this is the case
failure function will be activated because the user is stuck in place
'''
def stuck():
    counter = 0
    distances = [0]*5
    #this loop takes in 5 data points
    for i in range(5): 
        distances[i] = sensor1.distance()
        time.sleep(0.35)
        print(distances)
    #this loop compares all values within the list to see if they are within 10mm of each other
    for i in range(4): 
        if distances[i+1]-10 <= distances[i] and distances[i]<=distances[i+1]+10:
            counter += 1
    #if all 5 values are within that range failure will be called
    if counter == 4:
        failure()

'''
Balance function: This function will check if 1 side of the bar is 
imbalanced compared to the other side the respective motor will be 
activated to rebalance the bar. 
'''
def balance():
    #while sensor1 side of the bar is higher than sensor2 side motor1 is activated until rebalanced
    while sensor1.distance()>sensor2.distance():
        print(sensor2.distance() + 20)
        motor1.backward() 
        print("balancing weights - motor 1 is reversing")
        print("current plate 1 distance: ", sensor1.distance(), "\t current plate 2 distance: ", sensor2.distance())
    motor1.stop()
    
    #while sensor1 side of the bar is lower than sensor2 side motor2 is activated until rebalanced
    while sensor1.distance() < sensor2.distance():
        print(sensor2.distance() + 20)
        motor2.backward()
        print("balancing weights - motor 2 is reversing")
        print("current plate 1 distance: ", sensor1.distance(), "\t current plate 2 distance: ", sensor2.distance())
    motor2.stop()
    
    print("motor 1: OFF motor2: OFF \t current plate 1 distance: ", sensor1.distance(), "\t current plate 2 distance: ", sensor2.distance())

'''
Failure function: This function will sound a buzzer and then activate the motors
to bring the bar back up. It will then wait for the button to be pressed again
to reset the bar and then wait once again for the button to be pushed before
returning to the main
'''
def failure():
    sound.on()
    time.sleep(2)
    sound.off()
    #runs until the bar is 90mm away from the sensor
    while sensor1.distance() > 90:
        print ("Current distance: ", sensor1.distance())
        motor1.backward(0.2)
        motor2.backward(0.22)
        print("motor 1 and 2 are reversing")
    motor1.stop()
    motor2.stop()
    time.sleep(1)
    led_green.off()
    push.wait_for_press()
    print("waiting for press to reset bar")
    motor1.forward(0.2)
    motor2.forward(0.22)
    print("button was pressed")
    print("motor 1 and 2 moving forward")
    time.sleep(2.5)
    motor1.stop()
    motor2.stop()
    print("motor 1 and 2 stopped")
    push.wait_for_press()
    print("waiting for press to continue lifting")

    
'''
Main function:
This function executes all of the above functions to
1. button pressed and takes a threshold average during warmup
2. user presses button and begins lift
3. compare current average to threshold and activates failure if needed
4. check if user is stuck in one spot
'''
def main():
    push.wait_for_press()
    led_red.on()
    print("Red light ON")
    threshold = threshold_average()
    print("Threshold height: " , threshold)

    push.wait_for_press()
    led_red.off()
    print("Red light OFF")
    led_green.on()
    print("Green light ON, Red light OFF")
    
    #continuously runs to check for current average compared to threshold and stuck function    
    while True:
        current_average = rolling_average()
        print (current_average)
        if current_average > threshold+20:
            print("failure")
            failure()
        stuck()
