#!/usr/bin/env python3
"""
Example script demonstrating how to use the ServoController class
to control multiple servos in a coordinated sequence.

This script shows how to create more complex movements by combining
basic servo operations from the ServoController class.
"""

import time
import sys
import logging
from ..modules.servo_controller import ServoController

# Configure logging
logger = logging.getLogger('servo_example')

def wave_sequence(controller):
    """
    Perform a waving sequence using multiple servos.
    
    Args:
        controller: ServoController instance
    """
    if not controller.connected:
        logger.error("Not connected to PCA9685. Cannot perform wave sequence.")
        return
    
    logger.info("Starting wave sequence...")
    
    try:
        # Set all servos to neutral position
        controller.set_servo_pulse(0, controller.neutral_pulse)  # Center servo
        controller.set_servo_pulse(1, controller.neutral_pulse)  # Left servo
        controller.set_servo_pulse(2, controller.neutral_pulse)  # Right servo
        time.sleep(1)
        
        # Wave sequence - repeat 3 times
        for _ in range(3):
            # Move left servo up
            controller.set_servo_pulse(1, controller.min_pulse + 50)
            time.sleep(0.5)
            
            # Move left servo down
            controller.set_servo_pulse(1, controller.max_pulse - 50)
            time.sleep(0.5)
        
        # Return to neutral position
        controller.set_servo_pulse(0, controller.neutral_pulse)
        controller.set_servo_pulse(1, controller.neutral_pulse)
        controller.set_servo_pulse(2, controller.neutral_pulse)
        
        logger.info("Wave sequence completed")
    
    except Exception as e:
        logger.error(f"Error during wave sequence: {e}")

def move_servo_gradually(controller, channel, start_pulse, end_pulse, steps=20, delay=0.05):
    """
    Move a servo from one position to another gradually.
    
    Args:
        controller: ServoController instance
        channel: Servo channel number
        start_pulse: Starting pulse width
        end_pulse: Ending pulse width
        steps: Number of steps to take
        delay: Delay between steps in seconds
    """
    if not controller.connected:
        logger.error("Not connected to PCA9685. Cannot move servo gradually.")
        return
    
    logger.info(f"Moving servo {channel} gradually from {start_pulse} to {end_pulse}...")
    
    try:
        step_size = (end_pulse - start_pulse) / steps
        current_pulse = start_pulse
        
        for i in range(steps + 1):
            pulse = int(start_pulse + i * step_size)
            controller.set_servo_pulse(channel, pulse)
            time.sleep(delay)
        
        logger.info(f"Gradual movement of servo {channel} completed")
    
    except Exception as e:
        logger.error(f"Error during gradual servo movement: {e}")

def synchronized_movement(controller):
    """
    Perform synchronized movement of multiple servos.
    
    Args:
        controller: ServoController instance
    """
    if not controller.connected:
        logger.error("Not connected to PCA9685. Cannot perform synchronized movement.")
        return
    
    logger.info("Starting synchronized movement sequence...")
    
    try:
        # Set initial positions
        controller.set_servo_pulse(0, controller.neutral_pulse)  # Center servo
        controller.set_servo_pulse(1, controller.neutral_pulse)  # Left servo
        controller.set_servo_pulse(2, controller.neutral_pulse)  # Right servo
        time.sleep(1)
        
        # Move all servos simultaneously to one extreme
        controller.set_servo_pulse(0, controller.min_pulse + 50)
        controller.set_servo_pulse(1, controller.min_pulse + 50)
        controller.set_servo_pulse(2, controller.min_pulse + 50)
        time.sleep(1)
        
        # Move all servos simultaneously to the other extreme
        controller.set_servo_pulse(0, controller.max_pulse - 50)
        controller.set_servo_pulse(1, controller.max_pulse - 50)
        controller.set_servo_pulse(2, controller.max_pulse - 50)
        time.sleep(1)
        
        # Return to neutral position
        controller.set_servo_pulse(0, controller.neutral_pulse)
        controller.set_servo_pulse(1, controller.neutral_pulse)
        controller.set_servo_pulse(2, controller.neutral_pulse)
        
        logger.info("Synchronized movement sequence completed")
    
    except Exception as e:
        logger.error(f"Error during synchronized movement: {e}")

def demo_sequence(controller):
    """
    Run a demonstration sequence showing various servo movements.
    
    Args:
        controller: ServoController instance
    """
    if not controller.connected:
        logger.error("Not connected to PCA9685. Cannot run demo sequence.")
        return
    
    logger.info("Starting demo sequence...")
    
    try:
        # 1. Set all servos to neutral position
        logger.info("1. Setting all servos to neutral position")
        controller.set_servo_pulse(0, controller.neutral_pulse)
        controller.set_servo_pulse(1, controller.neutral_pulse)
        controller.set_servo_pulse(2, controller.neutral_pulse)
        time.sleep(2)
        
        # 2. Gradual movement of center servo
        logger.info("2. Gradual movement of center servo")
        move_servo_gradually(controller, 0, controller.neutral_pulse, controller.min_pulse + 50)
        time.sleep(1)
        move_servo_gradually(controller, 0, controller.min_pulse + 50, controller.max_pulse - 50)
        time.sleep(1)
        move_servo_gradually(controller, 0, controller.max_pulse - 50, controller.neutral_pulse)
        time.sleep(1)
        
        # 3. Wave sequence
        logger.info("3. Wave sequence")
        wave_sequence(controller)
        time.sleep(1)
        
        # 4. Synchronized movement
        logger.info("4. Synchronized movement")
        synchronized_movement(controller)
        time.sleep(1)
        
        # 5. Return to neutral position
        logger.info("5. Returning to neutral position")
        controller.set_servo_pulse(0, controller.neutral_pulse)
        controller.set_servo_pulse(1, controller.neutral_pulse)
        controller.set_servo_pulse(2, controller.neutral_pulse)
        
        logger.info("Demo sequence completed")
    
    except Exception as e:
        logger.error(f"Error during demo sequence: {e}")

def main():
    """Main function to run the example script."""
    logger.info("Starting servo example script")
    
    # Create a servo controller instance
    controller = ServoController()
    
    if not controller.connected:
        logger.error("Failed to connect to PCA9685. Check your connections and try again.")
        return
    
    # Display menu
    while True:
        logger.info("\nSelect an option:")
        logger.info("1. Wave sequence")
        logger.info("2. Gradual servo movement")
        logger.info("3. Synchronized movement")
        logger.info("4. Run full demo sequence")
        logger.info("5. Exit")
        
        choice = input("> ")
        
        if choice == '1':
            wave_sequence(controller)
        elif choice == '2':
            channel = int(input("Enter channel number (0-15): "))
            start = int(input("Enter start pulse width: "))
            end = int(input("Enter end pulse width: "))
            steps = int(input("Enter number of steps: "))
            move_servo_gradually(controller, channel, start, end, steps)
        elif choice == '3':
            synchronized_movement(controller)
        elif choice == '4':
            demo_sequence(controller)
        elif choice == '5':
            logger.info("Exiting servo example script")
            break
        else:
            logger.warning("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
