import multiprocessing
import threading
import time
import random


def process_task_process(task_id, difficulty, counter):
    time.sleep(difficulty * 0.1)  # Simulación de carga
    with counter.get_lock():
        counter.value += 1
        print(
            f"[Proceso] Tarea {task_id} completada (Total Procesos: {counter.value})")


class TaskProcessor:
    def __init__(self):
        # Para procesos
        self.process_tasks_completed = multiprocessing.Value('i', 0)
        # Para hilos
        self.thread_tasks_completed = 0
        self.lock = threading.Lock()

    def process_task_thread(self, task_id, difficulty):
        time.sleep(difficulty * 0.1)

        # Zona crítica para el contador de hilos
        with self.lock:
            self.thread_tasks_completed += 1
            print(
                f"[Hilo] Tarea {task_id} completada (Total Hilos: {self.thread_tasks_completed})")

    def run_with_threads(self, tasks):
        threads = []
        for task_id, difficulty in tasks:
            t = threading.Thread(
                target=self.process_task_thread, args=(task_id, difficulty))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    def run_with_processes(self, tasks):
        processes = []
        for task_id, difficulty in tasks:
            # Ahora llamamos a la función global 'process_task_process'
            p = multiprocessing.Process(target=process_task_process, args=(
                task_id, difficulty, self.process_tasks_completed))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()


if __name__ == "__main__":
    processor = TaskProcessor()
    tasks = [(i, random.randint(1, 5)) for i in range(20)]

    # Ejecutar hilos
    print("--- Ejecutando Hilos ---")
    start = time.time()
    processor.run_with_threads(tasks)
    end = time.time()
    print(f"Tiempo con hilos: {end - start:.2f}s")
    print(f"Tareas completadas en hilos: {processor.thread_tasks_completed}")

    # Ejecutar procesos
    print("\n--- Ejecutando Procesos ---")
    start = time.time()
    processor.run_with_processes(tasks)
    end = time.time()
    print(f"Tiempo con procesos: {end - start:.2f}s")
    print(
        f"Tareas completadas en procesos: {processor.process_tasks_completed.value}")
