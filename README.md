# me405_PenPlotterProject

## Project Description

### Project Introduction

For the Mechatronics term project, this group elected to design and build a 2.5 axis pen plotter. The purpose of this machine is to take a Hewlett-Packard Graphics Language (HPGL) file,
which encodes the relevant commands and coordinates to draw an image, and autonomously plot the image on a flat piece of paper. It is intended for educational use so that students can
practice both mechanical and firmware design principles.

### Hardware Design Overview

This group's pen plotter operates on a polar coordinate system, naturally producing curvilinear motion as it traces out the image on file over a 360 degree range of motion.
It rotates about a central base, upon which two Ametek-Pittman motors are mounted parallel to the plotting surface, in addition to the STM Nucleo microcontroller.
One motor is coupled to a 1/4 inch shaft and directly drives a wheel 14 inches from the rotating base, controlling the angular position of the pen during plotting. 
The other motor, locating directly beneath the first, is coupled to a threaded rod. An aluminum beam attached to the central mount provides structural support to the adjacent rod and shaft,
fixing them in place to minimize deviation from the encoded trajectory which would introduce undesirable wobble. Finally, a hobby servo motor is mounted next to the pen on the hex nut
which travels the length of the threaded rod, controlling the radial position of the pen. The servo actuates the pen via a small linkage to lift or drop the pen onto the paper. All three
motors are wired to the Nucleo which is connected to benchtop power supply. The nucleo is also connected to a computer which communicates to the Nucleo with a USB cable to run the program.
The motor mount and base, the drive wheel, and the pen/servo mount were 3D printed, while the threaded rod, shaft, support beam, and bearings were procured either on campus or from online vendors.

### Software Design Overview

Our program runs from a main script, which loops through a task list, executing each task from the scheduler according to its priority. Upon startup, gains are set from the PC and then the
HPGL file to be plotted is opened and read, at which point a list is created storing the sequence of setpoints determined by the HPGL coordinates. The task scheduler then starts iterating 
through the motor and plot tasks to trace out the image on file. The motor tasks, which include the controller, encoder, and motor drivers, are responsible for assigning setpoints and 
computing the error between each measured and desired position to output duty cycles to the motors. The measured position comes from the encoder driver, and the error and duty cycle output
is computed by the closed-loop controller driver, which sends the pulse width modulation (PWM) signal to the motor driver, which sends this signal to the corresponding channel of the relevant 
motor to actuate the pen in the radial or angular direction. Every time a Pen-Up or Pen-Down command is read from the HPGL file, the servo is actuated to lift or drop the pen.

### Testing & Results

Our system was mainly tested by applying a step response to the Ametek-Pittman motors to determine proportional gain values to use during plotting. Additional step response tests were conducted, 
varying the controller task frequency to test its performance. This ensured minimal overshoot and oscillation as the motors were directed to each setpoint. 
With gain values of 0.1 [% duty cycle / encoder count] at a rate of 100 Hz, our system performed reasonably well for its application.

### Project Takeaways & Learning Outcomes

Over the course of this project, we learned the most from what went wrong and not according to plan. The hardware design timeframe took much longer than anticipated, eating into the available
time to write and debug software. For example, tolerances and press fits for 3D printed parts were difficult and required multiple reprints. Simple attachments, such as between the pen and servo
linkage, were surprisingly difficult when trying to formulate a simple and robust connection for very small parts and surfaces. We found the simpler we kept our design, the better it functioned
and the less room for error there was. Designing a modular system made it easier to modify and improve our design when one subsystem was not performing well, like when the threaded rod needed
more constraints to minimize extraneous motion or when the servo and pen did not fit well in the hex nut mount. On the software side of the device, being able to independently develop and test
modules, like our controller and motor drivers, prior to this project allowed us to more easily integrate them into our main program because we knew they worked on their own. The biggest hurdle
that we ultimately could not overcome was the time constraint on this project, as we did not have enough time to further develop and debug our dual motor-controller program. This resulted in
distorted plots as each motor approached a setpoint at different rates along its own axis. If more time were available to improve our software, we would further debug our controllers and experiment 
with full PID control to mitigate this issue. We would also be able to refine our scaling function so that the coordinate system is feasible for our pen plotter, as well as interpolating between points
to minimize the room for error.

#### Bill of Materials 
###### Below is a bill of materials for major components of our system. 

| Qty. | Part                  | Source                | Est. Cost |
|:----:|:----------------------|:----------------------|:---------:|
|  2   | Pittperson Gearmotors | ME405 Tub             |    -      |
|  1   | Nucleo with Shoe      | ME405 Tub             |    -      |
|  1   | Sharpie    	       | Backpack              |    -      |
|  1   | Hobby Servo           | Amazon                |   $5      |
|  1   | Lead Screw  - 1/4-20  | McMaster-Carr         |   $15     |
|  1   | Drive Shaft - 1/4 in  | Teche Lab             |    -      |
|  1   | Shaft Couplers        | Amazon		       |   $5 	   |
|  1   | Hex Nut               | McMaster-Carr 	       |   $5 	   |
|  1   | Support Beam  	       | Teche Lab 	       |    -      |
|  1   | Motor Mount 	       | Teche Lab             |    -      |
|  1   | Base Mount 	       | Teche Lab             |    -      |
|  1   | Drive Wheel 	       | Teche Lab             |    -      |
|  1   | Pen/Servo Mount       | Teche Lab             |    -      |
|  1   | Support Mount 	       | Teche Lab             |    -      |


#### Picture of Pen Plotter
![Pen Plotter](Images/PenPlotter.png)
###### Above is a picture of our Pen Plotter. A video demonstration of our pen plotter can be found using this link: https://youtu.be/GVp6Itpa4hw 
