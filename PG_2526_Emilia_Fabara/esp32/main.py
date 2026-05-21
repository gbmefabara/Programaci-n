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

# 2. Página Web Completa (HTML + CSS + JS) incrustada
INDEX_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Control de Grúa Torre</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: sans-serif; background: #4B79BA; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; }
.container { background: #263544; padding: 40px 30px; border-radius: 12px; box-shadow: 0 15px 40px rgba(0,0,0,0.5); text-align: center; width: 90%; max-width: 420px; position: relative; overflow: hidden; }
.tape { position: absolute; width: 12px; height: 100%; top: 0; background: repeating-linear-gradient(-45deg, #F39C12, #F39C12 15px, #263544 15px, #263544 30px); }
.tape-left { left: 0; }
.tape-right { right: 0; background: repeating-linear-gradient(45deg, #F39C12, #F39C12 15px, #263544 15px, #263544 30px); }
.corner { position: absolute; width: 40%; height: 2px; background: #F39C12; left: 30%; }
.corner-top { top: 12px; } .corner-bottom { bottom: 12px; }
.corner::before, .corner::after { content: ''; position: absolute; width: 8px; height: 8px; }
.corner-top::before { left: -8px; top: 0; border-top: 2px solid #F39C12; border-left: 2px solid #F39C12; }
.corner-top::after { right: -8px; top: 0; border-top: 2px solid #F39C12; border-right: 2px solid #F39C12; }
.corner-bottom::before { left: -8px; bottom: 0; border-bottom: 2px solid #F39C12; border-left: 2px solid #F39C12; }
.corner-bottom::after { right: -8px; bottom: 0; border-bottom: 2px solid #F39C12; border-right: 2px solid #F39C12; }
.header { display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 25px; }
.crane-icon { width: 40px; height: 40px; }
h1 { font-size: 1.8rem; font-weight: 700; }
.status { background: #F39C12; color: #263544; padding: 12px 20px; border-radius: 6px; font-weight: 700; margin: 0 auto 35px auto; width: 85%; transition: background 0.3s; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
.status.connected { background: #2ECC71; color: white; }
.controls { display: grid; grid-template-areas: ". up ." "left stop right" ". down ."; gap: 15px; justify-content: center; }
.btn { border: none; border-radius: 50%; width: 90px; height: 90px; color: white; cursor: pointer; display: flex; flex-direction: column; align-items: center; justify-content: center; user-select: none; transition: transform 0.1s; box-shadow: 0 10px 20px rgba(0,0,0,0.6), inset 0 3px 5px rgba(255,255,255,0.3); }
.btn:active { transform: scale(0.95); box-shadow: 0 5px 10px rgba(0,0,0,0.6), inset 0 3px 5px rgba(0,0,0,0.4); }
.icon { font-size: 1.8rem; margin-bottom: 3px; font-weight: bold; }
.label { font-size: 0.8rem; font-weight: 600; }
.btn-up, .btn-down { background: radial-gradient(circle at 50% 20%, #5ba75b, #3d793d); grid-area: up; }
.btn-down { grid-area: down; }
.btn-left, .btn-right { background: radial-gradient(circle at 50% 20%, #3498db, #1d6fa5); }
.btn-left { grid-area: left; } .btn-right { grid-area: right; }
.btn-stop { background: radial-gradient(circle at 50% 20%, #e74c3c, #b3362a); grid-area: stop; }
</style>
</head>
<body>
<div class="container">
    <div class="tape tape-left"></div><div class="tape tape-right"></div>
    <div class="corner corner-top"></div><div class="corner corner-bottom"></div>
    <div class="header">
        <svg class="crane-icon" viewBox="0 0 24 24" fill="none" stroke="#F39C12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 21h18"></path><path d="M7 21V5a2 2 0 0 1 2-2h6"></path><path d="M9 7l12-3"></path><path d="M17 4v4"></path><path d="M17 8h3"></path>
        </svg>
        <h1>Control de la Grúa</h1>
    </div>
    <div id="status" class="status">Cargando...</div>
    <div class="controls">
        <button class="btn btn-up" onmousedown="snd('U')" onmouseup="snd('S')" ontouchstart="snd('U')" ontouchend="snd('S')"><span class="icon">&#8593;</span><span class="label">Subir</span></button>
        <button class="btn btn-left" onmousedown="snd('L')" onmouseup="snd('S')" ontouchstart="snd('L')" ontouchend="snd('S')"><span class="icon">&#8592;</span><span class="label">Izquierda</span></button>
        <button class="btn btn-stop" onclick="snd('S')"><span class="icon">&#9632;</span><span class="label">Parar</span></button>
        <button class="btn btn-right" onmousedown="snd('R')" onmouseup="snd('S')" ontouchstart="snd('R')" ontouchend="snd('S')"><span class="icon">&#8594;</span><span class="label">Derecha</span></button>
        <button class="btn btn-down" onmousedown="snd('D')" onmouseup="snd('S')" ontouchstart="snd('D')" ontouchend="snd('S')"><span class="icon">&#8595;</span><span class="label">Bajar</span></button>
    </div>
</div>
<script>
const st = document.getElementById('status');
function snd(cmd) {
    fetch('/'+cmd).then(r=>{
        if(r.ok){ st.innerHTML="✅ Conectado ("+cmd+")"; st.classList.add('connected'); }
    }).catch(e=>{ st.innerHTML="⚠️ Error"; st.classList.remove('connected'); });
}
snd('S');
</script>
</body>
</html>
"""

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
        if '/U' in req:
            enviar_comando_uart('U')
        elif '/D' in req:
            enviar_comando_uart('D')
        elif '/L' in req:
            enviar_comando_uart('L')
        elif '/R' in req:
            enviar_comando_uart('R')
        elif '/S' in req:
            enviar_comando_uart('S')
        elif 'GET / ' in req: # Solicitud de la página principal
            # Enviamos el HTML
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + INDEX_HTML
            writer.write(response.encode('utf-8'))
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return
            
        # Si fue un comando, respondemos con un simple OK
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

