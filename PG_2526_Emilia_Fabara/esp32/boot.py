# ==============================================================================
# boot.py - Menú de Inicio y Conexión WiFi
# ==============================================================================
# Este archivo es lo primero que ejecuta la ESP32 al encenderse.
# Contiene:
#   1. Un menú interactivo para elegir modo de ejecución o programación.
#   2. La conexión WiFi en modo Estación (STA) usando DHCP.
# Al finalizar, MicroPython ejecutará automáticamente main.py.
# ==============================================================================

#En este apartado se estan importando las librerías para el funcionamiento del código, como network para la conexión WiFi, time para manejar tiempos de espera, sys para interactuar con el sistema y uselect para manejar eventos de entrada/salida sin bloqueo.
import network
import time
import sys
import uselect

# ==============================================================================
# 1. MENÚ DE INICIO
# ==============================================================================
def menu_inicio(timeout_segundos=5): #Esperará 5 segundos para dar una respuesta
    """
    Muestra un menú en la terminal. Avanza automáticamente si no hay respuesta.
    """
    print("\n" + "="*40)
    print("      SISTEMA DE CONTROL - GRÚA TORRE")
    print("="*40)
    print("1. Iniciar sistema normalmente (Modo Ejecución)")
    print("2. Detener en modo programación (Liberar REPL)")
    print(f"Selecciona una opción (Avanza a opción 1 en {timeout_segundos}s)...")
    
    # Configurar la terminal para escuchar la entrada del usuario sin bloquear
    poller = uselect.poll()
    poller.register(sys.stdin, uselect.POLLIN)
    
    tiempo_inicio = time.time()
    while (time.time() - tiempo_inicio) < timeout_segundos:
        # Revisar si hay datos en la terminal (espera hasta 100ms por ciclo)
        if poller.poll(100):
            caracter = sys.stdin.read(1)
            if caracter == '1':
                print("\n-> Opción 1 seleccionada. Iniciando...")
                return True
            elif caracter == '2':
                print("\n-> Opción 2 seleccionada. Modo programación activo.")
                print("Consola REPL liberada. Puedes subir o modificar archivos.")
                return False
    
    # Si se agota el tiempo sin respuesta, asumimos modo autónomo
    print("\n-> Tiempo de espera agotado. Iniciando de forma automática...")
    return True

# ==============================================================================
# 2. CONEXIÓN WIFI (Modo Estación - DHCP)
# ==============================================================================
def connect_wifi():
    """Conecta la ESP32 a una red WiFi existente usando DHCP."""
    print("Iniciando Modo Estación (STA)...")
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.disconnect() # Forzar desconexión para limpiar configuraciones antiguas
    time.sleep(0.5)
    
    print("Conectando a la red WiFi doméstica...")
    print("[TELEMETRÍA] Usando DHCP (El router asignará la IP automáticamente)")

    # IMPORTANTE: Cambia estos valores por el nombre (SSID) y contraseña de tu WiFi
    sta.connect('NETLIFE-NELSON', 'Emily2008')
    
    # Esperamos a que se conecte (máximo 20 segundos)
    intentos = 0
    while not sta.isconnected() and intentos < 20:
        time.sleep(1)
        print(".", end="")
        intentos += 1
        
    if not sta.isconnected():
        print("\nError: No se pudo conectar al WiFi. Revisa el nombre y contraseña.")
        return
    
    # Conexión exitosa: mostramos la IP asignada
    print("\n¡Conexión WiFi exitosa!")
    ip = sta.ifconfig()[0]
    print("=======================================================")
    print("🌐 IP OBTENIDA PARA ACCEDER DESDE EL TELÉFONO:")
    print(f"   http://{ip}")
    print("=======================================================")
    print("Servidor listo para iniciar...\n")

# ==============================================================================
# 3. FLUJO DE INICIO
# ==============================================================================
# Ejecutamos el menú ANTES de conectar al WiFi.
# Si elige opción 1 (o se agota el tiempo), conecta WiFi y deja que
# MicroPython ejecute main.py automáticamente.
# Si elige opción 2, detenemos todo para liberar la consola REPL.

if menu_inicio(timeout_segundos=5):
    connect_wifi()
    # MicroPython ejecutará main.py automáticamente después de boot.py
else:
    print("\nSistema en modo de espera. Puedes modificar archivos y ejecutar comandos.")
    sys.exit()