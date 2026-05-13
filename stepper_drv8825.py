from machine import Pin
import time

# Definir los pines del ESP32 conectados al DRV8825
PIN_STEP = 26
PIN_DIR = 27

# Configurar los pines como salida (OUTPUT)
step = Pin(PIN_STEP, Pin.OUT)
dir = Pin(PIN_DIR, Pin.OUT)

# Establecer la dirección de giro inicial
# 1 = Un sentido (ej. horario)
# 0 = Sentido contrario (ej. antihorario)
dir.value(1)

# Velocidad del motor (pausa entre pasos)
# Un valor mayor hace que gire más lento. Un valor menor lo hace más rápido.
# Usamos 0.01 segundos (10 ms) para un movimiento lento y observable.
tiempo_espera = 0.01

print("Iniciando giro continuo del motor...")

# Bucle infinito para que el motor gire continuamente
try:
    while True:
        # Para dar un paso, el driver necesita recibir un "pulso" (Alto -> Bajo)
        
        # Poner el pin STEP en estado Alto
        step.value(1)
        
        # Una pequeña pausa para que el driver lea el pulso. 
        # (El DRV8825 requiere menos de 2 microsegundos, pero usamos 1 milisegundo por simplicidad)
        time.sleep_ms(1)
        
        # Poner el pin STEP en estado Bajo
        step.value(0)
        
        # Esperar antes de dar el siguiente paso. 
        # Esto es lo que controla la velocidad de giro.
        time.sleep(tiempo_espera)
        
except KeyboardInterrupt:
    # Si detenemos el programa (ej. con Ctrl+C en la consola), se detiene y avisa.
    print("Giro del motor detenido.")
