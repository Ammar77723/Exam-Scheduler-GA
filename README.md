# Exam Schedule Generator using Genetic Algorithm

This project implements an AI-based exam scheduling and timetable generation system using Genetic Algorithms. It reads data related to courses, students, and teachers, and attempts to find an optimal schedule respecting various hard and soft constraints.

## Features
Applies Genetic Algorithm (crossover, mutation, parent selection, fitness evaluation) to optimize the timetable.
Respects Hard Constraints:
- All exams must be scheduled.
- One exam per student at a time.
- Teachers cannot invigilate two exams at the exact same time.
- No exams scheduled on weekends.
- No repeated classrooms at the same time.

Evaluates Soft Constraints:
- Avoid consecutive exams for students.
- Preferred exam order for specific subjects (e.g. MG before CS).

## Directory Structure
- `main.py` - The main executable script.
- `models.py` - Contains the primary data shapes (Classes, Students, Schedule).
- `data_loader.py` - Functions to load models from CSVs.
- `constraints.py` - Hard and Soft constraints implementation logic.
- `genetic_algorithm.py` - Core evolutionary logic for the schedule algorithm.
- `config.py` - Global configuration.
- `utils.py` - Exporting to CSV and printing tables.
- `Dataset/` - Directory containing CSV files: `courses.csv`, `teachers.csv`, `studentCourse.csv`.

## Requirements
- Python 3.x
- pandas
- numpy

## Running the Code
Simply run the script:
```bash
python main.py
```
The program will output the generations and constraint satisfaction progress, and save the result in `Dataset/result.csv`.
