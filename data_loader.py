import pandas as pd
import random
from models import add_student

def is_course_in_list(courses, code):
    for course in courses:
        if code == course[0]:
            return True
    return False

def preprocess_allocations(previous_allocations_df):
    previous_allocations_df['Student Name'] = previous_allocations_df['Student Name'].str.strip()
    previous_allocations_df['Course Code'] = previous_allocations_df['Course Code'].str.strip()
    previous_allocations_df.drop_duplicates(inplace=True)
    return previous_allocations_df

def allocate_courses(courses_df, previous_allocations_df):
    previous_allocations_df = preprocess_allocations(previous_allocations_df)
    allocated_courses = set(zip(previous_allocations_df['Student Name'], previous_allocations_df['Course Code']))
    course_count = previous_allocations_df.groupby('Student Name').size()
    available_courses = list(courses_df['Course Code'].unique())
    eligible_students = course_count[course_count < 3]
    new_allocations = [] 
    
    for student_name, num_courses_taken in eligible_students.items():
        num_courses_to_add = 3 - num_courses_taken
        if num_courses_to_add > 0:
            available_unique_courses = [course for course in available_courses if (student_name, course) not in allocated_courses]
            if available_unique_courses:
                courses_to_add = random.sample(available_unique_courses, min(num_courses_to_add, len(available_unique_courses)))
                new_allocations.extend([(student_name, course) for course in courses_to_add])
                
    new_allocations_df = pd.DataFrame(new_allocations, columns=['Student Name', 'Course Code'])
    return pd.concat([previous_allocations_df, new_allocations_df])

def load_data():
    courses = []
    courses_df = pd.read_csv("Dataset/courses.csv")
    courses = list(courses_df.itertuples(index=False, name=None))

    student_list = []
    student_course_df = pd.read_csv("Dataset/studentCourse.csv")
    student_course_df.drop_duplicates(inplace=True)

    student_counts = student_course_df['Student Name'].value_counts()
    valid_students = student_counts[student_counts >= 3].index
    filtered_df = student_course_df[student_course_df['Student Name'].isin(valid_students)]

    for index, row in filtered_df.iterrows():
        name = row['Student Name']
        cc = row['Course Code']
        add_student(student_list, name, cc)
        
    teachers_df = pd.read_csv("Dataset/teachers.csv")
    teacher = teachers_df['Names'].tolist()
 
    return courses, teacher, student_list
