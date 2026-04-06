import random
from data_loader import load_data
from genetic_algorithm import genetic_algorithm
from utils import print_custom_schedule, save_schedule_to_csv
from constraints import print_constraint_fulfillment

def main():
    print("Loading data...")
    courses, teachers, course_allocation = load_data()
    
    population_size = random.randint(70, 150)       
    max_generations = random.randint(100, 400)      

    crossover_probability = 1
    mutation_probability = 0.8

    print(f'Population size: {population_size}')
    print(f'Number of generations: {max_generations}')
    print(f'Crossover probability: {crossover_probability}')
    print(f'Mutation probability: {mutation_probability}\n')
    
    print("Running Genetic Algorithm...")
    result = genetic_algorithm(
        population_size, max_generations, 
        crossover_probability, mutation_probability, 
        courses, teachers, course_allocation
    )

    if result:
        print("\nSaving schedule...")
        save_schedule_to_csv(result, "Dataset/result.csv")
        
        print("\nFinal Schedule:")
        print_custom_schedule(result)
        
        print("\nConstraints Feedback:")
        print(print_constraint_fulfillment(result, courses, course_allocation))
    else:
        print("Failed to find an optimal schedule before reaching max generations.")

if __name__ == "__main__":
    main()
