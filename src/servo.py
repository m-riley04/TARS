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

def main():
    logger.info("Starting servo testing...")

    # Create a servo controller instance
    controller = ServoController()

    if not controller.connected:
        logger.error("Failed to connect to PCA9685. Check your connections and try again.")
        return
    
    
    


if __name__ == "__main__":
    main()