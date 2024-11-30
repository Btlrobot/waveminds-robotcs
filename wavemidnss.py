#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
touchled_3 = Touchled(Ports.PORT3)
distance_2 = Distance(Ports.PORT2)
front_left = Motor(Ports.PORT12, False)
back_left = Motor(Ports.PORT6, False)
back_right = Motor(Ports.PORT1, True)
front_right = Motor(Ports.PORT7, True)
optical_9 = Optical(Ports.PORT9)
# vex-vision-config:begin
vision_4__RED_BLOCK = Signature(1, 5137, 8973, 7055,-2101, -375, -1238,1.8, 0)
vision_4 = Vision(Ports.PORT4, 150, vision_4__RED_BLOCK)
# vex-vision-config:end
drone_launcher = Motor(Ports.PORT8, False)



# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 
    
# Initialize random seed 
initializeRandomSeed()

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
# 	Author:       VEX
# 	Created:
# 	Description:  VEXcode IQ Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code
def stop_driving():
    front_left.stop()
    front_right.stop()
    back_left.stop() 
    back_right.stop()
def set_drive_speed(speed):
    front_left.set_velocity(speed)
    front_right.set_velocity(speed)
    back_left.set_velocity(speed)
    back_right.set_velocity(speed)
def drive_forward():
    front_left.spin(FORWARD)
    front_right.spin(FORWARD)
    back_left.spin(FORWARD)
    back_right.spin(FORWARD)
    
def drive_reverse():
    front_left.spin(REVERSE)
    front_right.spin(REVERSE)
    back_left.spin(REVERSE)
    back_right.spin(REVERSE)

def turn_left():
    front_left.spin(REVERSE)
    back_left.spin(REVERSE)
    front_right.spin(FORWARD)
    back_right.spin(FORWARD)

def turn_right():
    front_left.spin(FORWARD)
    back_left.spin(FORWARD)
    front_right.spin(REVERSE)
    back_right.spin(REVERSE)

def scan():
    print(distance_2.object_size())

    while not distance_2.is_object_detected():
        print(distance_2.object_size())
        turn_left()
        wait(20,MSEC)
    stop_driving()
    print(distance_2.object_size())

def moveToTarget(target):
    while not target > distance_2.object_distance(MM):
        drive_forward()
        wait(20,MSEC)
    stop_driving()

def blockScan():
    optical_9.gesture_disable()
    optical_9.set_light(LedStateType.ON)
    optical_9.set_light_power(100,PERCENT)
    while not optical_9.is_near_object() and distance_2.object_distance(MM) < 100:
        turn_left()
        wait(20,MSEC)
    stop_driving()
    return optical_9.color()

def UpdateLed(colorDetected):
    touchled_3.set_brightness(100)
    touchled_3.set_color(colorDetected)

def color_screen_color(color_screen):
    brain.screen.set_fill_color(color_screen)
    brain.screen.draw_rectangle(0,0,159,107)
    for i in range(5):
        brain.play_sound(SoundType.ALARM2)
        wait(100,MSEC)
    wait(1,SECONDS)
def go_to_object():
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)

        # Take a snapshot with the Vision Sensor with the specified signature and 
        # store the object data into a variable

        vision_object = vision_4.take_snapshot(vision_4__RED_BLOCK)

        # Check the variable to see if a valid object was detected when the snapshot
        # was captured. If yes, print the data
        if vision_object is not None:
            brain.screen.print("Center X:", vision_4.largest_object().centerX)
            brain.screen.next_row()

            brain.screen.print("Center Y:", vision_4.largest_object().centerY)
            brain.screen.next_row()
            if vision_4.largest_object().centerX < 100 and vision_object is not None:
                turn_right()
            if vision_4.largest_object().centerX > 170 and vision_object is not None:
                turn_left()
            if vision_4.largest_object().centerX > 100 and vision_4.largest_object().centerX < 170 and vision_object is not None:
                moveToTarget(200)
                return optical_9.color()
            
            # Take a new snapshot every 0.2 seconds
            wait(0.2, SECONDS)

        else:
            turn_left()
            brain.screen.print("No Object Found")
set_drive_speed(100)
 

'''
while True:
    testy = 0
    if testy == 0:
        if brain.buttonLeft.pressing():
            drive_forward()
            
            wait(2,SECONDS)
            stop_driving()
            turn_right()
            wait(2,SECONDS)
            stop_driving()
        elif brain.buttonRight.pressing():
            drive_reverse()
            wait(2,SECONDS)
            stop_driving()
            turn_left()
            wait(2,SECONDS)
            stop_driving()
        elif touchled_3.pressing():
            if testy == 0:
                testy = 1
                touchled_3.set_color(Color.BLUE)
                wait(20,MSEC)
            else:
                testy = 0
                touchled_3.set_color(Color.RED)
                wait(20,MSEC)
    elif testy == 1:
        if brain.buttonLeft.pressing():
            turn_left()
            wait(2,SECONDS)
            stop_driving()
        elif brain.buttonRight.pressing():
            turn_right()
            wait(2,SECONDS)
            stop_driving()
        elif touchled_3.pressing():
            if testy == 0:
                testy = 1
            else:
                testy = 0
'''
while True:
    

    go_to_object()
    colory = Color.RED

    UpdateLed(colory)
    color_screen_color(colory) 
    wait(5,SECONDS)
    turn_left()
    wait(1,SECONDS)
    stop_driving()
