# ==============================================================================
# main.py - Control de Grúa (Servidor Web + UART)
# ==============================================================================
# Este archivo contiene toda la lógica de control:
#   1. Configuración UART para comunicación serial con Arduino.
#   2. Servidor web asíncrono (uasyncio) que sirve la interfaz y
#      procesa los comandos de la grúa.
#   3. Tarea en segundo plano para leer telemetría del Arduino.
# ==============================================================================

import uasyncio as asyncio
import machine
import time

# ==============================================================================
# 1. CONFIGURACIÓN UART (Serial hacia el Arduino)
# ==============================================================================
# Usamos UART 2 con TX=17 y RX=16 según el hardware
# El TX de la ESP32 (Pin 17) va conectado al RX del Arduino (D0)
# El RX de la ESP32 (Pin 16) va conectado al TX del Arduino (D1)
# GND compartido entre ambos dispositivos
# ==============================================================================

print("Configurando UART2 en pines TX=17 y RX=16...")
try:
    uart = machine.UART(2, baudrate=9600, tx=17, rx=16)
    print("[TELEMETRÍA] UART configurado correctamente a 9600 baudios.")
except Exception as e:
    print("!!! ERROR CONFIGURANDO UART !!!", e)

# ==============================================================================
# 2. FUNCIONES UART
# ==============================================================================

def enviar_comando_uart(comando):
    """Envía el comando por Serial al Arduino añadiendo un salto de línea."""
    mensaje = comando + "\n"
    uart.write(mensaje)
    print("[TELEMETRÍA UART] -> Enviado a Arduino (TX): " + str(comando))

async def leer_telemetria_uart():
    """Lee constantemente el UART para recibir datos del Arduino."""
    while True:
        if uart.any():
            try:
                datos = uart.readline().decode('utf-8').strip()
                if datos:
                    print("[TELEMETRÍA UART] <- Recibido de Arduino (RX): " + str(datos))
            except Exception:
                pass
        await asyncio.sleep(0.05) # Pausa breve para no bloquear

# ==============================================================================
# 3. SERVIDOR WEB - Servir archivos estáticos
# ==============================================================================

async def enviar_archivo(writer, archivo, content_type):
    """Lee un archivo de la memoria del ESP32 y lo envía como respuesta HTTP."""
    try:
        with open(archivo, 'r') as f:
            contenido = f.read()
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n{contenido}"
        writer.write(response.encode('utf-8'))
        await writer.drain()
    except Exception as e:
        print("Error leyendo", archivo, ":", e)
        response = "HTTP/1.1 404 Not Found\r\n\r\nArchivo no encontrado"
        writer.write(response.encode('utf-8'))
        await writer.drain()

# ==============================================================================
# 4. SERVIDOR WEB - Manejar peticiones de los clientes
# ==============================================================================

async def handle_client(reader, writer):
    """Procesa cada petición HTTP entrante del navegador web."""
    try:
        request_line = await reader.readline()
        
        # Leer todas las cabeceras HTTP hasta la línea vacía
        while await reader.readline() != b"\r\n":
            pass
            
        req = str(request_line)
        
        # Extraer la ruta para telemetría HTTP
        ruta = req.split(' ')[1] if len(req.split(' ')) > 1 else "Desconocida"
        if ruta != "/favicon.ico":
            print("[TELEMETRÍA HTTP] Petición recibida: " + str(ruta))
        
        # --- Comandos de la grúa (se envían por UART al Arduino) ---
        is_command = False
        if '/up' in req:
            enviar_comando_uart('U')
            is_command = True
        elif '/down' in req:
            enviar_comando_uart('D')
            is_command = True
        elif '/left' in req:
            enviar_comando_uart('L')
            is_command = True
        elif '/right' in req:
            enviar_comando_uart('R')
            is_command = True
        elif '/stop' in req:
            enviar_comando_uart('S')
            is_command = True
        
        # --- Archivos estáticos (interfaz web) ---
        elif 'GET / ' in req or 'GET /index.html' in req:
            await enviar_archivo(writer, 'index.html', 'text/html')
            return
            
        # Si fue un comando, respondemos con un simple OK
        if is_command:
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK"
            writer.write(response.encode('utf-8'))
            await writer.drain()
        
    except Exception as e:
        print("Error con cliente:", e)
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass

# ==============================================================================
# 5. INICIAR SERVIDOR
# ==============================================================================

async def main():
    """Función principal: inicia el servidor web y la lectura UART en paralelo."""
    print("[TELEMETRÍA SISTEMA] Iniciando servidor web y receptor UART...")
    
    # Iniciamos la tarea de lectura UART en paralelo
    asyncio.create_task(leer_telemetria_uart())
    
    # Servidor web en el puerto 80
    server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
    print("[TELEMETRÍA SISTEMA] Servidor web activo en puerto 80.")
    print("[TELEMETRÍA SISTEMA] Abre la IP mostrada en boot.py desde tu navegador.\n")
    
    while True:
        await asyncio.sleep(1)

# ==============================================================================
# 6. ARRANQUE
# ==============================================================================

print(">>> INICIANDO SCRIPT MAIN.PY <<<")
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Sistema detenido por el usuario.")
except Exception as e:
    print("!!! ERROR FATAL EN MAIN.PY !!!")
    print(e)