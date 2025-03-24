"""
quiz_game.py

A multiple-choice quiz game that tracks user score and allows for replay.

Functions:
    display_question(question: dict) -> None: Displays a single question and its options
    validate_answer(user_input: str, valid_options: list) -> bool: Validates user input
    play_quiz() -> None: Main game function that runs the quiz
    calculate_percentage(score: int, total: int) -> float: Calculates score percentage

Command Line Usage Example:
    python quiz_game.py
"""

import random
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Quiz questions data
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["A) London", "B) Berlin", "C) Paris", "D) Madrid"],
        "correct_answer": "C"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A) Venus", "B) Mars", "C) Jupiter", "D) Saturn"],
        "correct_answer": "B"
    },
    {
        "question": "What is 2 + 2?",
        "options": ["A) 3", "B) 4", "C) 5", "D) 6"],
        "correct_answer": "B"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["A) Van Gogh", "B) Picasso", "C) Da Vinci", "D) Michelangelo"],
        "correct_answer": "C"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["A) African Elephant", "B) Blue Whale", "C) Giraffe", "D) Polar Bear"],
        "correct_answer": "B"
    }
]

def display_question(question: Dict[str, Any]) -> None:
    """
    Displays a question and its multiple choice options.

    Parameters:
        question (dict): Dictionary containing question data

    Returns:
        None
    """
    logger.debug(f"Displaying question: {question['question']}")
    print("\n" + question["question"])
    for option in question["options"]:
        print(option)

def validate_answer(user_input: str, valid_options: List[str]) -> bool:
    """
    Validates if the user input is among the valid options.

    Parameters:
        user_input (str): The user's input answer
        valid_options (list): List of valid answer options

    Returns:
        bool: True if input is valid, False otherwise
    """
    logger.debug(f"Validating input: {user_input}")
    return user_input.upper() in valid_options

def calculate_percentage(score: int, total: int) -> float:
    """
    Calculates the percentage score.

    Parameters:
        score (int): Number of correct answers
        total (int): Total number of questions

    Returns:
        float: Percentage score
    """
    logger.debug(f"Calculating percentage for score: {score}/{total}")
    return (score / total) * 100

def play_quiz() -> None:
    """
    Main function to run the quiz game.

    Parameters:
        None

    Returns:
        None
    """
    logger.info("Starting new quiz game")
    score = 0
    total_questions = len(QUIZ_QUESTIONS)
    
    # Create a copy of questions and shuffle them
    questions = QUIZ_QUESTIONS.copy()
    random.shuffle(questions)
    
    print("\nWelcome to the Quiz Game!")
    print("Answer each question by entering the letter (A, B, C, or D)")

    for question in questions:
        display_question(question)
        
        while True:
            answer = input("\nYour answer (or 'q' to quit): ").upper()
            logger.debug(f"User input: {answer}")
            
            if answer == 'Q':
                logger.info("User chose to quit the game")
                print("\nThanks for playing!")
                return
            
            if validate_answer(answer, ['A', 'B', 'C', 'D']):
                break
            else:
                print("Invalid input! Please enter A, B, C, or D.")
        
        if answer == question["correct_answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was {question['correct_answer']}")
        
        print(f"Current score: {score}/{total_questions}")
    
    # Calculate and display final score
    percentage = calculate_percentage(score, total_questions)
    logger.info(f"Quiz completed. Final score: {score}/{total_questions} ({percentage:.1f}%)")
    
    print(f"\nQuiz completed!")
    print(f"Final score: {score}/{total_questions}")
    print(f"Percentage: {percentage:.1f}%")

def main():
    """
    Main program loop.

    Parameters:
        None

    Returns:
        None
    """
    while True:
        play_quiz()
        
        while True:
            play_again = input("\nWould you like to play again? (y/n): ").lower()
            logger.debug(f"Play again input: {play_again}")
            
            if play_again in ['y', 'n']:
                break
            print("Please enter 'y' for yes or 'n' for no.")
        
        if play_again == 'n':
            logger.info("User chose to end the program")
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()