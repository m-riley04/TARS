from controller import Controller
from dotenv import load_dotenv, find_dotenv

# Load the .env file (should be in the root of the repo)
load_dotenv("../")

def main():
    controller: Controller = Controller(find_dotenv())
    controller.run()

if __name__ == "__main__":
    main()