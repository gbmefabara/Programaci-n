# OpenSpec: Arquitectura de Software Grúa Torre

## 1. Arquitectura General del Sistema
El sistema consta de dos controladores independientes que se comunican mediante protocolo serie (UART).

*   **Frontend (Cliente):** Interfaz web (HTML/CSS/JS) accesible desde cualquier navegador.
*   **Backend / Interfaz de Red (ESP32):** Servidor Web (uasyncio), genera red WiFi AP, recibe comandos HTTP y los traduce a comandos UART.
*   **Controlador Físico (Arduino Nano):** Recibe datos UART (del ESP32) y datos Analógicos (de Joysticks locales), consolida las intenciones de movimiento y controla los Drivers de los motores.

### Diagrama Lógico de Flujo
Página Web -> (HTTP Fetch) -> ESP32 -> (UART TX/RX) -> Arduino Nano -> (PWM/Digital) -> Drivers -> Motores

## 2. Mapa de Pines (Pinout)

### ESP32 (MicroPython)
| Pin / GPIO | Función | Conexión a |
| :--- | :--- | :--- |
| GPIO 17 | UART TX2 | Arduino Nano RX (D0) |
| GPIO 16 | UART RX2 | Arduino Nano TX (D1) - *No usado en esta versión* |
| GND | Tierra compartida | Arduino Nano GND |

### Arduino Nano (C++)
| Pin | Función | Conexión a |
| :--- | :--- | :--- |
| **D0 (RX)** | Comunicación UART | ESP32 TX (GPIO 17) |
| **A0** | Joystick X (Analógico) | Joystick Carro (Eje X) |
| **A1** | Joystick Y (Analógico) | Joystick Elevación (Eje Y) |
| **A2** | Joystick Z (Analógico) | Joystick Giro (Eje X o Y) |
| **D2, D4, D3** | Driver TB6612FNG (AIN1, AIN2, PWMA) | Motor Carro (N20) |
| **D7, D8, D5** | Driver TB6612FNG (BIN1, BIN2, PWMB) | Motor Elevación (N20) |
| **D9, D10** | Driver DRV8825 (STEP, DIR) | Motor Giro Torre (NEMA 17) |

## 3. Protocolo de Comunicación (Endpoints y UART)

El sistema utiliza endpoints HTTP simplificados para enviar la intención de movimiento de forma remota. El ESP32 traduce estos endpoints a caracteres únicos que envía por UART.

| Endpoint Web (HTTP GET) | Comando UART (Char + `\n`) | Acción Resultante en Arduino |
| :--- | :--- | :--- |
| `/U` | `U\n` | Sube la carga (Elevación positiva) |
| `/D` | `D\n` | Baja la carga (Elevación negativa) |
| `/L` | `L\n` | Gira torre a la Izquierda |
| `/R` | `R\n` | Gira torre a la Derecha |
| `/S` | `S\n` | Detiene todo movimiento remoto |

## 4. Flujo de Datos y Seguridad (Timeout)
1.  **Pulsación de Botón:** El usuario presiona el botón "Subir" en la web.
2.  **Petición Fetch:** Se lanza un `GET /U` en segundo plano.
3.  **Procesamiento ESP32:** El ESP32 recibe el `GET /U`, no recarga la página, y envía por el pin 17 la letra `U\n`.
4.  **Recepción Arduino:** El Arduino captura `U` por el puerto serial.
5.  **Reloj de Seguridad:** El Arduino inicia un temporizador de *500ms*.
6.  **Suma de intenciones:** El Arduino ignora el Joystick (si la intención remota es fuerte) y activa los pines correspondientes del TB6612FNG hacia el motor de Elevación.
7.  **Timeout:** Si el usuario cierra la página o pierde conexión, no llegarán más comandos `U`. Pasados 500ms, el Arduino sobrescribe el comando interno a `S` (Stop) y detiene el motor automáticamente.
