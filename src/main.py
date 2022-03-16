"""!
@file main.py
    This file contains a program that runs tasks which use proportional control 
    to run motors and encoders, and reads from an HPGL file. 

@author Nishka Chawla
@author Ronan Shaffer
@date   13-Mar-2022
@copyright (c) Released under GNU Public License
"""

import gc
import pyb
import cotask
import task_share
import print_task
import utime
import motor_chawla_shaffer
import encoder_chawla_shaffer
import closedloopcontrol
import servo
# import plot_task
import array as array
import math
import micropython

## Input pin configuration
inn = pyb.Pin.IN

## Output with push-pull control pin configuration
out = pyb.Pin.OUT_PP

# Define motor pins
## The enable pin for the motor 1. 
pinENA = pyb.Pin(pyb.Pin.cpu.A10, out)
## The enable pin for the motor 2. 
pinENB = pyb.Pin(pyb.Pin.cpu.C1, out)
## Pin variable for channel A of motor 1.
pinB4 = pyb.Pin(pyb.Pin.cpu.B4, out)
## Pin variable for channel B of motor 1.
pinB5 = pyb.Pin(pyb.Pin.cpu.B5, out)
## Pin variable for channel A of motor 2.
pinA0 = pyb.Pin(pyb.Pin.cpu.A0, out)
## Pin variable for channel B of motor 2.
pinA1 = pyb.Pin(pyb.Pin.cpu.A1, out)

# Define encoder pins
## Pin variable for channel 1 of the encoder A.
pinB6 = pyb.Pin(pyb.Pin.cpu.B6, out)
## Pin variable for channel 2 of the encoder A.
pinB7 = pyb.Pin(pyb.Pin.cpu.B7, out)
## Pin variable for channel 1 of the encoder B.
pinC6 = pyb.Pin(pyb.Pin.cpu.C6, out)
## Pin variable for channel 2 of the encoder B.
pinC7 = pyb.Pin(pyb.Pin.cpu.C7, out)

## Signal pin variable for servo.
pinA9 = pyb.Pin(pyb.Pin.board.PA9, out)

## Pin variable for limit switch.
pinC4 = pyb.Pin(pyb.Pin.board.PC4, out)

## Index to iterate through arrays
runs = 0

## Array size
array_size = int((2000/10)+1)

## Threaded rod scaling factor [ticks/in] 
r_sf = micropython.const(16384/20) 
## Wheel motor scaling factor [ticks/rad]
th_sf = micropython.const(276.3*180/math.pi) 

with open('line.hpgl') as f:
    ## Raw HPGL data
    raw_data = f.readline()
    ## HPGL data separated by semi-colons
    data = raw_data.split(';')

## Instantiation of servo object.
servo = servo.Servo(pinA9)

## Instantiation of Motor 1 position setpoint shared variable.
motor1setpoint = task_share.Share ('l', thread_protect = False, name = "motor1setpoint")
## Instantiation of Motor 2 position setpoint shared variable.
motor2setpoint = task_share.Share ('l', thread_protect = False, name = "motor2setpoint")

## Instantiation of Motor 1 position setpoint queue.
m1_queue = task_share.Queue ('l', 200, thread_protect = False, overwrite = False,
                        name = "m1_queue")
## Instantiation of Motor 2 position setpoint queue.
m2_queue = task_share.Queue ('l', 200, thread_protect = False, overwrite = False,
                        name = "m2_queue")

## Instantiation of Motor 1 proportional gain.
kp1 = task_share.Share ('f', thread_protect = False, name = "kp1")
## Instantiation of Motor 2 proportional gain.
kp2 = task_share.Share ('f', thread_protect = False, name = "kp2")

## Instantiation of motor 1 object.
motor1 = motor_chawla_shaffer.MotorDriver(pinENA, pinB4, pinB5, 3)
## Instantiation of motor 2 object.
motor2 = motor_chawla_shaffer.MotorDriver(pinENB, pinA0, pinA1, 5)

## Instantiation of encoder 1 object.
encoder1 = encoder_chawla_shaffer.EncoderDriver(pinB6, pinB7, 4)
## Instantiation of encoder 2 object.
encoder2 = encoder_chawla_shaffer.EncoderDriver(pinC6, pinC7, 8)

# Zeroing encoder 1.
encoder1.zero()
# Zeroing encoder 2.
encoder2.zero()

## Instantiation of controller object.
controller1 = closedloopcontrol.ClosedLoop(motor1setpoint.get(), kp1.get(), int(100), int(-100))
## Instantiation of controller object.
controller2 = closedloopcontrol.ClosedLoop(motor2setpoint.get(), kp2.get(), int(100), int(-100))

## Start time variable.
start_time = 0

def motor1_func ():
    """!
    Task which runs Motor 1 using proportional control, and reads current position from an encoder driver.
    """
    ## Current time variable.
    diff = 0
    start_time = utime.ticks_ms()
    while True:
        ## Sets motor duty cycle to actuation level
        next_time = utime.ticks_ms()
        diff = utime.ticks_diff(next_time, start_time)
        encoder1.update()
        motor1.set_duty_cycle(controller1.run(motor1setpoint.get(),encoder1.read()))
#         print_task.put(str(diff)+','+str(encoder1.read())+'\r\n')

        yield (0)
        
def motor2_func ():
    """!
    Task which runs Motor 2 using proportional control, and reads current position from an encoder driver.
    """
    ## Current time variable.
    diff = 0
    start_time = utime.ticks_ms()
    while True:
        ## Sets motor duty cycle to actuation level
        next_time = utime.ticks_ms()
        diff = utime.ticks_diff(next_time, start_time)
        encoder2.update()
        motor2.set_duty_cycle(controller2.run(motor2setpoint.get(),encoder2.read()))
#         print_task.put(str(diff)+','+str(encoder2.read())+'\r\n')
        yield (0)
        
def plot_func ():
    """!
    Task which reads an HPGL file and extracts r,theta coordinates
    """
    ## Index variable.
    idx = 0
    ## Pen down flag variable.
    PD_flag = 0
    ## Calibration flag variable.
    calib_flag = 0
    while True:
        
        if idx < len(data):
            ## Variable for current indexed variable of data
            item = data[idx]
            if item[0]+item[1] == 'IN' or calib_flag == 1 or calib_flag == 2:
                # Calibrate before beginning plot
                print('Calibrating...')
                calib_flag = 0
                idx += 1
            
            elif item[0]+item[1] == 'SP':
                print('SP')
                idx += 1
            
            elif item[0]+item[1] == 'PU':
                idx += 1
                # Raise pen servo.angle(60)
                print('Pen Up')
                servo.lift_pen()
            
            elif item[0]+item[1] == 'PD' and PD_flag == 0:
                PD_flag = 1
                ## List of raw HGL PD coordinates
                raw_item_list = item[2:]
                ## List of HGL PD coordinates separated by commas.
                item_list = raw_item_list.split(',')
                ## Item index variable 
                item_idx = 0
                # Lower pen servo.angle(-60)
                servo.drop_pen()
                
            elif PD_flag == 1:
                if item_idx < len(item_list):
                    ## X-coordinate variable
                    x = float(item_list[item_idx])
                    ## Y-coordinate variable
                    y = float(item_list[item_idx+1])
                    ## R-coordinate calculated from x- and y- coordinates.
                    r = math.sqrt(x**2+y**2)
                    ## Theta-coordinate calculated from x- and y- coordinates.
                    theta = math.atan(y/x)
                    
                    m1_queue.put(int(theta*th_sf))
                    m2_queue.put(int(r*r_sf))

                    motor1setpoint.put(int(theta*th_sf))
                    motor2setpoint.put(int(r*r_sf))
                    
                    if controller2.is_close():
                        item_idx += 2
                    
                elif item_idx == len(item_list):
                    idx += 1
                    
        yield (0)
        

def print_func ():
    """!
    Task which prints current encoder reading.
    """    
    ## Runs index variable.
    runs = 0
    while True:
        print_task.run()
        # while enc2reading.any():
            # encreading.run()
            # pos_list[runs].append(enc2reading.get())
            # print ("{:} ".format(enc2reading.get())) # this works 
            # print ("{:} ".format(pos_list[runs]))    # this doesnt
            
            # print(pos_list[runs])
        runs += 1

        yield (0)

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    # print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
    #        'Press ENTER to stop and show diagnostics.')

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed

    ## Instantiation of Motor 1 Task 
    motor1_task = cotask.Task (motor1_func, name = 'motor1_task', priority = 2, 
                         period = 10, profile = True, trace = False)
    ## Instantiation of Motor 2 Task 
    motor2_task = cotask.Task (motor2_func, name = 'motor2_task', priority = 2, 
                         period = 10, profile = True, trace = False)
    ## Instantiation of HPGL Plotting Task 
    plot_task = cotask.Task (plot_func, name = 'plot_task', priority = 2, 
                         period = 10, profile = True, trace = False)
    ## Instantiation of Read Task 
    read_task = cotask.Task (print_func, name = 'read_task', priority = 3, 
                         period = 20, profile = True, trace = False)
    
    ## Input for Kp 1
    KP1 = 0.1
    controller1.set_Kp(float(KP1))
    kp1.put(float(KP1))
    
    ## Input for Kp 2
    KP2 = 0.1
    controller2.set_Kp(float(KP2))
    kp2.put(float(KP2))
        
    cotask.task_list.append(motor1_task)
    cotask.task_list.append(motor2_task)
#     cotask.task_list.append(read_task)
    cotask.task_list.append(plot_task)
    
    start_time = utime.ticks_ms()

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    ## Serial port variable
    vcp = pyb.USB_VCP ()
    try:
        vcp.read ()
        while not vcp.any ():
            cotask.task_list.pri_sched ()
    except KeyboardInterrupt:
        motor1.set_duty_cycle(0)
        motor2.set_duty_cycle(0)
    # Empty the comm port buffer of the character(s) just pressed
    # vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))