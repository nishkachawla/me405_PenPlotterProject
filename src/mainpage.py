## @file mainpage.py
# @author Nishka Chawla
# @author Ronan Shaffer
# @mainpage
#
# @section ss_software Software Design
# Below is a proposed task diagram and state transition diagrams for our teams pen plotter machine. 
# 
#
#
# @subsection ss_taskdiagram Task Diagram 
# \image html Task_Diagram.png "Task Diagram" width=750cm
# This is a task diagram for our pen plotter. The eack motor task runs its own motor driver, 
# encoder driver, and controller.
# A calibration flags will be shared between the tasks to start plotting only after both 
# motors have been calibrated.
#
#
#
# @subsection ss_fsm1 Motor 1 State Transition Diagram
# \image html Motor_1_FSM.png "Motor 1 Finite State Machine" width=750cm 
# Our State Transition Diagram for Motor 1 has a calibration state, a wait state, and a run state. 
# When the Motor 1 task is run, the FSM starts in the calibration state to zero the position of the motor 
# using the hall effect sensor. Once the hall effect sensor flag is true, the FSM moves to the wait state to 
# wait for the Motor 2 to finish calibrating before moving to the run state to begin plotting. Once in the 
# run state, the motor 1 task runs until the plotting is completed. 
#
#
#
# @subsection ss_fsm2 Motor 2 State Transition Diagram
# \image html Motor_2_FSM.png "Motor 2 Finite State Machine" width=750cm
# Our State Transition Diagram for Motor 2 is very similar to motor 1 as it has a calibration state, a wait state, 
# and a run state. When the Motor 2 task is run, the FSM starts in the calibration state to zero the position of 
# the motor using the limit switch. Once the limit switch flag is true, the FSM moves to the wait state to 
# wait for the Motor 1 to finish calibrating before moving to the run state to begin plotting. Once in the 
# run state, the motor 2 task runs until the plotting is completed. 


