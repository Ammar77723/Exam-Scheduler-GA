def hard_constraint1_all_courses(schedule, courses):
    exam_list = set()
    total_exams = 0

    for day in schedule.days:
        class_list = schedule.days[day]

        for _class in class_list:
            total_exams += 2
            exam_list.add(_class.morning)
            exam_list.add(_class.noon)

    exam_codes = {course[0] for course in courses}
    missing_exams = len(exam_codes - exam_list)

    satisfaction_ratio = 1 / (1 + missing_exams)
    constraint_satisfied = missing_exams == 0
    return satisfaction_ratio, constraint_satisfied

def hard_constraint2a_three_courses(course_allocation):      
    for student in course_allocation:
        if len(student.courses) < 3:                
            return False
    return True

def count_exam_occurrences(schedule):
    exam_counts_morning = {}
    exam_counts_noon = {}
    
    for classes_list in schedule.days.values():
        for _class in classes_list:
            exam_counts_morning[_class.morning] = exam_counts_morning.get(_class.morning, 0) + 1
            exam_counts_noon[_class.noon] = exam_counts_noon.get(_class.noon, 0) + 1
            
    return exam_counts_morning, exam_counts_noon
    
def hard_constraint2b_one_exam(schedule, course_allocation):
    exam_counts_morning, exam_counts_noon = count_exam_occurrences(schedule)
    clashes = 0
    student_names_clashes = set()
    
    for classes_list in schedule.days.values():
        morning_clashes = {}
        for _class in classes_list:
            if exam_counts_morning[_class.morning] > 1:
                morning_clashes[_class.morning] = morning_clashes.get(_class.morning, 0) + 1
        
        noon_clashes = {}
        for _class in classes_list:
            if exam_counts_noon[_class.noon] > 1:
                noon_clashes[_class.noon] = noon_clashes.get(_class.noon, 0) + 1
        
        for student in course_allocation:
            name = student.name
            course_list = student.courses
            
            for exam, count in morning_clashes.items():
                if count > 1 and exam in course_list and name not in student_names_clashes:
                    clashes += 1
                    student_names_clashes.add(name)
            
            for exam, count in noon_clashes.items():
                if count > 1 and exam in course_list and name not in student_names_clashes:
                    clashes += 1
                    student_names_clashes.add(name)

    constraint_satisfied = clashes == 0
    satisfaction_ratio = 1 / (1 + clashes) if clashes else 1

    return satisfaction_ratio, constraint_satisfied

def hard_constraint3_no_weekends(schedule):
    for day, classes_list in schedule.days.items():
        if day.lower() == 'saturday' or day.lower() == 'sunday':
            for _class in classes_list:
                if _class.morning or _class.noon:
                    return False 
    return True 

def hard_constraint5a_teacher_sametime(schedule):
    clashes = 0

    for day, classes_list in schedule.days.items():
        morning_teachers = []
        noon_teachers = []

        for _class in classes_list:
            morning_teachers.append(_class.invig_morning)
            noon_teachers.append(_class.invig_noon)

        morning_teacher_counts = {}
        noon_teacher_counts = {}

        for teacher in morning_teachers:
            morning_teacher_counts[teacher] = morning_teacher_counts.get(teacher, 0) + 1

        for teacher in noon_teachers:
            noon_teacher_counts[teacher] = noon_teacher_counts.get(teacher, 0) + 1

        for count in morning_teacher_counts.values():
            if count > 1:
                clashes += 1

        for count in noon_teacher_counts.values():
            if count > 1:
                clashes += 1

    constraint_satisfied = clashes == 0
    satisfaction_ratio = 1 / (1 + clashes) if clashes else 1

    return satisfaction_ratio, constraint_satisfied

def hard_constraint5b_teacher_row(schedule):
    consecutive = 0

    for day, classes_list in schedule.days.items():
        morning_teachers = [cls.invig_morning for cls in classes_list]
        noon_teachers = [cls.invig_noon for cls in classes_list]

        for teacher in morning_teachers:
            if teacher in noon_teachers:
                consecutive += 1

    constraint_satisfied = consecutive == 0
    satisfaction_ratio = 1 / (1 + consecutive) if consecutive else 1

    return satisfaction_ratio, constraint_satisfied

def hard_constraint6_repeated_rooms(schedule):
    violations = 0

    for day_schedule in schedule.days.values():
        day_rooms = []
        for _class in day_schedule:
            day_rooms.append(_class.room_name)
        
        if len(day_rooms) != len(set(day_rooms)):
            violations += 1
    
    return violations == 0

def soft_constraint2_no_consecutive_exams(schedule, course_allocation):
    consecutive_exams = 0

    for classes_list in schedule.days.values():
        for i in range(len(classes_list) - 1):
            current_class = classes_list[i]
            next_class = classes_list[i + 1]

            for student in course_allocation:
                if current_class in student.courses and next_class in student.courses:
                    consecutive_exams += 1

    constraint_satisfied = consecutive_exams == 0
    satisfaction_ratio = 1 / (1 + consecutive_exams) if consecutive_exams else 1

    return satisfaction_ratio, constraint_satisfied

def soft_constraint3_mg_before_cs(schedule, course_allocation):
    student_names = set()
    wrong_order = 0

    for student in course_allocation:
        mg_courses = [course for course in student.courses if 'MG' in course]
        cs_courses = [course for course in student.courses if 'CS' in course]

        if mg_courses and cs_courses:
            mg_exam_before_cs = False

            for day in schedule.days.values():
                exam_list = [cls.morning for cls in day] + [cls.noon for cls in day]

                mg_exam = any(course in exam_list for course in mg_courses)
                cs_exam = any(course in exam_list for course in cs_courses)

                if mg_exam and cs_exam:
                    mg_exam_before_cs = True
                    break

            if not mg_exam_before_cs:
                if student.name not in student_names:
                    student_names.add(student.name)
                    wrong_order += 1

    constraint_satisfied = wrong_order == 0
    satisfaction_ratio = 1 / (1 + wrong_order) if wrong_order else 1

    return satisfaction_ratio, constraint_satisfied

def constraints_satisfied_check(schedule, courses, course_allocation):
    hc1, hb1 = hard_constraint1_all_courses(schedule, courses)
    hb2a = hard_constraint2a_three_courses(course_allocation)
    hc2b, hb2b = hard_constraint2b_one_exam(schedule, course_allocation)
    hb3 = hard_constraint3_no_weekends(schedule)
    hc5a, hb5a = hard_constraint5a_teacher_sametime(schedule)
    hc5b, hb5b = hard_constraint5b_teacher_row(schedule)
    hb6 = hard_constraint6_repeated_rooms(schedule)
    
    sc2, sb2 = soft_constraint2_no_consecutive_exams(schedule, course_allocation)
    sc3, sb3 = soft_constraint3_mg_before_cs(schedule, course_allocation)
    if hb1 and hb2b and hb2a and hb3 and hb5a and hb5b and hb6:
        if sb2 or sb3:
            return True

    return False

def print_constraint_fulfillment(schedule, courses, course_allocation):
    hc1, hb1 = hard_constraint1_all_courses(schedule, courses)
    hb2a = hard_constraint2a_three_courses(course_allocation)
    hc2b, hb2b = hard_constraint2b_one_exam(schedule, course_allocation)
    hb3 = hard_constraint3_no_weekends(schedule)
    hc5a, hb5a = hard_constraint5a_teacher_sametime(schedule)
    hc5b, hb5b = hard_constraint5b_teacher_row(schedule)
    hb6 = hard_constraint6_repeated_rooms(schedule)
    
    sc2, sb2 = soft_constraint2_no_consecutive_exams(schedule, course_allocation)
    sc3, sb3 = soft_constraint3_mg_before_cs(schedule, course_allocation)
    
    metrics = f'''
Hard Constraints Fulfillment:
Hard Constraint 1 (All courses scheduled): {'Met' if hb1 else 'Not Met'}
Hard Constraint 2a (Three courses per student): {'Met' if hb2a else 'Not Met'}
Hard Constraint 2b (One exam for a student at a time): {'Met' if hb2b else 'Not Met'}
Hard Constraint 3 (No exams scheduled on weekends): {'Met' if hb3 else 'Not Met'}
Hard Constraint 5a (Teachers not invigilating at same time): {'Met' if hb5a else 'Not Met'}
Hard Constraint 5b (Teachers not invigilating two exams in a row): {'Met' if hb5b else 'Not Met'}
Hard Constraint 6 (No repeated rooms): {'Met' if hb6 else 'Not Met'}

Soft Constraints Fulfillment:
Soft Constraint 2 (No consecutive exams for students): {'Met' if sb2 else 'Not Met'}
Soft Constraint 3 (MG exams before afternoon exams for CS students): {'Met' if sb3 else 'Not Met'}
'''
    return metrics
