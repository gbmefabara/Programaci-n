# ==============================================================================
# FASE 4 - Integración Total: boot.py
# ==============================================================================
# Este archivo es lo primero que ejecuta la ESP32 al encenderse.
# Aquí configuraremos la conexión WiFi en modo Estación (STA),
# para que la ESP32 se conecte a tu red WiFi doméstica.
# ==============================================================================

import network
import time

def connect_wifi():
    """Conecta la ESP32 a una red WiFi existente."""
    print("Iniciando Modo Estación (STA)...")
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.disconnect() # Forzar desconexión para limpiar configuraciones antiguas
    time.sleep(0.5)
    
    print("Conectando a la red WiFi doméstica...")
    
    # ---------------------------------------------------------
    # CONFIGURACIÓN DE IP PRIVADA/LOCAL (IP ESTÁTICA)
    # ---------------------------------------------------------
    # Basado en tu consola, tu red es 192.168.100.X y tu router es 192.168.100.1
    ip_fija = '192.168.100.200' # Usamos 200 para evitar que choque con otros dispositivos
    mascara = '255.255.255.0'
    puerta_enlace = '192.168.100.1'
    dns = '8.8.8.8'
    sta.ifconfig((ip_fija, mascara, puerta_enlace, dns))
    print(f"[TELEMETRÍA] Asignando IP estática local: {ip_fija}")

    # IMPORTANTE: Cambia estos valores por el nombre (SSID) y contraseña de tu WiFi
    sta.connect('NETLIFE-NELSON', 'Emily2008')
    
    # Esperamos a que se conecte
    intentos = 0
    while not sta.isconnected() and intentos < 20:
        time.sleep(1)
        print(".", end="")
        intentos += 1
        
    if not sta.isconnected():
        print("\nError: No se pudo conectar al WiFi. Revisa el nombre y contraseña.")
        return

    print("\n¡Conexión WiFi exitosa!")
    ip = sta.ifconfig()[0]
    print("=======================================================")
    print("🌐 IP OBTENIDA PARA ACCEDER DESDE EL TELÉFONO:")
    print(f"http://{ip}")
    print("=======================================================")
    print("Servidor listo para iniciar...\n")

# Llamamos a la función al encender
connect_wifi()

import main