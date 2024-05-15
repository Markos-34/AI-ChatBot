import json
from difflib import get_close_matches

import requests

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, date: dict):
    with open(file_path, 'w') as file:
        json.dump(date, file, indent=2)
        

def fetch_trivia_questions(amount: int, category: int, difficulty: str) -> list:
    url = "https://opentdb.com/api.php?amount=50&category=18&difficulty=medium"
    params = {
        "amount": amount,
        "category": category,
        "difficulty": difficulty
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print("Failed to fetch trivia questions.")
        return []
        
        
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_anwer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        
        
def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    
    while True:
        user_input: str = input('You: ')
        
        if user_input.lower() == 'quit':
            break
        
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        
        if best_match:
            answer: str = get_anwer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
            
        else:
            print('Bot: I don\'t know the answer. Let me fetch a trivia question for you.')
            trivia_questions = fetch_trivia_questions(amount=1, category=18, difficulty="medium")
            if trivia_questions:
                new_question = trivia_questions[0]["question"]
                print(f'Bot: Here\'s a trivia question for you: {new_question}')
                new_answer = input('Type the answer or "skip" to skip: ')
                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": new_question, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print('Bot: Thank you! I learned a new response!')

                
                
if __name__ == '__main__':
    chat_bot()
            