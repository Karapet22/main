import random
import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def create_file(filename):
    with open(filename, 'w') as f:
        for _ in range(100):
            line = " ".join(str(random.randint(1, 100)) for _ in range(20))
            f.write(line + "\n")

def process_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    filtered_lines = []
    for line in lines:
        numbers = list(map(int, line.split()))  
        filtered_numbers = list(filter(lambda x: x > 40, numbers))  
        filtered_lines.append(" ".join(map(str, filtered_numbers)))  
    
    with open(filename, 'w') as f:
        f.write("\n".join(filtered_lines))

def read_file_as_generator(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield list(map(int, line.split()))  

@measure_time
def run_all_operations(filename):
    create_file(filename) 
    process_file(filename) 
    
    # Read the file using generator and print the content
    print("Reading file using generator:")
    for line in read_file_as_generator(filename):
        print(line)


filename = "numbers.txt"


run_all_operations(filename)
