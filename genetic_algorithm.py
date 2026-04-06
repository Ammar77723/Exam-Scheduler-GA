import random
from models import Schedule1, Classrooms_Class
from config import total_days, room_names
from constraints import (
    hard_constraint1_all_courses,
    hard_constraint2b_one_exam,
    hard_constraint5a_teacher_sametime,
    hard_constraint5b_teacher_row,
    soft_constraint2_no_consecutive_exams,
    soft_constraint3_mg_before_cs,
    constraints_satisfied_check,
    print_constraint_fulfillment
)
from utils import print_schedule

def generate_population(population_size, courses, teachers):
    new_pop = []
    for _ in range(population_size):
        schedule = Schedule1()
        for day in total_days:
            classrooms_assigned = []
            total_classrooms = random.randint(1, len(room_names))
            for _ in range(total_classrooms):
                room = random.choice(room_names)
                morning_course, morning_invigilator = random.choice(courses), random.choice(teachers)
                noon_course, noon_invigilator = random.choice(courses), random.choice(teachers)
                class_r = Classrooms_Class(
                        room_name=room,
                        morning=morning_course[0],
                        invig_morning=morning_invigilator,
                        noon=noon_course[0],
                        invig_noon=noon_invigilator
                    )
                schedule.days[day].append(class_r)
        new_pop.append(schedule)
    return new_pop

def calculate_fitness(population, courses, course_allocation):
    for schedule in population:
        hc1, hb1 = hard_constraint1_all_courses(schedule, courses)
        hc2b, hb2b = hard_constraint2b_one_exam(schedule, course_allocation)
        hc5a, hb5a = hard_constraint5a_teacher_sametime(schedule)
        hc5b, hb5b = hard_constraint5b_teacher_row(schedule)
        sc2, sb2 = soft_constraint2_no_consecutive_exams(schedule, course_allocation)
        sc3, sb3 = soft_constraint3_mg_before_cs(schedule, course_allocation)
        
        fitness = hc1 + hc2b + hc5a + hc5b + sc2 + sc3
        schedule.fitness = fitness
    return population

def get_fitness(schedule):
    return schedule.fitness

def two_fittest_schedules(population):
    sorted_population = sorted(population, key=get_fitness, reverse=True)
    return sorted_population[:2]

def parent_selection(population):
    parents = []
    total_fitness = sum(schedule.fitness for schedule in population)
    highest, second_highest = two_fittest_schedules(population)
    parents.extend([highest, second_highest])
    fitness_sum = highest.fitness + second_highest.fitness

    while len(parents) < len(population):
        individual = random.randint(0, len(population) - 1)
        fitness_sum += population[individual].fitness
        if fitness_sum >= total_fitness:
            if population[individual] not in parents:
                parents.append(population[individual])
    return parents

def apply_crossover(population, crossover_probability):
    crossovered_population = []
    while len(crossovered_population) < len(population):
        if random.random() <= crossover_probability:
            no_days_to_mix = random.randint(1, len(total_days) - 1)
            child1 = Schedule1()
            child2 = Schedule1()
            
            days = list(total_days)
            random.shuffle(days)
            
            parent_a, _ = two_fittest_schedules(population) 
            parent_b = random.choice(population)
            
            for i, day in enumerate(days):
                if i < no_days_to_mix:
                    child1.days[day] = parent_a.days[day]
                    child2.days[day] = parent_b.days[day]
                else:
                    child1.days[day] = parent_b.days[day]
                    child2.days[day] = parent_a.days[day]
                    
            crossovered_population.append(child1)
            crossovered_population.append(child2)
    return crossovered_population

def mutate(schedule, mutation_probability, courses, teachers):
    if random.random() <= mutation_probability:
        random_days = random.randint(1, len(total_days)) 
        for _ in range(random_days):
            index = random.randint(0, len(total_days) - 1)
            day = total_days[index]
            classes_list = schedule.days[day]
            if classes_list:
                if random.random() < 0.5:
                    for cls in classes_list:
                        course_code, _ = random.choice(courses)  
                        cls.morning = course_code
                        cls.invig_morning = random.choice(teachers)
                        course_code, _ = random.choice(courses)
                        cls.noon = course_code
                        cls.invig_noon = random.choice(teachers)
                else:
                    classes_list.clear()
            else:
                total_classrooms = random.randint(1, len(room_names))
                for _ in range(total_classrooms):
                    room = random.choice(room_names)
                    course_code_m, _ = random.choice(courses)
                    m_invig = random.choice(teachers)  
                    course_code_n, _ = random.choice(courses)
                    n_invig = random.choice(teachers)
                    class_r = Classrooms_Class(room, course_code_m, m_invig, course_code_n, n_invig)
                    classes_list.append(class_r)
    return schedule

def apply_mutation(population, mutation_probability, courses, teachers):
    mutated_population = []
    for schedule in population:
        mutated_schedule = mutate(schedule, mutation_probability, courses, teachers)
        mutated_population.append(mutated_schedule)
    return mutated_population

def genetic_algorithm(population_size, max_generations, crossover_probability, mutation_probability, courses, teachers, course_allocation):
    best_solution = None
    population = [generate_population(population_size, courses, teachers)]
    
    stuck = 0
    reset_count = 0
    solutions_list = []
    prev_best = None

    for i in range(max_generations):
        population_fitness = calculate_fitness(population[0], courses, course_allocation)
        parents = parent_selection(population_fitness)
        crossover_population = apply_crossover(parents, crossover_probability)
        calculate_fitness(crossover_population, courses, course_allocation)
        mutated_population = apply_mutation(crossover_population, mutation_probability, courses, teachers)
        calculate_fitness(mutated_population, courses, course_allocation)
        schedule, _ = two_fittest_schedules(mutated_population)

        if best_solution is None or schedule.fitness > best_solution.fitness:
            stuck = 0
            best_solution = schedule

        if best_solution.fitness == prev_best:
            stuck += 1
        prev_best = best_solution.fitness

        if constraints_satisfied_check(best_solution, courses, course_allocation):
            print(print_constraint_fulfillment(best_solution, courses, course_allocation))
            print("\nSolution Found!\n")
            return best_solution

        if stuck == 50:
            print("\nAlgorithm unable to further optimize. Restarting with a new random population.\n")
            solutions_list.append(best_solution)
            stuck = 0
            reset_count += 1
            pop = generate_population(population_size, courses, teachers)
            best_solution = None
            population.clear()
            population.append(pop)
            continue
        else:
            population.clear()
            population.append(mutated_population)

        if i % 50 == 0:
            print("Current generation: ", i)
            print("Best solution Fitness: ", best_solution.fitness)
            print_schedule(best_solution)
            print(print_constraint_fulfillment(best_solution, courses, course_allocation))
            
        print(f"{i} - Fitness of best solution: {best_solution.fitness:.2f} (Fitness of current: {schedule.fitness:.2f}) (Stuck Count: {stuck})")

    return best_solution
