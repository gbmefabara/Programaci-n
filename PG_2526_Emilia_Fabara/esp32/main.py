# ==============================================================================
# FASE 4 - Integración Total: main.py (ESP32)
# ==============================================================================
# Este archivo une todo: el Servidor Web (uasyncio) y la transmisión UART.
# Contiene el HTML/CSS/JS incrustado para simplificar la carga a la ESP32.
# ==============================================================================

import uasyncio as asyncio
import machine
import time

# 1. Configuración del UART (Serial hacia el Arduino)
print("Configurando UART2 en pines 16 y 17...")
try:
    # Usamos UART 2 con TX=17 y RX=16 según tu hardware fijo
    uart = machine.UART(2, baudrate=9600, tx=17, rx=16)
except Exception as e:
    print("!!! ERROR CONFIGURANDO UART !!!", e)

# 2. Función para servir archivos estáticos desde la memoria del ESP32
async def enviar_archivo(writer, archivo, content_type):
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

# 3. Función para enviar comandos por UART
def enviar_comando_uart(comando):
    """Envía el comando por Serial al Arduino añadiendo un salto de línea."""
    mensaje = comando + "\n"
    uart.write(mensaje)
    print("[TELEMETRÍA UART] -> Enviado a Arduino (TX): " + str(comando))

# Tarea en segundo plano para leer datos del Arduino
async def leer_telemetria_uart():
    """Lee constantemente el UART para recibir datos del Arduino y mostrarlos en el monitor serial."""
    while True:
        if uart.any():
            try:
                datos = uart.readline().decode('utf-8').strip()
                if datos:
                    print("[TELEMETRÍA UART] <- Recibido de Arduino (RX): " + str(datos))
            except Exception:
                pass
        await asyncio.sleep(0.05) # Pausa breve para no bloquear

# 4. Función para manejar las peticiones web de los clientes
async def handle_client(reader, writer):
    try:
        request_line = await reader.readline()
        
        while await reader.readline() != b"\r\n":
            pass
            
        req = str(request_line)
        
        # Extrayendo la ruta para telemetría HTTP
        ruta = req.split(' ')[1] if len(req.split(' ')) > 1 else "Desconocida"
        if ruta != "/favicon.ico":
            print("[TELEMETRÍA HTTP] Petición recibida: " + str(ruta))
        
        # Filtramos qué endpoint se solicitó y enviamos por UART
        # (Nuevas rutas alineadas con fetch('/up') de script.js)
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
        elif 'GET / ' in req or 'GET /index.html' in req:
            await enviar_archivo(writer, 'index.html', 'text/html')
            return
        elif 'GET /style.css' in req:
            await enviar_archivo(writer, 'style.css', 'text/css')
            return
        elif 'GET /script.js' in req:
            await enviar_archivo(writer, 'script.js', 'application/javascript')
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

# 5. Iniciar Servidor
async def main():
    print("[TELEMETRÍA SISTEMA] Iniciando servidor web y receptor UART...")
    
    # Iniciamos la tarea de lectura UART en paralelo
    asyncio.create_task(leer_telemetria_uart())
    
    server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
    while True:
        await asyncio.sleep(1)

# Arrancar la rutina principal
print(">>> INICIANDO SCRIPT MAIN.PY <<<")
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Sistema detenido por el usuario.")
except Exception as e:
    print("!!! ERROR FATAL EN MAIN.PY !!!")
    print(e)