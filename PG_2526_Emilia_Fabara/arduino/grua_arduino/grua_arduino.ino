/*
 * ==============================================================================
 * FASE 4 - Integración Total: grua_arduino.ino
 * ==============================================================================
 * Este código controla todos los motores de la grúa y suma las intenciones
 * del control remoto (vía Web) y del control manual (Joysticks).
 * 
 * Hardware Asignado:
 * - TB6612FNG (Motor Carro y Elevación): D2, D3, D4, D5, D7, D8
 * - DRV8825 (Motor Nema 17 - Giro): D9, D10
 * - Joysticks: A0 (Carro), A1 (Elevación), A2 (Giro)
 * - UART RX: D0 (conectado a TX 17 del ESP32)
 * ==============================================================================
 */

// Librería para mover el motor Nema 17 suavemente (no bloqueante)
#include <AccelStepper.h>

// --- PINES DEL MOTOR NEMA 17 (Giro de la Torre) ---
#define PIN_STEP 9
#define PIN_DIR 10
// Creamos el objeto stepper usando driver de 2 pines (STEP y DIR)
AccelStepper stepper(AccelStepper::DRIVER, PIN_STEP, PIN_DIR);

// --- PINES DEL TB6612FNG (Motores DC N20) ---
// Motor A: Carro (Adelante / Atrás)
#define AIN1 2
#define AIN2 4
#define PWMA 3
// Motor B: Elevación (Subir / Bajar)
#define BIN1 7
#define BIN2 8
#define PWMB 5

// --- PINES DE LOS JOYSTICKS ---
#define JOY_X A0 // Carro
#define JOY_Y A1 // Elevación
#define JOY_Z A2 // Giro de la torre

// --- VARIABLES DE ESTADO (Comandos de la Web) ---
// Guardan la "intención" recibida desde la web
String comandoWeb = "S"; 

// Tiempos para seguridad (Timeout)
unsigned long ultimoComandoWebTime = 0;
const unsigned long TIMEOUT_WEB = 500; // Si no hay comandos en 500ms, detenemos (Seguridad)

void setup() {
  // 1. Iniciar UART
  Serial.begin(9600);
  
  // 2. Configurar pines del TB6612FNG como salidas
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(PWMB, OUTPUT);
  
  // 3. Configurar Stepper
  stepper.setMaxSpeed(1000);   // Velocidad máxima permitida
  stepper.setAcceleration(500); // Aceleración para movimientos suaves
  
  Serial.println("Grúa Iniciada.");
}

void loop() {
  // 1. LEER COMANDOS WEB (Vía UART)
  if (Serial.available() > 0) {
    String entrante = Serial.readStringUntil('\n');
    entrante.trim();
    if (entrante.length() > 0) {
      comandoWeb = entrante;
      ultimoComandoWebTime = millis(); // Actualizamos el reloj de seguridad
    }
  }

  // Comprobar Timeout (si pasa mucho tiempo sin pulsar botón en web, detenemos remoto)
  if (millis() - ultimoComandoWebTime > TIMEOUT_WEB) {
    comandoWeb = "S"; 
  }

  // 2. LEER JOYSTICKS (Intención Local)
  // map(valor, fromLow, fromHigh, toLow, toHigh) convierte la lectura 0-1023 a algo manejable
  int valJoyCarro = analogRead(JOY_X);
  int valJoyElevacion = analogRead(JOY_Y);
  int valJoyGiro = analogRead(JOY_Z);

  // Zona muerta (deadzone) de joysticks para evitar que se mueva solo si no está en el centro perfecto
  int velCarroManual = 0;
  if (valJoyCarro < 400) velCarroManual = -255;
  else if (valJoyCarro > 600) velCarroManual = 255;

  int velElevacionManual = 0;
  if (valJoyElevacion < 400) velElevacionManual = -255;
  else if (valJoyElevacion > 600) velElevacionManual = 255;

  int velGiroManual = 0;
  if (valJoyGiro < 400) velGiroManual = -500; // Velocidad Stepper negativa
  else if (valJoyGiro > 600) velGiroManual = 500;  // Velocidad Stepper positiva

  // 3. SUMAR INTENCIONES (Web + Manual)
  // Variables finales que determinan cómo se mueven los motores
  int intencionCarro = velCarroManual;
  int intencionElevacion = velElevacionManual;
  int intencionGiro = velGiroManual;

  // Si la web nos manda algo, sobrescribimos la intención o la sumamos
  if (comandoWeb == "L") { // Giro Izquierda
    intencionGiro = -500;
  } else if (comandoWeb == "R") { // Giro Derecha
    intencionGiro = 500;
  } else if (comandoWeb == "U") { // Subir
    intencionElevacion = 255;
  } else if (comandoWeb == "D") { // Bajar
    intencionElevacion = -255;
  }
  // (Omitimos movimiento de carro por web si no hay botones en HTML, 
  // pero el joystick sigue activo)

  // 4. APLICAR MOVIMIENTO A LOS MOTORES DC (TB6612FNG)
  moverMotorA(intencionCarro);      // Carro
  moverMotorB(intencionElevacion);  // Elevación

  // 5. APLICAR MOVIMIENTO AL STEPPER (DRV8825)
  if (intencionGiro != 0) {
    // Si queremos girar, ajustamos la velocidad
    stepper.setSpeed(intencionGiro);
    stepper.runSpeed(); // Ejecuta un solo paso SI corresponde (es no bloqueante)
  } else {
    // Detener Stepper suavemente
    stepper.setSpeed(0);
    stepper.runSpeed();
  }
}

// --- FUNCIONES AUXILIARES PARA MOTORES DC ---

void moverMotorA(int velocidad) {
  // Motor A: Carro
  if (velocidad > 0) {
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    analogWrite(PWMA, velocidad);
  } else if (velocidad < 0) {
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH);
    analogWrite(PWMA, -velocidad); // Pasamos valor positivo
  } else {
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, LOW);
    analogWrite(PWMA, 0); // Freno
  }
}

void moverMotorB(int velocidad) {
  // Motor B: Elevación
  if (velocidad > 0) {
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMB, velocidad);
  } else if (velocidad < 0) {
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, HIGH);
    analogWrite(PWMB, -velocidad);
  } else {
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMB, 0); // Freno
  }
}
