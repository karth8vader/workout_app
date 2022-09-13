import database

MENU_PROMPT = """
1. Add an exercise
2. View exercises
3. Create a workout
4. View workouts
5. Start a workout
6. Exit

Your selection: """


def prompt_add_exercise():
    name = input("Enter exercise name: ")
    type_code = input("Enter type code: ")
    database.add_exercise(name, type_code)


def main() -> None:
    print("Welcome to the workout app")
    database.create_tables()

    while (user_input := input(MENU_PROMPT)) != '6':
        if user_input == '1':
            prompt_add_exercise()
        elif user_input == '2':
            exercises = database.get_exercises()
            for exercise in exercises:
                print(f"Name: {exercise[1]} Type: {exercise[2]}")


if __name__ == "__main__":
    main()
