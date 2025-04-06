from .modules.tars import TARS
import asyncio, dotenv, logging

async def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] [%(asctime)s] %(name)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger('main')
    logger.info("Starting main...")
    
    # Load the .env file (should be in the root of the repo)
    dotenv.load_dotenv("../")
    
    tars: TARS = TARS(dotenv.find_dotenv()) # Find the .env file and get the path back to it
    await tars.run()

if __name__ == "__main__":
    asyncio.run(main())