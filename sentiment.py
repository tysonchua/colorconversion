from transformers import pipeline
from colorama import Fore, Style, init
init(autoreset=True)
classifier = pipeline(
    task = "sentiment-analysis",
    model = "distilbert-base-uncased-finetuned-sst-2-english"
)
total_count = 0
positive = 0
negative = 0
print(Fore.CYAN + Style.BRIGHT + "\nAI Sentiment Analysis System")
print(Fore.CYAN + "-" * 35)
print(Fore.YELLOW + "Enter any sentence to analyze sentiment")
print(Fore.YELLOW + "Enter 'exit' to terminate the system")
print(Fore.GREEN + "- " * 18)
while True:
    user_input = input(Fore.GREEN + "Input text: \n").strip()
    if user_input.lower() == "exit":
        print(Fore.CYAN + Style.BRIGHT + "SESSION SUMMARY")
        print(Fore.CYAN + "-" * 35)
        print(Fore.YELLOW + f"Total inputs: {total_count}")
        print(Fore.GREEN + f"Positive inputs: {positive}")
        print(Fore.RED + f"Negative inputs: {negative}")
        break
    if not user_input:
        print(Fore.RED + "Input cannot be empty.")
        continue
    result = classifier(user_input)[0]
    label = result["label"]
    confidence = round(result["score"] * 100, 2)
    if confidence >= 85:
        strength = "Strong"
    elif confidence >= 65:
        strength = "Moderate"
    else:
        strength = "Weak"
    total_count += 1
    if label == "POSITIVE":
        positive += 1
        color = Fore.GREEN
    else:
        negative += 1
        color = Fore.RED

    print(color + Style.BRIGHT + "ANALYSIS RESULTS")
    print(color + "-" * 35)
    print(color + f"Sentiment: {label}")
    print(color + f"Strength level: {strength}")
    print(color + f"Confidence: {confidence}%")