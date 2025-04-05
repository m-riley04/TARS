import time
import sys
import logging
from modules.servo_controller import ServoController

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
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
        # This is just to test 1 servo -- for now
        # Set all servos to neutral position
        TARS.set_servo_pulse(0, TARS.neutral_pulse)
        #TARS.set_servo_pulse(1, TARS.neutral_pulse)
        #TARS.set_servo_pulse(2, TARS.neutral_pulse)
        #TARS.set_servo_pulse(3, TARS.neutral_pulse)
            # Ideally: 0,2 are up down -- 1,3 are movement 
            # 0,1 are left
            # 2,3 are right
        time.sleep(1)

        """ Theory
        To walk:
        1st step:
            Move left leg up
        Move left leg + 45 deg
            Move left leg down
        wait 0.1
            Move right leg up
        Move right leg + 45 deg
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
            for i in range(steps):
                if i % 2 != 0:
                    # Left side operation
                    TARS.set_servo_pulse(1, TARS.max_pulse - 150)
                    time.sleep(ts)
                    TARS.set_servo_pulse(3, TARS.max_pulse - 150)
                    time.sleep(ts)
                else:
                    # Right side operation
                    TARS.set_servo_pulse(3, TARS.max_pulse - 150)
                    time.sleep(ts)
                    TARS.set_servo_pulse(1, TARS.max_pulse - 150)
                    time.sleep(ts)
        elif direction == 'bkwd':
            for i in range(steps):
                if i % 2 != 0:
                    # Left side operation
                    TARS.set_servo_pulse(1, TARS.min_pulse + 150)
                    time.sleep(ts)
                    TARS.set_servo_pulse(3, TARS.min_pulse + 150)
                    time.sleep(ts)
                else:
                    # Right side operation
                    TARS.set_servo_pulse(3, TARS.min_pulse + 150)
                    time.sleep(ts)
                    TARS.set_servo_pulse(1, TARS.min_pulse + 150)
                    time.sleep(ts)
        else:
            logger.info("Not a valid direction")


        
    except Exception as e:
        logger.error(f"Error during walk sequence: {e}")







#########################################################################

def main():
    logger.info("Starting servo testing...")

    # Create a servo controller instance
    TARS = ServoController()

    if not TARS.connected:
        logger.error("Failed to connect to PCA9685. Check your connections and try again.")
        return
    
    # Display menu?
    while True:
        logger.info("\nSelect an option:")
        logger.info("1. Walk forward")
        logger.info("2. Walk backward")

        choice = input("> ")

        if choice == '1':
            walk(TARS, 1, "fwd")
        elif choice == '2':
            walk(TARS, 1, "bkwd")
        else:
            logger.warning("Invalid choice. Please try again.")


    


if __name__ == "__main__":
    main()