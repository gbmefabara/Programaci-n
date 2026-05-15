# ==============================================================================
# FASE 3 - Servidor Web ESP32 con MicroPython (uasyncio)
# ==============================================================================
# Este archivo es una maqueta de cómo funcionará el servidor web.
# Usa uasyncio para no bloquear el procesador mientras espera peticiones.
# ==============================================================================

import uasyncio as asyncio
import network

# 1. Función para manejar a cada cliente (navegador web) que se conecta
async def handle_client(reader, writer):
    print("Nuevo cliente web conectado.")
    
    # Leemos la primera línea de la petición (ej: GET /up HTTP/1.1)
    request_line = await reader.readline()
    print("Petición cruda:", request_line)
    
    # Leemos el resto de las cabeceras HTTP hasta encontrar una línea vacía
    while await reader.readline() != b"\r\n":
        pass
        
    request = str(request_line)
    
    # 2. Lógica para determinar qué botón se presionó
    if '/left' in request:
        print("=> Comando Web Identificado: LEFT")
    elif '/right' in request:
        print("=> Comando Web Identificado: RIGHT")
    elif '/up' in request:
        print("=> Comando Web Identificado: UP")
    elif '/down' in request:
        print("=> Comando Web Identificado: DOWN")
    elif '/stop' in request:
        print("=> Comando Web Identificado: STOP")
        
    # 3. Respondemos al navegador web con un código HTTP 200 (Todo Bien)
    response = "HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\nOK"
    await writer.awrite(response)
    
    # Cerramos la conexión con este cliente
    await writer.aclose()

# 4. Bucle principal del servidor
async def main():
    print("Iniciando servidor asíncrono en el puerto 80...")
    # Creamos el servidor y lo asociamos a nuestra función "handle_client"
    server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
    
    # Mantenemos el servidor corriendo indefinidamente
    while True:
        await asyncio.sleep(1)

# Para ejecutar este código en la placa (descomentar la siguiente línea):
# asyncio.run(main())
