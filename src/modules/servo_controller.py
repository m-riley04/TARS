import time
import sys
import logging
import math
from modules.helpers.servo_logic import ServoController
from modules.helpers.pid_logic import PID

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
        steps: Step count -- Alternates left and right stride
        direction: Forwards or Backwards
    """
    if not TARS.connected:
        logger.error("Not connected to PCA9685. Cannot perform walking sequence.")
        return
    
    logger.info("Starting walk sequence...")
    try:
        # Predefine
        start_pulse = TARS.mid
        down = 290 # 124~ deg
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

        if direction == 'forward':
            # Math to get left and right movements 
            end_pulse = TARS.max - TARS.half
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
                    TARS.move_servo_gradually(lh, end_pulse, start_pulse)
                    time.sleep(ts)
            logger.info(f"Walked {steps} steps forward")
        elif direction == 'backward':
            # Math to get left and right movements 
            end_pulse = TARS.min + TARS.half
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
        else:
            logger.info("Not a valid direction")
        
    except Exception as e:
        logger.error(f"Error during walk sequence: {e}")

def turn(TARS, angle:int, direction:str):
    """
    TARS turn function

    Args:
        TARS: ServoController instancwe
        angle: Turn Angle
        direction: Clockwise or Counterclockwise
    """
    if not TARS.connected:
        logger.error("Not connected to PCA9685. Cannot perform turning sequence.")
        return
    
    logger.info("Starting turn sequence...")

    try:
        """ Theory

        cry
        
        """


        cry = 'sadness'

    except Exception as e:
        logger.error(f"Error during turn sequence: {e}")

def run_declaration(TARS, distance:int, direction:str):
    """
    TARS run function w/ PID

    Args:
        TARS: ServoController instancwe
        distance: Distance
    """
    if not TARS.connected:
        logger.error("Not connected to PCA9685. Cannot perform turning sequence.")
        return
    
    logger.info("Starting run sequence...")

    try:
        """ Theory

        cry
        
        """
        base_stride_cm = 4.5  # Your estimated distance per step
        stride_adjustment_per_output = 0.05  # Scales how PID affects stride
        time_step = 0.2
        start_time = time.perf_counter()

        # Pulse range reference
        start_pulse = TARS.mid
        down = 206
        up = 600

        lv, lh, rv, rh = 0, 1, 2, 3

        # Set home
        TARS.set_servo_pulse(lv, down)
        TARS.set_servo_pulse(lh, start_pulse)
        TARS.set_servo_pulse(rv, down)
        TARS.set_servo_pulse(rh, start_pulse)
        time.sleep(time_step)

        # PID setup
        pid = PID(kp=0.05, ki=0.0001, kd=0.002)
        distance_walked = 0
        step = 0

        while distance_walked < distance:
            # Estimate current position
            output = pid.compute(distance, distance_walked, time_step)
            stride_modifier = 1 + (output * stride_adjustment_per_output)
            stride_modifier = max(0.8, min(1.5, stride_modifier))  # clamp

            # Convert to pulse movement
            max_stride_pulse = (TARS.max - TARS.half) if direction == 'forward' else (TARS.min + TARS.half)
            stride_pulse = int((max_stride_pulse - start_pulse) * stride_modifier + start_pulse)

            logger.info(f"S{step+1} | Dist: {distance_walked:.2f}cm | stride {stride_modifier:.2f} | output {output:.2f} | kp {pid.proportional:.2f} | ki {pid.integral:.2f} | kd {pid.derivative:.2f} | Time: {time.perf_counter()-start_time:.4f}sec")

            # Alternate left/right
            if step % 2 == 0:
                # Left step
                TARS.set_servo_pulse(lv, up)
                TARS.move_servo_gradually(lh, start_pulse, stride_pulse)
                time.sleep(time_step)

                TARS.set_servo_pulse(lv, down)
                TARS.set_servo_pulse(rv, up)
                TARS.move_servo_gradually(rh, start_pulse, stride_pulse)
                TARS.move_servo_gradually(lh, stride_pulse, start_pulse)
                time.sleep(time_step)

                TARS.set_servo_pulse(rh, down)
                TARS.move_servo_gradually(rh, stride_pulse, start_pulse)
                time.sleep(time_step)
            else:
                # Right step
                TARS.set_servo_pulse(rv, up)
                TARS.move_servo_gradually(rh, start_pulse, stride_pulse)
                time.sleep(time_step)

                TARS.set_servo_pulse(rv, down)
                TARS.set_servo_pulse(lv, up)
                TARS.move_servo_gradually(lh, start_pulse, stride_pulse)
                TARS.move_servo_gradually(rh, stride_pulse, start_pulse)
                time.sleep(time_step)

                TARS.set_servo_pulse(lh, down)
                TARS.move_servo_gradually(lh, stride_pulse, start_pulse)
                time.sleep(time_step)

            step += 1
            distance_walked += base_stride_cm * stride_modifier
        
        time_elapsed = time.perf_counter() - start_time
        logger.info(f"Finished walking ~{distance_walked:.2f}cm in {step} steps | Output: {output:.2f} | Elapsed time: {time_elapsed:.4f} seconds")

    except Exception as e:
        logger.error(f"Error during run sequence: {e}")


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
        logger.info("3. Run distance")
        logger.info("5. Exit")

        choice = input("> ")

        if choice == '1':
            try:
                step_count = int(input("How many steps? > "))
            except ValueError:
                print("Not an integer value...")
            walk(TARS, step_count, "forward")
        elif choice == '2':
            try:
                step_count = int(input("How many steps? > "))
            except ValueError:
                print("Not an integer value...")
            walk(TARS, step_count, "backward")
        elif choice == '3':
            try:
                distance = float(input("Target distance (cm) > "))
                direction = input("Direction (forward/backward) > ").strip()
                run_declaration(TARS, distance, direction)
            except ValueError:
                print("Invalid input.")
        elif choice == '5':
            logger.info("Exiting servo.py script")
            break
        else:
            logger.warning("Invalid choice. Please try again.")


    
if __name__ == "__main__":
    main()