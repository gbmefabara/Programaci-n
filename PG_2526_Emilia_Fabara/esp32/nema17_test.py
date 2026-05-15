# ==============================================================================
# FASE 1 - Prueba de Motor NEMA 17 con Driver DRV8825 usando MicroPython
# ==============================================================================
# Este archivo está diseñado para un estudiante principiante.
# Aquí aprendemos a mover un motor a pasos de manera continua.
# 
# Explicación de Velocidad y Dirección:
# - Dirección (DIR): Controla hacia dónde gira el motor. 
#   Si enviamos un 1 (HIGH), gira en un sentido (ej: derecha).
#   Si enviamos un 0 (LOW), gira en el otro sentido (ej: izquierda).
# - Velocidad (STEP): El motor avanza un "pasito" cada vez que enviamos
#   un pulso (cambiamos de 0 a 1). Si enviamos los pulsos muy rápido,
#   el motor gira rápido. Si hay mucha pausa entre pulsos, gira lento.
# ==============================================================================

import machine  # Librería para controlar los pines (hardware) de la ESP32
import time     # Librería para manejar pausas (delays)

# 1. Configuración de los pines
# Elegimos pines cualesquiera para la prueba en ESP32 (por ejemplo, 26 y 27)
# En el Arduino usaremos otros pines (D9 y D10), pero la lógica es la misma.
pin_step = machine.Pin(26, machine.Pin.OUT) # Configuramos el pin STEP como salida
pin_dir = machine.Pin(27, machine.Pin.OUT)  # Configuramos el pin DIR como salida

# 2. Función para mover el motor
def mover_motor(pasos, direccion, retardo_ms):
    """
    Función que mueve el motor a pasos.
    :param pasos: Cantidad de "pasitos" que va a dar el motor.
    :param direccion: 1 para derecha, 0 para izquierda.
    :param retardo_ms: Tiempo de pausa entre pasos. A menor pausa, más velocidad.
    """
    # Establecemos la dirección del motor
    pin_dir.value(direccion)
    print("Moviendo motor... Dirección:", direccion)
    
    # Repetimos la acción tantas veces como pasos queramos dar
    for i in range(pasos):
        pin_step.value(1)       # Encendemos el pin (inicio del pulso)
        time.sleep_ms(retardo_ms) # Esperamos un poco
        pin_step.value(0)       # Apagamos el pin (fin del pulso)
        time.sleep_ms(retardo_ms) # Esperamos para completar el ciclo

# 3. Código Principal
print("Iniciando prueba del motor Nema 17...")

# Hacemos que el motor gire de forma continua en un ciclo infinito
try:
    while True:
        # Giramos 200 pasos hacia un lado (200 pasos suele ser una vuelta completa)
        # Usamos un retardo de 5 milisegundos para una velocidad moderada
        mover_motor(200, 1, 5) 
        
        # Pausa de 1 segundo
        time.sleep(1)
        
        # Giramos 200 pasos hacia el otro lado
        mover_motor(200, 0, 5)
        
        # Pausa de 1 segundo
        time.sleep(1)

except KeyboardInterrupt:
    # Esto ocurre si detenemos el programa manualmente
    print("Prueba detenida.")
