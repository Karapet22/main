import os
import time
from collections import Counter
from threading import Thread, Lock
from multiprocessing import Process, Manager
import random


def create_large_file(filename, num_lines, num_words_per_line):
    words = ["word", "text", "python", "code", "example", "test", "performance"]
    with open(filename, "w") as file:
        for _ in range(num_lines):
            file.write(" ".join(random.choice(words) for _ in range(num_words_per_line)) + "\n")


def count_words(filename):
    with open(filename, 'r') as file:
        return Counter(word for line in file for word in line.split())


def count_words_thread(chunk, word_counter, lock):
    with lock:
        word_counter.update(chunk.split())


def multithreaded_word_count(filename, num_threads=4):
    file_size = os.path.getsize(filename)
    chunk_size = file_size // num_threads
    word_counter = Counter()
    lock = Lock()

    with open(filename, 'r') as file:
        threads = [
            Thread(target=count_words_thread, args=(file.read(chunk_size), word_counter, lock))
            for _ in range(num_threads)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    return word_counter


def count_words_process(chunk, return_dict):
    return_dict.update(Counter(chunk.split()))


def multiprocessing_word_count(filename, num_processes=4):
    file_size = os.path.getsize(filename)
    chunk_size = file_size // num_processes
    manager = Manager()
    return_dict = manager.dict()

    with open(filename, 'r') as file:
        processes = [
            Process(target=count_words_process, args=(file.read(chunk_size), return_dict))
            for _ in range(num_processes)
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join()

    return Counter(return_dict)


if __name__ == "__main__":
    filename = "large_text_file.txt"
    create_large_file(filename, num_lines=5000, num_words_per_line=100)

    start_time = time.time()
    sequential_result = count_words(filename)
    sequential_time = time.time() - start_time
    print(f"Sequential execution time: {sequential_time:.4f} seconds")

    start_time = time.time()
    threaded_result = multithreaded_word_count(filename)
    threaded_time = time.time() - start_time
    print(f"Multithreading execution time: {threaded_time:.4f} seconds")

    start_time = time.time()
    multiprocessing_result = multiprocessing_word_count(filename)
    multiprocessing_time = time.time() - start_time
    print(f"Multiprocessing execution time: {multiprocessing_time:.4f} seconds")

    print("\nSpeedup:")
    print(f"Multithreading speedup: {sequential_time / threaded_time:.2f}")
    print(f"Multiprocessing speedup: {sequential_time / multiprocessing_time:.2f}")
