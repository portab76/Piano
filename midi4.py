from flask import Flask, request, jsonify
import json
import threading
import time
import pygame
import pygame.midi

app = Flask(__name__)
playing = False
stop_event = threading.Event()

# Inicializar pygame y pygame.midi
pygame.init()
pygame.midi.init()

# Abrir el dispositivo MIDI
midi_out = pygame.midi.Output(3)

# Ruta para reproducir el archivo JSON guardado
@app.route('/reproducir_json', methods=['POST'])
def reproducir_json():
    global playing
    if playing:
        return "Already playing"
    json_filepath = r'C:\Code\mid\note.json'
    with open(json_filepath, 'r') as json_file:
        pistas_procesadas = json.load(json_file)
    if not pistas_procesadas:
        return "Invalid JSON"
    playing = True
    stop_event.clear()
    threading.Thread(target=play_tracks, args=(pistas_procesadas,)).start()
    return "Playing"

# Función para reproducir las pistas procesadas
def play_tracks(pistas_procesadas):
    global playing
    for pista in pistas_procesadas:
        for note in pista['notes']:
            if stop_event.is_set():
                playing = False
                return
            if note['type'] == 'note_on':
                play_note(note['note'], note['velocity'])
            elif note['type'] == 'note_off':
                stop_note(note['note'])
            time.sleep(note['time'] / 1000.0)  # Convertir tiempo a segundos
    playing = False

# Función para reproducir una nota
def play_note(note, velocity):
    midi_out.note_on(note, velocity)

# Función para detener una nota
def stop_note(note):
    midi_out.note_off(note, 0)

# Ruta para detener la reproducción
@app.route('/stop', methods=['POST'])
def stop():
    global playing
    if not playing:
        return "Not playing"
    stop_event.set()
    playing = False
    return "Stopped"

if __name__ == '__main__':
    reproducir_json()
    #app.run(debug=True)


# Cerrar el dispositivo MIDI al finalizar
def cleanup():
    midi_out.close()
    pygame.midi.quit()
    pygame.quit()

import atexit
atexit.register(cleanup)
