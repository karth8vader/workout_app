import sqlite3

CREATE_EXERCISE_TABLE = """CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type_code TEXT
);"""

CREATE_WORKOUT_TABLE = """CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    exercises TEXT
);"""

CREATE_WORKOUT_HISTORY = """CREATE TABLE IF NOT EXISTS workout_history (
    id INTEGER PRIMARY KEY,
    timestamp REAL,
    workout_id INTEGER,
    FOREIGN KEY(workout_id) REFERENCES workouts(id)
);"""

CREATE_EXERCISE_HISTORY = """CREATE TABLE IF NOT EXISTS exercise_history (
    exercise_id INTEGER,
    workout_history_id INTEGER,
    repetitions INTEGER,
    weight REAL,
    duration REAL,
    FOREIGN KEY(exercise_id) REFERENCES exercises(id),
    FOREIGN KEY(workout_history_id) REFERENCES workout_history(id)
);"""

INSERT_EXERCISE = "INSERT INTO exercises (name, type_code) VALUES (?, ?);"
INSERT_WORKOUT = "INSERT INTO workouts (name, exercises) VALUES (?, ?);"
SELECT_ALL_EXERCISES = "SELECT * FROM exercises;"
SELECT_ALL_WORKOUTS = "SELECT * FROM workouts;"

connection = sqlite3.connect("data.db")


def create_tables():
    with connection:
        connection.execute(CREATE_EXERCISE_TABLE)
        connection.execute(CREATE_WORKOUT_TABLE)
        connection.execute(CREATE_WORKOUT_HISTORY)
        connection.execute(CREATE_EXERCISE_HISTORY)


def add_exercise(name: str, type_code: str):
    with connection:
        connection.execute(INSERT_EXERCISE, (name, type_code))


def get_exercises() -> list(list()):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL_EXERCISES)
        return cursor.fetchall()


def add_workout(name: str, exercises: str):
    with connection:
        connection.execute(INSERT_WORKOUT, (name, exercises))


def get_workouts() -> list(list()):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL_WORKOUTS)
        return cursor.fetchall()

