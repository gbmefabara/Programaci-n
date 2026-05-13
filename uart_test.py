from machine import UART
import time

# Configuración del puerto serial UART en la ESP32
# Usamos UART(2) que es el segundo puerto serial de hardware disponible en la ESP32
# baudrate=9600 debe ser exactamente el mismo en el código del Arduino Nano
# tx=17 y rx=16 son los pines físicos que asignamos, de acuerdo a la arquitectura del proyecto
uart = UART(2, baudrate=9600, tx=17, rx=16)

print("Iniciando prueba de comunicación serial ESP32 -> Arduino...")

try:
    while True:
        # Preparamos el mensaje. Añadimos '\n' (salto de línea) al final
        # para que sea más fácil para el Arduino saber cuándo termina el texto.
        mensaje = "hola\n"
        
        # uart.write() envía los datos.
        # Es buena práctica convertir el string a bytes usando .encode()
        uart.write(mensaje.encode('utf-8'))
        
        # Mostramos en la consola de Thonny lo que acabamos de enviar
        print("Mensaje enviado:", mensaje.strip())
        
        # Hacemos una pausa de 2 segundos exactos
        time.sleep(2)
        
except KeyboardInterrupt:
    # Se ejecuta si presionas el botón Stop en Thonny o haces Ctrl+C
    print("Prueba UART detenida.")
