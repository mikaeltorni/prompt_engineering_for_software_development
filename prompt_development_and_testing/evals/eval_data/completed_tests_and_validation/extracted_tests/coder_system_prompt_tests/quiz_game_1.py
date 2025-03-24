"""
quiz_game.py

A multiple-choice quiz game that tracks user score and allows for replay.

Functions:
    display_welcome(): Displays welcome message
    present_question(question_data: dict) -> bool: Presents a single question and returns if correct
    play_quiz(questions: list) -> int: Runs the complete quiz and returns final score
    get_valid_input(valid_choices: list) -> str: Gets and validates user input
    display_final_score(score: int, total: int) -> None: Displays the final score

Command Line Usage Example:
    python quiz_game.py
"""

import random
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

# Quiz questions database
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "choices": ["London", "Berlin", "Paris", "Madrid"],
        "correct_answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "choices": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct_answer": "Mars"
    },
    {
        "question": "What is the largest mammal in the world?",
        "choices": ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "correct_answer": "Blue Whale"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "choices": ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Michelangelo"],
        "correct_answer": "Leonardo da Vinci"
    },
    {
        "question": "What is the chemical symbol for gold?",
        "choices": ["Ag", "Fe", "Au", "Cu"],
        "correct_answer": "Au"
    }
]

def display_welcome() -> None:
    """
    Displays the welcome message for the quiz game.

    Parameters:
        None

    Returns:
        None
    """
    logger.debug("Displaying welcome message")
    print("\n=== Welcome to the Quiz Game! ===")
    print("Answer the following multiple-choice questions.\n")
    time.sleep(1)

def get_valid_input(valid_choices: list) -> str:
    """
    Gets and validates user input against a list of valid choices.

    Parameters:
        valid_choices (list): List of valid input choices

    Returns:
        str: Valid user input
    """
    logger.debug(f"Valid choices: {valid_choices}")
    
    while True:
        user_input = input("Your answer (enter the letter): ").upper()
        if user_input in valid_choices:
            logger.debug(f"Valid input received: {user_input}")
            return user_input
        logger.warning(f"Invalid input received: {user_input}")
        print(f"Invalid input! Please enter one of: {', '.join(valid_choices)}")

def present_question(question_data: dict) -> bool:
    """
    Presents a single question to the user and checks the answer.

    Parameters:
        question_data (dict): Dictionary containing question, choices, and correct answer

    Returns:
        bool: True if answer is correct, False otherwise
    """
    logger.debug(f"Presenting question: {question_data['question']}")
    
    print("\n" + question_data["question"])
    choices = question_data["choices"]
    correct_answer = question_data["correct_answer"]
    
    # Create answer mapping (A, B, C, D)
    answer_mapping = {chr(65+i): choice for i, choice in enumerate(choices)}
    
    # Display choices
    for letter, choice in answer_mapping.items():
        print(f"{letter}) {choice}")
    
    # Get user's answer
    user_answer = get_valid_input(list(answer_mapping.keys()))
    selected_answer = answer_mapping[user_answer]
    
    is_correct = selected_answer == correct_answer
    logger.debug(f"Answer correct: {is_correct}")
    
    # Display result
    if is_correct:
        print("\n✓ Correct!")
    else:
        print(f"\n✗ Wrong! The correct answer was: {correct_answer}")
    
    time.sleep(1)
    return is_correct

def play_quiz(questions: list) -> int:
    """
    Runs the complete quiz game.

    Parameters:
        questions (list): List of question dictionaries

    Returns:
        int: Final score
    """
    logger.debug("Starting new quiz game")
    
    score = 0
    total_questions = len(questions)
    
    # Shuffle questions for variety
    random.shuffle(questions)
    
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i} of {total_questions}")
        if present_question(question):
            score += 1
    
    logger.debug(f"Quiz completed. Final score: {score}/{total_questions}")
    return score

def display_final_score(score: int, total: int) -> None:
    """
    Displays the final score and a corresponding message.

    Parameters:
        score (int): Number of correct answers
        total (int): Total number of questions

    Returns:
        None
    """
    logger.debug(f"Displaying final score: {score}/{total}")
    
    percentage = (score / total) * 100
    print("\n=== Quiz Complete! ===")
    print(f"Your final score: {score}/{total} ({percentage:.1f}%)")
    
    if percentage == 100:
        print("Perfect score! Excellent work! 🏆")
    elif percentage >= 80:
        print("Great job! 👏")
    elif percentage >= 60:
        print("Good effort! 👍")
    else:
        print("Keep practicing! 💪")

def main():
    """
    Main game loop.

    Parameters:
        None

    Returns:
        None
    """
    while True:
        display_welcome()
        score = play_quiz(QUIZ_QUESTIONS)
        display_final_score(score, len(QUIZ_QUESTIONS))
        
        # Ask to play again
        print("\nWould you like to play again?")
        play_again = get_valid_input(['Y', 'N'])
        
        if play_again == 'N':
            print("\nThanks for playing! Goodbye! 👋")
            break

if __name__ == "__main__":
    main()