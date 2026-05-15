// Obtenemos el elemento HTML donde mostramos el estado de la conexión
const statusDiv = document.getElementById('status');

/**
 * Función para enviar un comando al servidor ESP32
 * @param {string} cmd - El comando a enviar ('up', 'down', 'left', 'right', 'stop')
 */
function sendCommand(cmd) {
    const url = `/${cmd}`;
    
    // Usamos Fetch API para hacer la petición asíncrona
    fetch(url)
        .then(response => {
            if (response.ok) {
                // Si la respuesta es exitosa (200 OK)
                statusDiv.innerHTML = "✅ Conectado (" + cmd.toUpperCase() + ")";
                statusDiv.classList.add('connected');
            } else {
                // Hubo un error del servidor
                statusDiv.innerHTML = "⚠️ Error en respuesta";
                statusDiv.classList.remove('connected');
            }
        })
        .catch(error => {
            // Error de red (ESP32 desconectado)
            console.error('Error enviando comando:', error);
            statusDiv.innerHTML = "⚠️ Error en respuesta";
            statusDiv.classList.remove('connected');
        });
}

// Para arrancar, podemos hacer un 'ping' para verificar conexión inicial
sendCommand('stop');
