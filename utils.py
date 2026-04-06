import os
import pandas as pd

def print_custom_schedule(schedule):
    for day, classes_list in schedule.days.items():
        if len(classes_list) > 0:
            print("\n" + day + "\n")
            print("Room No - 9_12 - Morning Invigilator - 2_5 - Evening Invigilator")
            for _class in classes_list:
                print(_class)

def get_custom_schedule_as_dataframe(schedule):
    data = []
    for day in schedule.days:
        if len(schedule.days[day]) > 0:
            for _class in schedule.days[day]:
                data.append([day, _class.room_name, _class.morning, _class.invig_morning, _class.noon, _class.invig_noon])
    df = pd.DataFrame(data, columns=['Day', 'Room No', '9 - 12', 'Morning Invigilator', '2 - 5', 'Evening Invigilator'])
    return df

def save_schedule_to_csv(schedule, file_path):
    if os.path.exists(file_path):
        open(file_path, 'w').close()
    df = get_custom_schedule_as_dataframe(schedule)
    df.to_csv(file_path, index=False, mode='w')

def print_schedule(schedule):
    for day in schedule.days:
        if len(schedule.days[day]) > 0:
            print("\nDay: ", day)
            for _class in schedule.days[day]:
                print(_class)
    print()
    
def print_population(population):
    for i, schedule in enumerate(population):
        print(f"Schedule {i + 1}:")
        print_schedule(schedule[0])
        print()
