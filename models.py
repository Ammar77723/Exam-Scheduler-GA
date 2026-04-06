from config import total_days

class Classrooms_Class:
    def __init__(self, room_name, morning, invig_morning, noon, invig_noon):
        self.room_name = room_name
        self.morning = morning
        self.invig_morning = invig_morning
        self.noon = noon
        self.invig_noon = invig_noon
        
    def __repr__(self):
        morning_paper = self.morning.ljust(6)
        m_invigilator = self.invig_morning.ljust(18)
        noon_paper = self.noon.ljust(6)
        n_invigilator = self.invig_noon.ljust(18)

        return f"{self.room_name.ljust(10)} {morning_paper} {m_invigilator} {noon_paper} {n_invigilator}"

class StudentData:
    def __init__(self, name, courses):
        self.name = name
        self.courses = []
        self.courses.append(courses)

    def add_course(self, course):
        self.courses.append(course)

    def __repr__(self):                                               
        output = "Name: " + self.name + " ---- " + "Courses: " + str(self.courses) + "\n"
        return output
    
def add_student(student_list, name, course):                              
    for student in student_list:
        if student.name == name:
            if course not in student.courses:                              
                student.add_course(course)
            return

    new_student = StudentData(name, course)
    student_list.append(new_student)

class Schedule1:
    def __init__(self, days=None, fitness=0):
        if days is None:
            self.days = {}
        else:
            self.days = days
        self.fitness = fitness

        for day in total_days:
            if day not in self.days:
                self.days[day] = []
                
    def __repr__(self):
        return f"Schedule1(days={self.days}, fitness={self.fitness})"
