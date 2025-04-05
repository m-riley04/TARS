#!/usr/bin/env python3
"""
Hardware Connection Tester for Adafruit PCA9685 Servo Controller

This script tests the connection to the Adafruit PCA9685 PWM controller board
connected to a Raspberry Pi via I2C. It helps diagnose common connection issues
and verifies that the hardware is properly set up.
"""

import sys
import time
import logging
import subprocess

# Configure logging
logger = logging.getLogger('hardware_tester')

def check_i2c_tools():
    """Check if i2c-tools is installed and install if needed."""
    try:
        subprocess.check_call(["which", "i2cdetect"])
        logger.info("i2c-tools is already installed")
        return True
    except subprocess.CalledProcessError:
        logger.warning("i2c-tools not found, attempting to install...")
        try:
            subprocess.check_call(["sudo", "apt-get", "update", "-y"])
            subprocess.check_call(["sudo", "apt-get", "install", "-y", "i2c-tools"])
            logger.info("i2c-tools installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install i2c-tools: {e}")
            return False

def check_i2c_enabled():
    """Check if I2C is enabled on the Raspberry Pi."""
    try:
        # Check if /dev/i2c-1 exists (or /dev/i2c-0 on older Pi models)
        for bus_num in [1, 0]:
            if subprocess.call(["ls", f"/dev/i2c-{bus_num}"], 
                              stdout=subprocess.DEVNULL, 
                              stderr=subprocess.DEVNULL) == 0:
                logger.info(f"I2C bus {bus_num} is available at /dev/i2c-{bus_num}")
                return True
        
        logger.error("I2C does not appear to be enabled on this Raspberry Pi")
        logger.info("To enable I2C, run 'sudo raspi-config', navigate to 'Interfacing Options' > 'I2C' and enable it")
        return False
    except Exception as e:
        logger.error(f"Error checking I2C status: {e}")
        return False

def scan_i2c_bus(bus_num=1):
    """Scan the I2C bus for connected devices."""
    try:
        logger.info(f"Scanning I2C bus {bus_num} for devices...")
        result = subprocess.run(["i2cdetect", "-y", str(bus_num)], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("I2C bus scan results:")
            print(result.stdout)
            
            # Check if 0x40 (default PCA9685 address) is present
            if "40" in result.stdout:
                logger.info("PCA9685 detected at address 0x40")
                return True
            else:
                logger.warning("PCA9685 not detected at default address (0x40)")
                logger.info("Check your connections and ensure the board is powered")
                return False
        else:
            logger.error(f"Failed to scan I2C bus: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error scanning I2C bus: {e}")
        return False

def check_adafruit_library():
    """Check if the Adafruit PCA9685 library is installed."""
    try:
        import Adafruit_PCA9685
        logger.info("Adafruit_PCA9685 library is installed")
        return True
    except ImportError:
        logger.warning("Adafruit_PCA9685 library not found, attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "adafruit-pca9685"])
            import Adafruit_PCA9685
            logger.info("Adafruit_PCA9685 library installed successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to install Adafruit_PCA9685 library: {e}")
            logger.info("To install manually, run: pip install adafruit-pca9685")
            return False

def test_pca9685_connection(bus_num=1):
    """Test connection to the PCA9685 by attempting to initialize it."""
    try:
        import Adafruit_PCA9685
        logger.info(f"Attempting to connect to PCA9685 on bus {bus_num}...")
        
        pwm = Adafruit_PCA9685.PCA9685(busnum=bus_num)
        pwm.set_pwm_freq(60)
        logger.info("Successfully connected to PCA9685!")
        
        # Test setting a PWM value
        logger.info("Testing PWM output on channel 0...")
        pwm.set_pwm(0, 0, 0)  # Turn off channel 0
        time.sleep(1)
        pwm.set_pwm(0, 0, 2048)  # Set channel 0 to 50% duty cycle
        time.sleep(1)
        pwm.set_pwm(0, 0, 4095)  # Set channel 0 to 100% duty cycle
        time.sleep(1)
        pwm.set_pwm(0, 0, 0)  # Turn off channel 0 again
        
        logger.info("PCA9685 test completed successfully")
        return True
    except FileNotFoundError as e:
        logger.error(f"I2C device not found. Ensure that /dev/i2c-{bus_num} exists. Details: {e}")
        return False
    except Exception as e:
        logger.error(f"Error testing PCA9685 connection: {e}")
        return False

def run_hardware_tests():
    """Run all hardware tests."""
    logger.info("Starting hardware tests for Adafruit PCA9685 Servo Controller")
    
    # Check if i2c-tools is installed
    if not check_i2c_tools():
        logger.error("Failed to install i2c-tools. Some tests may not work.")
    
    # Check if I2C is enabled
    if not check_i2c_enabled():
        logger.error("I2C is not enabled. Please enable it and try again.")
        return False
    
    # Scan I2C bus for devices
    if not scan_i2c_bus():
        logger.warning("PCA9685 not detected on I2C bus. Check connections and power.")
    
    # Check if Adafruit library is installed
    if not check_adafruit_library():
        logger.error("Adafruit_PCA9685 library not installed. Please install it and try again.")
        return False
    
    # Test connection to PCA9685
    if not test_pca9685_connection():
        logger.error("Failed to connect to PCA9685. Check hardware connections.")
        return False
    
    logger.info("All hardware tests completed successfully!")
    return True

if __name__ == "__main__":
    run_hardware_tests()
