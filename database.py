import sqlite3
from datetime import datetime

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
INSERT_WORKOUT_HISTORY = "INSERT INTO workout_history (timestamp, workout_id) VALUES (?, ?);"
INSERT_EXERCISE_HISTORY = """INSERT INTO exercise_history (
    exercise_id, workout_history_id, repetitions, weight, duration) 
    VALUES (?, ?, ?, ?, ?);"""
SELECT_ALL_EXERCISES = "SELECT * FROM exercises;"
SELECT_ALL_WORKOUTS = "SELECT * FROM workouts;"
SELECT_EXERCISE_LIST = "SELECT exercises FROM workouts WHERE id = ?;"
SELECT_EXERCISE = "SELECT name, type_code FROM exercises WHERE id = ?;"
SELECT_EXERCISE_HISTORY = "SELECT * FROM exercise_history WHERE exercise_id = ?;"
SELECT_WORKOUT_HISTORY_TIMESTAMP = "SELECT timestamp FROM workout_history WHERE id = ?;"

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


def get_exercises() -> list[list]:
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL_EXERCISES)
        return cursor.fetchall()


def add_workout(name: str, exercises: str):
    with connection:
        connection.execute(INSERT_WORKOUT, (name, exercises))


def get_workouts() -> list[list]:
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL_WORKOUTS)
        return cursor.fetchall()


def get_exercise_list(workout_id: int) -> list[int]:
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_EXERCISE_LIST, (workout_id,))
        return cursor.fetchone()[0].split(',')


def log_workout(workout_id: int) -> int:
    with connection:
        now = datetime.now().timestamp()
        cursor = connection.cursor()
        cursor.execute(INSERT_WORKOUT_HISTORY, (now, workout_id))
        return cursor.lastrowid


def get_exercise(exercise_id: int) -> tuple[str, str]:
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_EXERCISE, (exercise_id,))
        result = cursor.fetchone()
        return result[0], result[1]


def log_exercise(exercise_id: int, workout_history_id: int, repetitions: int, weight: float, duration: float):
    with connection:
        connection.execute(INSERT_EXERCISE_HISTORY, (exercise_id, workout_history_id, repetitions, weight, duration))


def get_exercise_history(exercise_id: int) -> list[list]:
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_EXERCISE_HISTORY, (exercise_id,))
        return cursor.fetchall()


def get_workout_timestamp(workout_history_id) -> float:
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WORKOUT_HISTORY_TIMESTAMP, (workout_history_id,))
        return cursor.fetchone()[0]
