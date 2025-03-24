"""
quiz_game.py

A multiple-choice quiz game that tracks user score and allows for replay.

Functions:
    display_question(question_data: dict) -> None
    get_valid_answer() -> str
    play_quiz() -> int
    display_results(score: int, total_questions: int) -> None
    main() -> None

Command Line Usage Example:
    python quiz_game.py
"""

import random
import logging
import time
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

# Quiz questions database
QUIZ_QUESTIONS: List[Dict] = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct": "C"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": "B"
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct": "B"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Van Gogh", "Da Vinci", "Picasso", "Rembrandt"],
        "correct": "B"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "correct": "B"
    }
]

def display_question(question_data: dict) -> None:
    """
    Displays a question and its multiple choice options.

    Parameters:
        question_data (dict): Dictionary containing question information

    Returns:
        None
    """
    logger.debug(f"Displaying question: {question_data['question']}")
    
    print("\n" + "="*50)
    print(question_data["question"])
    print("="*50)
    
    for i, option in enumerate(question_data["options"]):
        print(f"{chr(65+i)}. {option}")

def get_valid_answer() -> str:
    """
    Gets and validates user input for answer choice.

    Parameters:
        None

    Returns:
        str: Validated user answer (A, B, C, or D)
    """
    while True:
        answer = input("\nYour answer (A/B/C/D): ").strip().upper()
        logger.debug(f"User input: {answer}")
        
        if answer in ['A', 'B', 'C', 'D']:
            return answer
        else:
            logger.warning(f"Invalid input: {answer}")
            print("Invalid input! Please enter A, B, C, or D.")

def play_quiz() -> int:
    """
    Runs through all quiz questions and returns the final score.

    Parameters:
        None

    Returns:
        int: Final score
    """
    score = 0
    questions = QUIZ_QUESTIONS.copy()
    random.shuffle(questions)
    
    logger.info("Starting new quiz game")
    print("\nWelcome to the Quiz Game!")
    print("Answer the following multiple-choice questions.")
    
    for question in questions:
        display_question(question)
        user_answer = get_valid_answer()
        
        if user_answer == question["correct"]:
            print("Correct! ✓")
            score += 1
            logger.debug(f"Correct answer. Score: {score}")
        else:
            correct_option = question["options"][ord(question["correct"]) - 65]
            print(f"Wrong! The correct answer was: {correct_option} ✗")
            logger.debug(f"Wrong answer. Score remains: {score}")
        
        time.sleep(1)  # Brief pause between questions
    
    return score

def display_results(score: int, total_questions: int) -> None:
    """
    Displays the final quiz results.

    Parameters:
        score (int): Final score
        total_questions (int): Total number of questions

    Returns:
        None
    """
    logger.info(f"Game finished. Final score: {score}/{total_questions}")
    
    print("\n" + "="*50)
    print(f"Final Score: {score}/{total_questions}")
    percentage = (score / total_questions) * 100
    print(f"Percentage: {percentage:.1f}%")
    
    if percentage == 100:
        print("Perfect score! Excellent! 🏆")
    elif percentage >= 80:
        print("Great job! 🌟")
    elif percentage >= 60:
        print("Good effort! 👍")
    else:
        print("Keep practicing! 📚")
    print("="*50)

def main() -> None:
    """
    Main game loop that handles replay functionality.

    Parameters:
        None

    Returns:
        None
    """
    while True:
        score = play_quiz()
        display_results(score, len(QUIZ_QUESTIONS))
        
        while True:
            play_again = input("\nWould you like to play again? (yes/no): ").lower().strip()
            logger.debug(f"Play again response: {play_again}")
            
            if play_again in ['yes', 'no']:
                break
            print("Please enter 'yes' or 'no'.")
        
        if play_again == 'no':
            print("\nThanks for playing! Goodbye! 👋")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Game interrupted by user")
        print("\nGame interrupted. Goodbye! 👋")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print("\nAn unexpected error occurred. Please try again.")