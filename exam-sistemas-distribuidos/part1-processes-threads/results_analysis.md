# Análisis de Resultados: Hilos vs. Procesos

## 📊 Resultados de Ejecución

Al ejecutar `task_processor.py` con 20 tareas de dificultad aleatoria (1-5), los resultados son:

--- Ejecutando Hilos ---
[Hilo] Tarea 4 completada (Total Hilos: 1)
[Hilo] Tarea 9 completada (Total Hilos: 2)
[Hilo] Tarea 1 completada (Total Hilos: 3)
[Hilo] Tarea 5 completada (Total Hilos: 4)
[Hilo] Tarea 8 completada (Total Hilos: 5)
[Hilo] Tarea 18 completada (Total Hilos: 6)
[Hilo] Tarea 15 completada (Total Hilos: 7)
[Hilo] Tarea 12 completada (Total Hilos: 8)
[Hilo] Tarea 0 completada (Total Hilos: 9)
[Hilo] Tarea 16 completada (Total Hilos: 10)
[Hilo] Tarea 13 completada (Total Hilos: 11)
[Hilo] Tarea 2 completada (Total Hilos: 12)
[Hilo] Tarea 3 completada (Total Hilos: 13)
[Hilo] Tarea 10 completada (Total Hilos: 14)
[Hilo] Tarea 7 completada (Total Hilos: 15)
[Hilo] Tarea 17 completada (Total Hilos: 16)
[Hilo] Tarea 19 completada (Total Hilos: 17)
[Hilo] Tarea 11 completada (Total Hilos: 18)
[Hilo] Tarea 14 completada (Total Hilos: 19)
[Hilo] Tarea 6 completada (Total Hilos: 20)
Tiempo con hilos: 0.50s
Tareas completadas en hilos: 20

--- Ejecutando Procesos ---
[Proceso] Tarea 1 completada (Total Procesos: 1)
[Proceso] Tarea 4 completada (Total Procesos: 2)
[Proceso] Tarea 5 completada (Total Procesos: 3)
[Proceso] Tarea 12 completada (Total Procesos: 4)
[Proceso] Tarea 9 completada (Total Procesos: 5)
[Proceso] Tarea 8 completada (Total Procesos: 6)
[Proceso] Tarea 0 completada (Total Procesos: 7)
[Proceso] Tarea 15 completada (Total Procesos: 8)
[Proceso] Tarea 18 completada (Total Procesos: 9)
[Proceso] Tarea 16 completada (Total Procesos: 10)
[Proceso] Tarea 13 completada (Total Procesos: 11)
[Proceso] Tarea 7 completada (Total Procesos: 12)
[Proceso] Tarea 3 completada (Total Procesos: 13)
[Proceso] Tarea 2 completada (Total Procesos: 15)
[Proceso] Tarea 14 completada (Total Procesos: 17)
[Proceso] Tarea 11 completada (Total Procesos: 18)
[Proceso] Tarea 19 completada (Total Procesos: 19)
[Proceso] Tarea 6 completada (Total Procesos: 20)
Tiempo con procesos: 0.69s
Tareas completadas en procesos: 20

### ¿Por qué los Hilos ganan en esta prueba?

En esta prueba, **los hilos (0.50s) fueron más rápidos que los procesos (0.69s)**.

La tarea simulada es `time.sleep(difficulty * 0.1)`. Esta es una operación **I/O-Bound** (limitada por Entrada/Salida o, en este caso, espera).

1.  **Hilos (Threading):** Python tiene un "Global Interpreter Lock" (GIL) que impide que dos hilos ejecuten código Python en la CPU al mismo tiempo. Sin embargo, cuando un hilo realiza una operación de I/O (como `time.sleep()`, esperar una descarga o leer un archivo), **libera el GIL**. Esto permite que otro hilo comience a ejecutarse. El resultado es una concurrencia muy eficiente para tareas de espera, con un bajo costo de arranque.

2.  **Procesos (Multiprocessing):** Cada proceso tiene su propio intérprete de Python y su propio GIL, por lo que pueden ejecutarse en paralelo real en diferentes núcleos de CPU. Sin embargo, crear un proceso es una operación muy "costosa" (lenta) para el sistema operativo; requiere copiar memoria y asignar muchos más recursos que un hilo.

**Conclusión:** Dado que la tarea es de espera (I/O-Bound), el bajo costo de creación de los hilos supera el alto costo de creación de los procesos.

> **Nota:** Si la tarea fuera **CPU-Bound** (un cálculo matemático pesado), los **Procesos** ganarían, ya que podrían usar múltiples núcleos de CPU simultáneamente.
