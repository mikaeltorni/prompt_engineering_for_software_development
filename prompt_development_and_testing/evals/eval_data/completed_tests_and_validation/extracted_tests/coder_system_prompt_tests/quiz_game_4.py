"""
quiz_game.py

A multiple-choice quiz game that tracks user score and allows for replay.

Functions:
    display_welcome(): Displays welcome message
    get_valid_input(valid_choices: list) -> str: Gets and validates user input
    present_question(question: dict, question_num: int) -> bool: Presents a question and checks answer
    run_quiz(questions: list) -> int: Runs the complete quiz
    play_game() -> None: Main game loop

Command Line Usage Example:
    python quiz_game.py
"""

import random
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

# Quiz questions and answers
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
        "choices": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
        "correct_answer": "Leonardo da Vinci"
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

def get_valid_input(valid_choices: List[str]) -> str:
    """
    Gets and validates user input against a list of valid choices.

    Parameters:
        valid_choices (List[str]): List of valid input choices

    Returns:
        str: Validated user input
    """
    logger.debug(f"Valid choices: {valid_choices}")
    
    while True:
        user_input = input("Your answer (enter the letter): ").upper()
        if user_input in valid_choices:
            logger.debug(f"Valid input received: {user_input}")
            return user_input
        logger.warning(f"Invalid input received: {user_input}")
        print(f"Invalid input! Please enter one of: {', '.join(valid_choices)}")

def present_question(question: Dict, question_num: int) -> bool:
    """
    Presents a question to the user and checks if the answer is correct.

    Parameters:
        question (Dict): Dictionary containing question data
        question_num (int): Current question number

    Returns:
        bool: True if answer is correct, False otherwise
    """
    logger.debug(f"Presenting question {question_num}")
    
    print(f"\nQuestion {question_num}:")
    print(question["question"])
    
    # Create answer choices mapping
    choices = question["choices"]
    choice_letters = ['A', 'B', 'C', 'D']
    
    # Display choices
    for letter, choice in zip(choice_letters, choices):
        print(f"{letter}. {choice}")
    
    # Get user's answer
    user_answer = get_valid_input(choice_letters)
    selected_answer = choices[choice_letters.index(user_answer)]
    
    is_correct = selected_answer == question["correct_answer"]
    logger.debug(f"Answer correct: {is_correct}")
    
    # Display result
    if is_correct:
        print("Correct! ✓")
    else:
        print(f"Wrong! The correct answer was: {question['correct_answer']} ✗")
    
    return is_correct

def run_quiz(questions: List[Dict]) -> int:
    """
    Runs the complete quiz and returns the final score.

    Parameters:
        questions (List[Dict]): List of question dictionaries

    Returns:
        int: Final score
    """
    logger.debug("Starting quiz")
    
    score = 0
    total_questions = len(questions)
    
    # Shuffle questions
    random.shuffle(questions)
    
    # Present each question
    for i, question in enumerate(questions, 1):
        if present_question(question, i):
            score += 1
    
    logger.debug(f"Quiz completed. Final score: {score}/{total_questions}")
    return score

def play_game() -> None:
    """
    Main game loop that handles the complete game flow.

    Parameters:
        None

    Returns:
        None
    """
    logger.debug("Starting game")
    
    while True:
        display_welcome()
        
        # Run the quiz
        score = run_quiz(QUIZ_QUESTIONS)
        total_questions = len(QUIZ_QUESTIONS)
        
        # Display final score
        print(f"\nFinal Score: {score}/{total_questions}")
        percentage = (score / total_questions) * 100
        print(f"Percentage: {percentage:.1f}%")
        
        # Ask to play again
        play_again = input("\nWould you like to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    play_game()