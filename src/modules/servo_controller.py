import time
import sys
import logging
from helpers.servo_logic import ServoController

# Configure logging
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
logger = logging.getLogger('servo')

#########################################################################

def walk(TARS, steps:int, direction:str):
    """
    TARS walk function

    Args:
        TARS: ServoController instance
    """
    if not TARS.connected:
        logger.error("Not connected to PCA9685. Cannot perform walking sequence.")
        return
    
    logger.info("Starting walk sequence...")
    try:
        # Set all servos to neutral position
        TARS.set_servo_pulse(0, TARS.neutral_pulse)
        TARS.set_servo_pulse(1, TARS.neutral_pulse)
        TARS.set_servo_pulse(2, TARS.neutral_pulse)
        TARS.set_servo_pulse(3, TARS.neutral_pulse)
            # Ideally: 0,2 are up down -- 1,3 are movement 
            # 0,1 are left
            # 2,3 are right

        time.sleep(0.5)

        """ Theory
        To walk:
        1st step:
            Move left leg up
        Move left leg + 45 deg
            Move left leg down
        wait 0.1
            Move right leg up
        Move right leg + 45 deg + Move left leg 0 deg
            Move right leg down
        wait 0.1

        2nd step:
            Move right leg up
        Move right leg + 45 deg
            Move right leg down
        wait 0.1
            Move left leg up
        move left leg + 45 deg
            Move left leg 
        wait 0.1
        """

        ts = 0.5 # Time asleep

        if direction == 'fwd':
            # Math to get left and right movements 
            start_pulse = TARS.neutral_pulse
            end_pulse = TARS.max_pulse - TARS.half
            home = TARS.min_pulse + TARS.half - 10 # 154
            target = 600 # 0

            for i in range(steps):
                if i % 2 != 0:
                    # Left side operation
                    TARS.move_servo_gradually(1, start_pulse, end_pulse)
                    time.sleep(ts)
                    TARS.move_servo_gradually(1, end_pulse, start_pulse)
                    TARS.move_servo_gradually(3, start_pulse, end_pulse)
                    time.sleep(ts)
                    TARS.move_servo_gradually(3, end_pulse, start_pulse)

                else:
                    # Right side operation
                    TARS.move_servo_gradually(3, start_pulse, end_pulse)
                    time.sleep(ts)
                    TARS.move_servo_gradually(3, end_pulse, start_pulse)
                    TARS.move_servo_gradually(1, start_pulse, end_pulse)
                    time.sleep(ts)
                    TARS.move_servo_gradually(1, end_pulse, start_pulse)

            logger.info(f"Walked {steps} steps forward")
        elif direction == 'bkwd':
            logger.info("Not implemented yet...")
            logger.info(f"Walked {steps} steps forward")
        else:
            logger.info("Not a valid direction")
        
    except Exception as e:
        logger.error(f"Error during walk sequence: {e}")







#########################################################################

def main():
    logger.info("\n")
    logger.info("Starting servo testing...")

    # Create a servo controller instance
    TARS = ServoController()

    if not TARS.connected:
        logger.error("Failed to connect to PCA9685. Check your connections and try again.")
        return
    
    # Display menu?
    while True:
        logger.info("\n\n")
        logger.info("Select an option:")
        logger.info("1. Walk forward")
        logger.info("2. Walk backward")
        logger.info("5. Exit")

        choice = input("> ")

        if choice == '1':
            try:
                step_count = int(input("How many steps? > "))
            except ValueError:
                print("Not an integer value...")
            walk(TARS, step_count, "fwd")
        elif choice == '2':
            try:
                step_count = int(input("How many steps? > "))
            except ValueError:
                print("Not an integer value...")
            walk(TARS, step_count, "bkwd")
        elif choice == '5':
            logger.info("Exiting servo.py script")
            break
        else:
            logger.warning("Invalid choice. Please try again.")


    
if __name__ == "__main__":
    main()