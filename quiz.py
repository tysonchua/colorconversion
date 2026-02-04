import html
import colorama
import requests
import random
from colorama import Fore, init
init(autoreset=True)
def getData():
    url = "https://www.opentdb.com/api.php?amount=1&type=multiple"
    res = requests.get(url)
    data = res.json()
    if data["response_code"] != 0:
        return None
    q = data["results"][0]
    questions = html.unescape(q["question"])
    correct = html.unescape(q["correct_answer"])
    incorrect = [html.unescape(i) for i in (q["incorrect_answers"])]
    options = incorrect + [correct]
    random.shuffle(options)
    labels = ["A", "B", "C", "D"]
    mapped = dict(zip(labels, options))
    return questions, correct, mapped
def askQuestion():
    data = getData()
    if not data:
        print(Fore.RED + "Unable to fetch questions.")
        return False
    question, correct, mapped = data
    print(Fore.CYAN + "\n" + question)
    for label, text in mapped.items():
        print(Fore.CYAN + f"{label}. {text}")
    choice = input(Fore.GREEN + "Your answer (A-D): ").upper().strip()
    if choice in mapped:
        if mapped[choice] == correct:
            print(Fore.BLUE + "Correct!\n")
            return True
        print(Fore.RED + "Incorrect. Correct Answer: " + correct)
        return False
    print(Fore.RED + "Invalid choice.\n")
    return False
def startQuiz():
    score = 0
    total = 10
    print(Fore.MAGENTA + "\n(:--- Quiz Game! ---:) \n")
    for _ in range(total):
        if askQuestion():
            score += 1
    print(Fore.MAGENTA + f"Final Score: {score}/{total}\n")
startQuiz()