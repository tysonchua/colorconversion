import sys
import joblib
import re
import numpy as np
from colorama import Fore, Style, init
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

TRAINING_DATA = [
    # Complaint
    ("the service was extremely slow", "Complaint"),
    ("customer support did not respond", "Complaint"),
    ("this app keeps crashing", "Complaint"),
    ("delivery was delayed again", "Complaint"),
    ("very disappointed with the performance", "Complaint"),
    ("system freezes frequently", "Complaint"),
    ("too many bugs in the application", "Complaint"),
    ("this update broke everything", "Complaint"),
    ("poor response from support team", "Complaint"),
    ("this experience is frustrating", "Complaint"),
    ("application is unstable after update", "Complaint"),
    ("facing frequent downtime", "Complaint"),
    ("service quality has degraded", "Complaint"),
    ("not happy with the recent changes", "Complaint"),
    ("nothing works as expected", "Complaint"),
    ("continuous errors are annoying", "Complaint"),
    ("support is unprofessional", "Complaint"),
    ("this feature does not work", "Complaint"),
    ("very poor performance overall", "Complaint"),
    ("completely dissatisfied with the service", "Complaint"),

    # Query
    ("how do i reset my password", "Query"),
    ("what are the pricing plans", "Query"),
    ("how can i upgrade my subscription", "Query"),
    ("where can i download invoices", "Query"),
    ("is offline mode available", "Query"),
    ("how long does verification take", "Query"),
    ("can i change my email address", "Query"),
    ("where is account settings located", "Query"),
    ("how do i contact customer support", "Query"),
    ("can you explain this feature", "Query"),
    ("what payment methods are supported", "Query"),
    ("how to enable notifications", "Query"),
    ("can i schedule a call", "Query"),
    ("is there a free trial", "Query"),
    ("how to cancel my plan", "Query"),
    ("can i get usage reports", "Query"),
    ("where can i update profile details", "Query"),
    ("how does billing work", "Query"),
    ("what is the refund policy", "Query"),
    ("is technical documentation available", "Query"),

    # Feedback
    ("design looks very modern", "Feedback"),
    ("performance has improved a lot", "Feedback"),
    ("interface is smooth and clean", "Feedback"),
    ("user experience feels better", "Feedback"),
    ("navigation is intuitive", "Feedback"),
    ("features are easy to find", "Feedback"),
    ("workflow is very logical", "Feedback"),
    ("application feels stable now", "Feedback"),
    ("loading speed is impressive", "Feedback"),
    ("overall experience is pleasant", "Feedback"),
    ("nice improvement in performance", "Feedback"),
    ("this update made things better", "Feedback"),
    ("interface design is excellent", "Feedback"),
    ("response time has improved", "Feedback"),
    ("app is much faster now", "Feedback"),
    ("everything feels more polished", "Feedback"),
    ("the layout is well structured", "Feedback"),
    ("system feels optimized", "Feedback"),
    ("very smooth user journey", "Feedback"),
    ("great overall enhancement", "Feedback"),

    # Appreciation
    ("thank you for the quick help", "Appreciation"),
    ("excellent customer support", "Appreciation"),
    ("great service from the team", "Appreciation"),
    ("i appreciate your assistance", "Appreciation"),
    ("very satisfied with the support", "Appreciation"),
    ("thanks for resolving my issue", "Appreciation"),
    ("wonderful service experience", "Appreciation"),
    ("outstanding response time", "Appreciation"),
    ("support team was very helpful", "Appreciation"),
    ("keep up the great work", "Appreciation"),
    ("many thanks for your guidance", "Appreciation"),
    ("really appreciate your effort", "Appreciation"),
    ("excellent follow up", "Appreciation"),
    ("great job on this update", "Appreciation"),
    ("very grateful for the help", "Appreciation"),
    ("impressed by the service quality", "Appreciation"),
    ("thank you for your patience", "Appreciation"),
    ("fantastic experience overall", "Appreciation"),
    ("superb customer service", "Appreciation"),
    ("highly appreciate the support", "Appreciation"),

    # General Conversation
    ("hello there", "General_Conversation"),
    ("good morning", "General_Conversation"),
    ("hope you are doing well", "General_Conversation"),
    ("nice talking to you", "General_Conversation"),
    ("how is everything going", "General_Conversation"),
    ("let us discuss later", "General_Conversation"),
    ("just checking in", "General_Conversation"),
    ("that sounds interesting", "General_Conversation"),
    ("looking forward to it", "General_Conversation"),
    ("let me know your thoughts", "General_Conversation"),
    ("hope to hear from you soon", "General_Conversation"),
    ("good evening", "General_Conversation"),
    ("have a great day", "General_Conversation"),
    ("pleased to meet you", "General_Conversation"),
    ("wish you all the best", "General_Conversation"),
    ("talk to you later", "General_Conversation"),
    ("enjoy your day", "General_Conversation"),
    ("take care", "General_Conversation"),
    ("nice chatting with you", "General_Conversation"),
    ("catch up soon", "General_Conversation")
]

def build_pipeline():
    return Pipeline([
        ("tfidf", 
        TfidfVectorizer(
            ngram_range=(1,3),
            max_features = 6000,
            sublinear_tf=True,
            stop_words="english"
        )),
        ("clf", MultinomialNB(alpha=1.0))
    ])
    

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[a-z\s]", "", text)
    return text.strip()

def train_model():
    texts = [clean_text(x[0]) for x in TRAINING_DATA]
    labels = [x[1] for x in TRAINING_DATA]
    pipeline = build_pipeline()
    pipeline.fit(texts, labels)
    joblib.dump(pipeline,"intent_classifier.pkl")

def load_model():
    try:
        return joblib.load("intent_classifier.pkl")
    except:
        print(Fore.YELLOW + "Training optimized NLP model")
        train_model()
        return load_model()
def analyze(text,model):
    cleaned = clean_text(text)
    probs = model.predict_proba([cleaned])[0]
    idx = np.argmax(probs)
    return model.classes_[idx], round(probs[idx] * 100, 2)
def main():
    print(Fore.CYAN + Style.BRIGHT + "\nADVANCED TEXT INTENT CLASSIFIER")
    print(Fore.CYAN + "-" * 60)
    print(Fore.YELLOW + "Enterprise-grade NLP Classification system")
    print(Fore.YELLOW + "Type 'exit' to close")
    model = load_model()
    while True:
        text = input(Fore.WHITE + "Input Text: " ).strip()
        if text.lower() == "exit":
            print(Fore.CYAN + "\nSystem terminated successfully.")
            sys.exit()
        if not text:
            print(Fore.RED + "Input cannot be empty.\n")
            continue
        label, confidence = analyze(text,model)
        print(Fore.GREEN + Style.BRIGHT + "\nClassification Results")
        print(Fore.GREEN + "-" * 60)
        print(f"Predicated Label: {label}")
        print(f"Confidence: {confidence}")
if __name__ == "__main__":
    main()