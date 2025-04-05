from controller import Controller
from dotenv import load_dotenv, find_dotenv
import asyncio

# Load the .env file (should be in the root of the repo)
load_dotenv("../")

async def main():
    controller: Controller = Controller(find_dotenv()) # Find the .env file and get the path back to it
    await controller.run()

if __name__ == "__main__":
    asyncio.run(main())