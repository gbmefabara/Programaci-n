# ==============================================================================
# FASE 2 - Comunicación UART (ESP32 a Arduino) - ESP32
# ==============================================================================
# Este archivo configura a la ESP32 para enviar comandos de texto
# a través del puerto serial (UART) hacia el Arduino Nano.
#
# Explicación:
# - RX / TX: RX significa Recibir, TX significa Transmitir.
#   El TX de la ESP32 va conectado al RX del Arduino.
# - Baudrate: Es la velocidad de comunicación (9600 bps en este caso).
#   Ambos dispositivos deben hablar a la misma velocidad para entenderse.
# - GND compartido: Los cables de tierra (GND) del ESP32 y del Arduino
#   DEBEN estar conectados juntos, de lo contrario la comunicación fallará.
# ==============================================================================

import machine  # Para usar los pines y el hardware UART
import time     # Para manejar pausas

# 1. Configuración de UART
# Usamos UART 2. En la ESP32, podemos asignar qué pines usamos.
# Según el requirement, el TX de la ESP32 es el GPIO 17. 
# El RX no lo usaremos para recibir en esta fase, pero lo asignamos al 16.
print("Configurando UART2 a 9600 baudios...")
uart = machine.UART(2, baudrate=9600, tx=17, rx=16)

# 2. Lista de comandos de prueba
comandos = ["LEFT", "RIGHT", "UP", "DOWN", "STOP"]

print("Iniciando transmisión UART...")
print("Asegúrate de que el TX (Pin 17) de la ESP32 está conectado al RX (D0) del Arduino.")
print("Asegúrate de compartir el GND entre ambos.")

# 3. Bucle infinito de envío
try:
    while True:
        # Recorremos cada comando en la lista
        for comando in comandos:
            # Enviamos el comando sumando un salto de línea (\n)
            # El salto de línea le ayuda al Arduino a saber dónde termina el mensaje
            mensaje = comando + "\n"
            uart.write(mensaje) # Escribimos en el puerto serial
            
            print("Mensaje enviado al Arduino:", comando)
            
            # Esperamos 2 segundos antes de enviar el siguiente comando
            time.sleep(2)
            
except KeyboardInterrupt:
    print("Transmisión UART detenida por el usuario.")
