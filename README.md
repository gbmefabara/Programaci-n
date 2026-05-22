# Guía de Usuario - WebSockets ESP32

Este proyecto permite ejecutar una aplicación web con WebSockets en una placa **ESP32** utilizando **Thonny** como entorno de desarrollo.

## 📋 Requisitos

- **Placa ESP32** con puerto USB
- **Thonny IDE** instalado en tu computadora
- Cable USB para conectar la ESP32
- Los tres archivos esenciales:
  - `boot.py` - Configuración inicial
  - `main.py` - Código principal de la aplicación
  - `index.html` - Interfaz web

## 🛠️ Instalación de Thonny

1. Descarga Thonny desde [https://thonny.org/](https://thonny.org/)
2. Instala la aplicación en tu computadora
3. Ejecuta Thonny

## 📱 Configuración de Thonny para ESP32

### Paso 1: Conectar la ESP32
1. Conecta tu placa ESP32 a la computadora mediante un cable USB
2. Abre Thonny
3. Ve a **Tools** → **Options** (o **Herramientas** → **Opciones** si está en español)

### Paso 2: Seleccionar el intérprete correcto
1. En la ventana de opciones, ve a la pestaña **Interpreter**
2. En el dropdown **Which interpreter or device to use?**, selecciona:
   - **MicroPython (ESP32)**
3. En **Which port?**, selecciona el puerto COM donde está conectada tu ESP32 (ej: COM3, COM4), es recomendable que selecciones *Intenta detectar el puerto automaticamente* debido a que si cambias de puerto no debes volver a modificarlo
4. Haz clic en **OK** para guardar los cambios

> **Nota:** Si no aparece el puerto COM, asegúrate de que:
> - La ESP32 está conectada correctamente
> - Tienes los drivers USB instalados

## 📁 Estructura de Archivos en la ESP32

Cuando cargues los archivos, deben estar en la raíz de la ESP32 con esta estructura:

```
/
├── boot.py
├── main.py
└── index.html
```

### Thonny 

1. En Thonny, abre el archivo `boot.py`:
   - Archivo → Abrir → Selecciona `boot.py`

2. Con el archivo abierto, haz clic derecho en el área de texto y selecciona:
   - **Save as...** → **MicroPython device**
   - Asegúrate de que el nombre sea `boot.py`
   - Haz clic en **OK**

3. Repite el proceso para `main.py`:
   con su respectivo nombre

4. Para `index.html`:
   - Abre `index.html` (si no se abre, usa un editor de texto)
   - En Thonny, copia el contenido completo
   - Abre la terminal Thonny (parte inferior)
   - Usa el siguiente código para crear el archivo:

```python
with open('index.html', 'w') as f:
    f.write('''[Aquí va el contenido de index.html]''')
```

Alternativamente, puedes usar el File Manager de Thonny:
- En la parte inferior, selecciona la pestaña **Files**
- Haz clic en el botón + para agregar archivos a la ESP32

## 📶 Configurar WiFi para Conectarse a Tu Red 

Para que la ESP32 se conecte a la **misma red WiFi que tu teléfono**, necesitas cambiar dos valores en el archivo `boot.py`:

### Paso 1: Abrir boot.py en Thonny
1. En Thonny, haz clic en **File** → **Open** (o **Archivo** → **Abrir**)
2. Selecciona el archivo `boot.py` de tu computadora

### Paso 2: Encontrar la Línea de Configuración WiFi
Busca la siguiente línea en `boot.py` (normalmente está alrededor de la línea 60):

```python
sta.connect('NETLIFE-NELSON', 'Emily2008')
```

### Paso 3: Cambiar el Nombre y Contraseña de WiFi
Reemplaza los valores entre comillas:

**Antes (configuración actual):**
```python
sta.connect('NETLIFE-NELSON', 'Emily2008')
```

**Después (tu red WiFi):**
> - Reemplaza `NETLIFE-NELSON` con el SSID (nombre) de tu red WiFi
> - Reemplaza `Emily2008` con la contraseña de tu red WiFi
> - Asegúrate de mantener las comillas simples ( ' ' )
> - Respeta mayúsculas y minúsculas (el nombre de WiFi es sensible a mayúsculas)
> - No dejes espacios innecesarios

### Paso 4: Guardar los Cambios
1. Presiona **Ctrl + S** para guardar los cambios locales
2. Haz clic derecho en el área de texto y selecciona **Save as...** → **MicroPython device**
3. Guarda como `boot.py` en la ESP32


## ▶️ Ejecutando el Programa

1. Una vez que los tres archivos están en la ESP32 y has configurado el WiFi, presiona el botón de **Run** en Thonny (▶️)
   - Thonny ejecutará automáticamente `boot.py` primero, luego `main.py`

2. Observa la terminal de Thonny para ver los mensajes de inicio

3. Cuando veas el mensaje con la **dirección IP** (ejemplo: `http://192.168.1.100`), la ESP32 estará lista

4. La ESP32 ahora estará ejecutando tu aplicación conectada a tu red WiFi

## 🌐 Accediendo a la Interfaz Web

Una vez que `main.py` está corriendo:

1. La ESP32 se conectará a una red WiFi
2. Abre tu navegador web
3. Ingresa la dirección IP de tu ESP32 (se mostrará en la terminal de Thonny)
4. Verás la interfaz cargada desde `index.html`

## 🔄 Actualizando el Código

Para realizar cambios en tu código:

1. Edita los archivos Python en Thonny
2. Guarda los cambios locales (Ctrl + S)
3. Guarda en la ESP32 nuevamente (Clic derecho → Save as → MicroPython device)
4. Presiona el botón **Stop** (⏹️) en Thonny
5. Presiona el botón **Run** (▶️) para reiniciar

## 📝 Notas Importantes

- **boot.py** se ejecuta automáticamente al encender la ESP32
- **main.py** contiene el código principal de tu aplicación
- **index.html** es servido por el servidor web en la ESP32
- Asegúrate de usar nombres de archivo exactos (sensibles a mayúsculas)
- Si la ESP32 deja de responder, desconéctala y vuelve a conectarla

## ❓ Solución de Problemas

**Problema:** La ESP32 no aparece en Thonny
- Solución: Instala los drivers CH340 o CP2102 según tu ESP32 (controlador de sofware)

**Problema:** No puedo guardar archivos en la ESP32
- Solución: Asegúrate de que el intérprete está correctamente seleccionado y la ESP32 está conectada

**Problema:** El programa no se ejecuta automáticamente
- Solución: Verifica que `boot.py` esté correctamente cargado y contiene el código de inicio

---

**¡Listo! Ya puedes comenzar a usar tu aplicación WebSockets en la ESP32.**
