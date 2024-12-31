# Piano MiDI Json con Frontend html Interactivo

![Piano html optimizado pantalla táctitles](https://youtube.com/shorts/HpyIE5fVtbc?si=3noHl-wVBYNZtm66)

Este proyecto combina un servidor Python (`PianoServer.py`) con una interfaz gráfica en HTML para simular y controlar un piano virtual con múltiples pistas y reproducción MIDI. Está diseñado para proporcionar una experiencia de usuario interactiva que permite reproducir partituras en formato JSON y visualizar animaciones sincronizadas de las teclas.

![Piano html optimizado pantalla táctitles](https://github.com/portab76/Piano/blob/main/piano.png?raw=true)


---

## Descripción del Proyecto

### PianoServer.py
El programa `PianoServer.py` actúa como el backend del sistema. Sus principales funciones son:

- Gestionar un servidor HTTP para interactuar con el frontend.
- Procesar las pistas y partituras enviadas desde la interfaz.
- Reproducir archivos MIDI utilizando un dispositivo MIDI conectado o un sintetizador virtual.

**Requisito adicional:** Si no tienes un dispositivo MIDI físico, necesitas instalar el software **CoolSoft VirtualMIDISynth (versión 2.13.9)** para emular un sintetizador MIDI. Este software está disponible en su [página oficial](https://coolsoft.altervista.org/en/virtualmidisynth).

### Frontend (HTML)
La interfaz gráfica permite:

- Seleccionar instrumentos MIDI disponibles.
- Visualizar y reproducir partituras con una animación sincronizada de las teclas del piano.
- Crear y enviar partituras en formato JSON directamente desde el navegador.

---

## Requisitos Previos

1. Python 3.8 o superior.
2. Librerías requeridas (instalables con `pip`):
   - Flask
   - mido
   - python-rtmidi
3. Un dispositivo MIDI físico o el programa **CoolSoft VirtualMIDISynth** instalado.

## Cómo Ejecutar el Proyecto

python PianoServer.py
Abre el archivo piano.html en un navegador.
Configura la URL del servidor (http://127.0.0.1:5000) en el campo correspondiente.
Usa la interfaz para cargar instrumentos, enviar pistas y reproducir partituras con animación sincronizada.

## Ejemlo de Partitura JSON
{
    "pista1": {
        "notas": [
            { "nota": "C3", "duracion": "W" },
            { "nota": "E3", "duracion": "W" }
        ],
        "instrumento": 1
    },
    "pista2": {
        "notas": [
            { "nota": "", "duracion": "H" },
            { "nota": "B3", "duracion": "H" }
        ],
        "instrumento": 2
    }
}
- Duracion de las notas:

Redonda (W):	 	 2.0 segundos
Blanca (H): 		 1.0 segundo
Negra (Q): 			 0.5 segundos
Corchea (E): 		 0.2 segundos
Semicorchea (S): 0.1 segundos
Fusa (T): 		   0.06 segundos
Semifusa (X):		 0.03 segundos
