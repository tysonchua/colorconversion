import requests
import random
from colorama import Fore, init
init(autoreset=True)
API_URL = "https://official-joke-api.appspot.com/random_ten"
def get_jokes(times=4):
    jokes = []
    for _ in range(times):
        jokes.extend(requests.get(API_URL, timeout=10).json())
    return jokes
def show_jokes(joke):
    print(Fore.YELLOW + "\nCategory:", joke["type"])
    print(Fore.GREEN + "\nSetup:", joke["setup"])
    print(Fore.MAGENTA + "\nPunchline:", joke["punchline"])
    print(Fore.CYAN + "-" * 50)
def run():
    try:
        print(Fore.CYAN + "\n" + "=====================================")
        print(Fore.CYAN + "     Interactive Joke Generator      ")
        print(Fore.CYAN + "\n" + "=====================================")
        jokes = get_jokes()
        categories = sorted({j["type"] for j in jokes})
        while True:
            print(Fore.GREEN + "\nAvailable Categories\n")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            print("0. Exit")
            choice = input(Fore.YELLOW + "\nPlease choose a Category:") 
            if not choice.isdigit():
                print(Fore.RED + "Please choose a number.")
                continue
            choice = int(choice)
            if choice == 0:
                print(Fore.CYAN + "\n Thank you for using the Interactive Joke Generator!")
                break
            if choice > len(categories):
                print(Fore.RED + "Invalid Choice.")
                continue
            selected = categories[choice - 1]
            selected_jokes = [j for j in jokes if j["type"] == selected]
            show_jokes(random.choice(selected_jokes))
    except requests.exceptions.RequestException:
        print(Fore.RED + "Network Error. Please check your internet connection.")
if __name__ == "__main__":
    run()