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
        # Predefine
        start_pulse = TARS.mid
        end_pulse = TARS.max - TARS.half
        down = 206 # 154 deg
        up = 600 # 0
        ts = 0.75 # Time asleep -- need to tune later to make faster
    
        # Set all servos to neutral position
        # Ideally: 0,2 are up down -- 1,3 are movement 
            # 0,1 are left
            # 2,3 are right

        lv = 0
        lh = 1
        rv = 2
        rh = 3

        # Set Servos to Home
        TARS.set_servo_pulse(lv, down)
        TARS.set_servo_pulse(lh, start_pulse)
        TARS.set_servo_pulse(rv, down)
        TARS.set_servo_pulse(rh, start_pulse)

        time.sleep(ts)

        """ Theory
        To walk:
        1st step:
            Move left leg up
        Move left leg + 45 deg
        wait 0.1
            Move left leg down
            Move right leg up
        Move right leg + 45 deg + Move left leg 0 deg
        wait 0.1
            Move right leg down
        Move right leg 0 deg
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

        if direction == 'fwd':
            # Math to get left and right movements 
            for i in range(steps):
                if i % 2 != 0:
                    # Left side operation
                    TARS.set_servo_pulse(lv, up)
                    TARS.move_servo_gradually(lh, start_pulse, end_pulse)
                    time.sleep(ts)

                    TARS.set_servo_pulse(lv, down)
                    TARS.set_servo_pulse(rv, up)
                    TARS.move_servo_gradually(rh, start_pulse, end_pulse)
                    TARS.move_servo_gradually(lh, end_pulse, start_pulse)
                    time.sleep(ts)

                    TARS.set_servo_pulse(rh, down)
                    TARS.move_servo_gradually(rh, end_pulse, start_pulse)
                    time.sleep(ts)

                else:
                    # Right side operation
                    TARS.set_servo_pulse(rv, up)
                    TARS.move_servo_gradually(rh, start_pulse, end_pulse)
                    time.sleep(ts)

                    TARS.set_servo_pulse(rv, down)
                    TARS.set_servo_pulse(lv, up)
                    TARS.move_servo_gradually(lh, start_pulse, end_pulse)
                    TARS.move_servo_gradually(rh, end_pulse, start_pulse)
                    time.sleep(ts)

                    TARS.set_servo_pulse(lh, down)
                    TARS.move_servo_gradually(lv, end_pulse, start_pulse)
                    time.sleep(ts)
            logger.info(f"Walked {steps} steps forward")
        elif direction == 'bkwd':
            end_pulse = TARS.min + TARS.half
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