# ==============================================================================
# FASE 4 - Integración Total: boot.py
# ==============================================================================
# Este archivo es lo primero que ejecuta la ESP32 al encenderse.
# Aquí configuraremos la conexión WiFi en modo Access Point (Punto de Acceso),
# para que nos podamos conectar directamente a la grúa sin usar un router.
# ==============================================================================

import network
import time

def setup_ap():
    """Configura la ESP32 para crear su propia red WiFi."""
    print("Iniciando Modo Punto de Acceso (AP)...")
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    
    # Nombre de la red (SSID) y contraseña
    ap.config(essid="GruaTorre_ESP32", password="password123")
    
    while not ap.active():
        pass
        
    print("Red WiFi 'GruaTorre_ESP32' creada con éxito.")
    print("Contraseña: password123")
    print("IP para acceder a la web:", ap.ifconfig()[0])

# Llamamos a la función al encender
setup_ap()
