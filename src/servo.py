"""!
@file servo.py
This file contains code used to configure the servo motor. 

@details Objects of this class can be used to control the servo to raise and lower the pen.
    
@author Nishka Chawla
@author Ronan Shaffer
@date   13-Mar-2022
@copyright (c) Released under GNU Public License
"""

import pyb
import time
import math

## Output with push-pull control pin configuration
out = pyb.Pin.OUT_PP

class Servo:
    """!
    This class implements an servo driver for the ME405 Pen Plotter Term Project. 
    """
    
    def __init__(self, pinA, tim_num=1):
        """!
        Creates a servo driver.
        @param pinA         Defines the signal pin variable for the servo.
        @param tim_num      Defines the number of the timer object.
        """
        
        ## Timer object used for encoder counting.
        self.tim = pyb.Timer(tim_num, freq=50)
        
        ## Servo Channel 3 for a timer object.
        self.tch2 = self.tim.channel(2, pyb.Timer.PWM, pin=pinA)

        
    def drop_pen(self):
        """!
        This method actuates the servo to draw on the paper.
        """
        self.tch2.pulse_width_percent(3)
        
    def lift_pen(self):
        """!
        This method actuates the servo to lift the pen from the paper.
        """
        self.tch2.pulse_width_percent(6)

# 2-12 pulse width percent is 0-90 deg

# if __name__ == '__main__':
# 
#     ## Pin variable for channel 2 of the encoder B.
#     pinA9 = pyb.Pin(pyb.Pin.board.PA9, out)
#     
#     ## Instantiation of servo object.
#     servo = Servo(pinA9)
    
#     try:
#     while True:
#         pinA9.high()
#         servo.drop_pen()
#         time.sleep(0.5)
#         servo.lift_pen()
#         pinA9.low()
#         time.sleep(0.5)
#         pinA9.high()
#         time.sleep(0.5)
#         pinA9.low()
#     except KeyboardInterrupt:
#     
#         break