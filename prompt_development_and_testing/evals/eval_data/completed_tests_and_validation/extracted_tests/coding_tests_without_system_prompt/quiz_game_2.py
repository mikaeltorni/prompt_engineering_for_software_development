def run_quiz():
    # Dictionary containing questions and their corresponding answers
    quiz_questions = {
        "What is the capital of France?": {
            "options": ["A) London", "B) Berlin", "C) Paris", "D) Madrid"],
            "correct": "C"
        },
        "Which planet is known as the Red Planet?": {
            "options": ["A) Venus", "B) Mars", "C) Jupiter", "D) Saturn"],
            "correct": "B"
        },
        "What is the largest mammal in the world?": {
            "options": ["A) African Elephant", "B) Giraffe", "C) Blue Whale", "D) Polar Bear"],
            "correct": "C"
        },
        "Who painted the Mona Lisa?": {
            "options": ["A) Vincent van Gogh", "B) Pablo Picasso", "C) Leonardo da Vinci", "D) Michelangelo"],
            "correct": "C"
        },
        "What is the chemical symbol for gold?": {
            "options": ["A) Ag", "B) Fe", "C) Cu", "D) Au"],
            "correct": "D"
        }
    }

    score = 0
    total_questions = len(quiz_questions)

    print("\nWelcome to the Quiz Game!")
    print("------------------------")
    print("Instructions:")
    print("- Choose the correct answer by entering A, B, C, or D")
    print("- Each correct answer is worth 1 point")
    print(f"- There are {total_questions} questions in total\n")

    # Iterate through each question
    for question_num, (question, data) in enumerate(quiz_questions.items(), 1):
        print(f"\nQuestion {question_num}: {question}")
        
        # Display options
        for option in data["options"]:
            print(option)

        # Get user's answer
        while True:
            user_answer = input("\nYour answer (A/B/C/D): ").upper()
            if user_answer in ['A', 'B', 'C', 'D']:
                break
            print("Invalid input! Please enter A, B, C, or D.")

        # Check if answer is correct
        if user_answer == data["correct"]:
            print("Correct! ✓")
            score += 1
        else:
            print(f"Wrong! The correct answer was {data['correct']} ✗")

    # Display final results
    print("\n------------------------")
    print("Quiz Complete!")
    print(f"Your final score: {score}/{total_questions}")
    percentage = (score / total_questions) * 100
    print(f"Percentage: {percentage:.1f}%")

    # Provide feedback based on score
    if percentage == 100:
        print("Perfect score! Excellent work!")
    elif percentage >= 80:
        print("Great job!")
    elif percentage >= 60:
        print("Good effort!")
    else:
        print("Keep practicing!")

# Ask if user wants to play again
def play_again():
    while True:
        choice = input("\nWould you like to play again? (yes/no): ").lower()
        if choice in ['yes', 'no']:
            return choice == 'yes'
        print("Please enter 'yes' or 'no'")

# Main game loop
def main():
    while True:
        run_quiz()
        if not play_again():
            print("\nThanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()