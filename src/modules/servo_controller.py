#!/usr/bin/env python3
"""
Servo Controller for Raspberry Pi with Adafruit PCA9685

This module provides a comprehensive set of functions to control servos using the 
Adafruit PCA9685 PWM controller board connected to a Raspberry Pi via I2C.
Based on the TARS-AI project implementation.

Features:
- Basic servo control (position, pulse width)
- Auto-calibration for finding min, max, and neutral positions
- Multi-servo control for synchronized movements
- Error handling for hardware connection issues
"""

from __future__ import division
import time
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('servo_controller')

# Try to import the Adafruit PCA9685 library
try:
    import Adafruit_PCA9685
except ImportError:
    logger.error("Adafruit_PCA9685 library not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "adafruit-pca9685"])
    import Adafruit_PCA9685
    logger.info("Adafruit_PCA9685 library installed successfully")

class ServoController:
    """
    A class to control servos using the Adafruit PCA9685 PWM controller.
    """
    
    def __init__(self, busnum=1, address=0x40, frequency=60):
        """
        Initialize the servo controller.
        
        Args:
            busnum (int): I2C bus number (default: 1 for Raspberry Pi 3, 4)
            address (int): I2C address of the PCA9685 (default: 0x40)
            frequency (int): PWM frequency in Hz (default: 60Hz for most servos)
        """
        self.busnum = busnum
        self.address = address
        self.frequency = frequency
        self.pwm = None
        self.connected = False
        
        # Default pulse width range
        self.min_pulse = 0
        self.max_pulse = 600
        self.neutral_pulse = 300
        
        # Connect to the PCA9685
        self.connect()
    
    def connect(self):
        """
        Connect to the PCA9685 controller.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.pwm = Adafruit_PCA9685.PCA9685(busnum=self.busnum, address=self.address)
            self.pwm.set_pwm_freq(self.frequency)
            self.connected = True
            logger.info(f"Connected to PCA9685 on bus {self.busnum}, address 0x{self.address:02X}")
            return True
        except FileNotFoundError as e:
            logger.error(f"I2C device not found. Ensure that /dev/i2c-{self.busnum} exists. Details: {e}")
            self.connected = False
            return False
        except Exception as e:
            logger.error(f"Unexpected error during PCA9685 initialization: {e}")
            self.connected = False
            return False
    
    def set_servo_pulse(self, channel, pulse):
        """
        Set a servo to a specific pulse width.
        
        Args:
            channel (int): Channel number (0-15)
            pulse (int): Pulse width (typically between 150-600)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected:
            logger.warning("Not connected to PCA9685. Cannot set servo pulse.")
            return False
            
        if not self.min_pulse <= pulse <= self.max_pulse:
            logger.warning(f"Pulse out of range ({self.min_pulse}-{self.max_pulse}): {pulse}")
            return False
            
        try:
            self.pwm.set_pwm(channel, 0, pulse)
            logger.debug(f"Set servo on channel {channel} to pulse {pulse}")
            return True
        except Exception as e:
            logger.error(f"Error setting servo pulse: {e}")
            return False
    
    def set_servo_angle(self, channel, angle):
        """
        Set a servo to a specific angle.
        
        Args:
            channel (int): Channel number (0-15)
            angle (float): Angle in degrees (0-180)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not 0 <= angle <= 180:
            logger.warning(f"Angle out of range (0-180): {angle}")
            return False
            
        # Convert angle to pulse width
        pulse = int(self.min_pulse + (self.max_pulse - self.min_pulse) * angle / 180)
        return self.set_servo_pulse(channel, pulse)
    
    def auto_calibrate_servo(self, channel, is_center_servo=False):
        """
        Automatically calibrate a servo to find min, max, and neutral positions.
        
        Args:
            channel (int): Channel number (0-15)
            is_center_servo (bool): Whether this is a center servo with additional height values
            
        Returns:
            dict: Dictionary containing calibration values
        """
        if not self.connected:
            logger.warning("Not connected to PCA9685. Cannot calibrate servo.")
            return None
            
        logger.info(f"Starting auto-calibration for servo on channel {channel}...")
        
        # Find minimum PWM value using a curved approach
        step = 150  # Initial large step
        pwm_value = self.max_pulse  # Start at the high end
        min_pulse = None
        
        logger.info("Finding minimum PWM value...")
        while step >= 1:
            logger.info(f"Testing PWM: {pwm_value}")
            self.set_servo_pulse(channel, pwm_value)
            time.sleep(0.5)
            
            user_input = input(f"Did the servo start moving? (y/n): ").strip().lower()
            if user_input == "y":
                min_pulse = pwm_value
                pwm_value -= step
            else:
                pwm_value += step
            
            step //= 2
        
        if min_pulse is None:
            logger.error("Failed to find minimum PWM value.")
            return None
            
        logger.info(f"Servo starts moving at PWM: {min_pulse}")
        
        # Find maximum PWM value
        step = 50
        pwm_value = min_pulse  # Start from the found minimum value
        max_pulse = None
        
        logger.info("Finding maximum PWM value...")
        while step >= 1:
            logger.info(f"Testing PWM: {pwm_value}")
            self.set_servo_pulse(channel, pwm_value)
            time.sleep(0.5)
            
            user_input = input(f"Did the servo stop moving? (y/n): ").strip().lower()
            if user_input == "y":
                max_pulse = pwm_value
                pwm_value -= step
            else:
                pwm_value += step
            
            step //= 2
        
        if max_pulse is None:
            logger.error("Failed to find maximum PWM value.")
            return None
            
        logger.info(f"Servo stops moving at PWM: {max_pulse}")
        
        # Calculate neutral position
        neutral_pulse = (min_pulse + max_pulse) // 2
        logger.info(f"Setting servo to neutral position: {neutral_pulse}")
        self.set_servo_pulse(channel, neutral_pulse)
        
        # Store calibration values
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.neutral_pulse = neutral_pulse
        
        calibration = {
            "min_pulse": min_pulse,
            "max_pulse": max_pulse,
            "neutral_pulse": neutral_pulse
        }
        
        # Additional calculations for center servo
        if is_center_servo:
            down_height = abs(min_pulse - max_pulse) // 2
            up_height = min_pulse
            neutral_height = (down_height + up_height) // 2
            
            calibration.update({
                "up_height": up_height,
                "neutral_height": neutral_height,
                "down_height": down_height
            })
            
            logger.info(f"Calibration complete for center servo {channel}:")
            logger.info(f"  Up Height: {up_height}")
            logger.info(f"  Neutral Height: {neutral_height}")
            logger.info(f"  Down Height: {down_height}")
        else:
            logger.info(f"Calibration complete for servo {channel}:")
            
        logger.info(f"  Back Port: {min_pulse}")
        logger.info(f"  Neutral Port: {neutral_pulse}")
        logger.info(f"  Forward Port: {max_pulse}")
        
        return calibration
    
    def set_all_servos_preset(self):
        """
        Set all servos to preset positions.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected:
            logger.warning("Not connected to PCA9685. Cannot set servo presets.")
            return False
            
        try:
            # Example preset pulse values for different servos
            self.set_servo_pulse(0, 128)  # Example preset pulse for servo 0
            self.set_servo_pulse(1, 350)  # Example preset pulse for servo 1
            self.set_servo_pulse(2, 350)  # Example preset pulse for servo 2
            logger.info("All servos set to preset positions")
            return True
        except Exception as e:
            logger.error(f"Error setting servo presets: {e}")
            return False
    
    def set_single_servo(self, channel):
        """
        Interactively set a single servo to a user-specified pulse width.
        
        Args:
            channel (int): Channel number (0-15)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connected:
            logger.warning("Not connected to PCA9685. Cannot set servo.")
            return False
            
        while True:
            try:
                pulse_input = input(f"Enter pulse width for servo {channel} ({self.min_pulse}-{self.max_pulse}): ")
                pulse = int(pulse_input)
                
                if self.min_pulse <= pulse <= self.max_pulse:
                    result = self.set_servo_pulse(channel, pulse)
                    logger.info(f"Set servo on channel {channel} to pulse {pulse}")
                    break  # Exit the loop after a valid pulse is entered
                else:
                    logger.warning(f"Pulse out of range ({self.min_pulse}-{self.max_pulse}): {pulse}")
            except ValueError:
                logger.error("Invalid input. Please enter a number.")
        
        return True
    
    def servo_control_menu(self):
        """
        Display an interactive menu for controlling servos.
        """
        if not self.connected:
            logger.warning("Not connected to PCA9685. Cannot display servo control menu.")
            return
            
        logger.info("Servo Control Menu (Pulse Width)")
        
        while True:
            logger.info("\nSelect an option:")
            logger.info("1. Set all servos to preset pulse widths")
            logger.info("2. Manually set servo 0 pulse width")
            logger.info("3. Manually set servo 1 pulse width")
            logger.info("4. Manually set servo 2 pulse width")
            logger.info("5. Manually set servo 15 pulse width")
            logger.info("6. Auto-calibrate servo")
            logger.info("7. Exit")
            
            choice = input("> ")
            
            if choice == '1':
                self.set_all_servos_preset()
            elif choice == '2':
                self.set_single_servo(0)
            elif choice == '3':
                self.set_single_servo(1)
            elif choice == '4':
                self.set_single_servo(2)
            elif choice == '5':
                self.set_single_servo(15)
            elif choice == '6':
                channel = int(input("Enter channel number (0-15): "))
                is_center = input("Is this a center servo? (y/n): ").lower() == 'y'
                self.auto_calibrate_servo(channel, is_center)
            elif choice == '7':
                logger.info("Exiting servo control menu")
                break
            else:
                logger.warning("Invalid choice. Please try again.")

# Example usage
if __name__ == "__main__":
    # Create a servo controller instance
    controller = ServoController()
    
    if controller.connected:
        # Display the servo control menu
        controller.servo_control_menu()
    else:
        logger.error("Failed to connect to PCA9685. Check your connections and try again.")
