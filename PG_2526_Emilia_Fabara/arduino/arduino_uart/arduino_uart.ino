/*
 * ==============================================================================
 * FASE 2 - Comunicación UART (ESP32 a Arduino) - Arduino Nano
 * ==============================================================================
 * Este código recibe los comandos enviados por la ESP32 y los imprime
 * en el Monitor Serie del Arduino IDE para comprobar que llegan correctamente.
 *
 * Explicación de Hardware:
 * - RX (D0): En este pin el Arduino recibe la información. Conéctalo
 *   al TX (GPIO 17) del ESP32.
 * - GND: ¡No olvides conectar el GND de Arduino con el GND del ESP32!
 * ==============================================================================
 */

// 1. Función de configuración inicial
void setup() {
  // Iniciamos la comunicación serial hacia la computadora (Monitor Serie)
  // Utilizamos 9600 baudios (misma velocidad que la ESP32).
  // En el Arduino Nano, los pines RX (D0) y TX (D1) están vinculados al Serial.
  Serial.begin(9600);
  
  // Imprimimos un mensaje de bienvenida
  Serial.println("Arduino Nano Iniciado.");
  Serial.println("Esperando comandos del ESP32...");
}

// 2. Bucle principal
void loop() {
  // Comprobamos si hay información llegando por el puerto Serial (desde el ESP32)
  if (Serial.available() > 0) {
    
    // Leemos la información entrante hasta encontrar el salto de línea '\n'
    // que la ESP32 añadió al final de cada mensaje.
    String comandoRecibido = Serial.readStringUntil('\n');
    
    // Limpiamos el texto por si hay espacios invisibles
    comandoRecibido.trim(); 
    
    // Mostramos el comando recibido en el Monitor Serie de la computadora
    Serial.print("Comando recibido: ");
    Serial.println(comandoRecibido);
    
    // Aquí es donde, en el futuro, compararemos el comando
    // para mover los motores. Por ejemplo:
    if (comandoRecibido == "LEFT") {
      Serial.println(" -> Acción simulada: Moviendo grúa a la IZQUIERDA");
    } else if (comandoRecibido == "RIGHT") {
      Serial.println(" -> Acción simulada: Moviendo grúa a la DERECHA");
    } else if (comandoRecibido == "UP") {
      Serial.println(" -> Acción simulada: Subiendo carga");
    } else if (comandoRecibido == "DOWN") {
      Serial.println(" -> Acción simulada: Bajando carga");
    } else if (comandoRecibido == "STOP") {
      Serial.println(" -> Acción simulada: DETENIENDO TODOS LOS MOTORES");
    } else {
      Serial.println(" -> Comando desconocido");
    }
    
    Serial.println("-------------------------------------------------");
  }
}
