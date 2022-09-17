import database
import matplotlib.pyplot as plt

MENU_PROMPT = """
1. Add an exercise
2. View exercises
3. Create a workout
4. View workouts
5. Start a workout
6. View exercise history
7. Exit

Your selection: """
TYPE_CODE_PROMPT = """Choose exercise type:
    1. Repetitions
    2. Weight and repetitions
    3. Duration
    4. Weight and duration
Choice: """
type_code_dict = {
	'1': 'r__',
	'2': 'rw_',
	'3': '__d',
	'4': '_wd',
	'r__': 'Repetitions',
	'rw_': 'Weight and repetitions',
	'__d': 'Duration',
	'_wd': 'Weight and duration'
}


def prompt_add_exercise():
	name = input("Enter exercise name: ")

	type_code = input(TYPE_CODE_PROMPT)
	type_code = type_code_dict[type_code]
	database.add_exercise(name, type_code)


def print_exercise_list():
	exercises = database.get_exercises()
	for exercise in exercises:
		print(f"#{exercise[0]:3} Name: {exercise[1]:20} Type: {type_code_dict[exercise[2]]}")


def prompt_add_workout():
	print("Choose exercises to add to workout, press x to finish.")
	print_exercise_list()
	exercise_list = ""
	while (user_input := input("Choose exercise #: ")) != 'x':
		exercise_list = exercise_list + user_input + ','
	exercise_list = exercise_list[:-1]

	database.add_workout(input("Enter workout name: "), exercise_list)


def print_workout_list():
	workouts = database.get_workouts()
	exercises = database.get_exercises()
	exercise_dict = {}
	for exercise in exercises:
		exercise_dict[exercise[0]] = exercise[1]

	for workout in workouts:
		exercise_list = workout[2].split(',')
		print(f"#{workout[0]:3} Name: {workout[1]:20} Exercises: ", end="")
		exercise_str = ""
		for exercise in exercise_list:
			exercise_str = exercise_str + exercise_dict[int(exercise)] + ", "
		exercise_str = exercise_str[:-2]
		print(exercise_str)


def select_workout():
	# select a workout from the list
	print_workout_list()
	choice = int(input("Workout choice: "))
	exercise_ids = database.get_exercise_list(choice)
	# log workout in history table
	workout_id = database.log_workout(choice)
	for exercise_id in exercise_ids:
		name, type_code = database.get_exercise(exercise_id)
		print(name)
		if type_code == 'r__':
			repetitions = int(input("# of repetitions: "))
			database.log_exercise(exercise_id, workout_id, repetitions, 0.0, 0.0)
		elif type_code == 'rw_':
			repetitions = int(input("# of repetitions: "))
			weight = float(input("Weight: "))
			database.log_exercise(exercise_id, workout_id, repetitions, weight, 0.0)
		elif type_code == '__d':
			duration = float(input('Duration: '))
			database.log_exercise(exercise_id, workout_id, 0, 0.0, duration)
		elif type_code == '_wd':
			duration = float(input('Duration: '))
			weight = float(input("Weight: "))
			database.log_exercise(exercise_id, workout_id, 0, weight, duration)


def view_exercise_history():
	print_exercise_list()
	exercise_id = int(input("Choice: "))
	exercise_history = database.get_exercise_history(exercise_id)
	name, type_code = database.get_exercise(exercise_id)
	workout_totals = {}
	if type_code == 'r__':
		for exercise in exercise_history:
			if exercise[1] not in workout_totals:
				workout_totals[exercise[1]] = 0
			workout_totals[exercise[1]] += exercise[2]
	elif type_code == 'rw_':
		for exercise in exercise_history:
			if exercise[1] not in workout_totals:
				workout_totals[exercise[1]] = 0
			workout_totals[exercise[1]] += exercise[2] * exercise[3]
	elif type_code == '__d':
		for exercise in exercise_history:
			if exercise[1] not in workout_totals:
				workout_totals[exercise[1]] = 0
			workout_totals[exercise[1]] += exercise[4]
	elif type_code == '_wd':
		for exercise in exercise_history:
			if exercise[1] not in workout_totals:
				workout_totals[exercise[1]] = 0
			workout_totals[exercise[1]] += exercise[4] * exercise[3]

	x = []
	y = []
	for key in workout_totals:
		x.append(database.get_workout_timestamp(key))
		y.append(workout_totals[key])
	plt.title(f"Total volume per workout: {name}")
	plt.plot(x, y, '-o')
	plt.show()


def main() -> None:
	print("Welcome to the workout app")
	database.create_tables()
	user_input_dict = {
		'1': prompt_add_exercise,
		'2': print_exercise_list,
		'3': prompt_add_workout,
		'4': print_workout_list,
		'5': select_workout,
		'6': view_exercise_history
	}
	while (user_input := input(MENU_PROMPT)) != '7':
		user_input_dict[user_input]()


if __name__ == "__main__":
	main()
