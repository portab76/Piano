import ast
from flask import Flask, request, jsonify
import json
import threading
import time
import pygame
import pygame.midi
import os
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={
    r"/instrumentos": {"origins": "*"},
    r"/tocar_nota": {"origins": "*"},
    r"/enviar_pistas": {"origins": "*"},
    r"/cambiar_instrumento": {"origins": "*"},
    r"/stop": {"origins": "*"},
    r"/pistas": {"origins": "*"},
    r"/notas": {"origins": "*"}
})
playing = False
stop_event = threading.Event()
notas_activas_set = set()

# Inicializar pygame y pygame.midi
pygame.init()
pygame.midi.init()

# Abrir el dispositivo MIDI
midi_out = pygame.midi.Output(3)

def convertir_nota_a_numero(nota):
    notas = {
        'A0': 21, 'A#0': 22, 'B0': 23,
        'C1': 24, 'C#1': 25, 'D1': 26, 'D#1': 27, 'E1': 28, 'F1': 29, 'F#1': 30, 'G1': 31, 'G#1': 32, 'A1': 33, 'A#1': 34, 'B1': 35,
        'C2': 36, 'C#2': 37, 'D2': 38, 'D#2': 39, 'E2': 40, 'F2': 41, 'F#2': 42, 'G2': 43, 'G#2': 44, 'A2': 45, 'A#2': 46, 'B2': 47,
        'C3': 48, 'C#3': 49, 'D3': 50, 'D#3': 51, 'E3': 52, 'F3': 53, 'F#3': 54, 'G3': 55, 'G#3': 56, 'A3': 57, 'A#3': 58, 'B3': 59,
        'C4': 60, 'C#4': 61, 'D4': 62, 'D#4': 63, 'E4': 64, 'F4': 65, 'F#4': 66, 'G4': 67, 'G#4': 68, 'A4': 69, 'A#4': 70, 'B4': 71,
        'C5': 72, 'C#5': 73, 'D5': 74, 'D#5': 75, 'E5': 76, 'F5': 77, 'F#5': 78, 'G5': 79, 'G#5': 80, 'A5': 81, 'A#5': 82, 'B5': 83,
        'C6': 84, 'C#6': 85, 'D6': 86, 'D#6': 87, 'E6': 88, 'F6': 89, 'F#6': 90, 'G6': 91, 'G#6': 92, 'A6': 93, 'A#6': 94, 'B6': 95,
        'C7': 96, 'C#7': 97, 'D7': 98, 'D#7': 99, 'E7': 100, 'F7': 101, 'F#7': 102, 'G7': 103, 'G#7': 104, 'A7': 105, 'A#7': 106, 'B7': 107,
        'C8': 108
    }
    return notas.get(nota)
@app.route('/notas', methods=['GET'])
def notas_activas():
    global notas_activas_set
    return jsonify(list(notas_activas_set))

@app.route('/tocar_nota', methods=['POST'])
def tocar_nota():
    data = request.get_json()
    midi_out.set_instrument(int(data['instrumento']))
    note = data['note']
    action = data['action']
    note_number = convertir_nota_a_numero(note)
    if action == 'press':
        midi_out.note_on(note_number, 127)
    elif action == 'release':
        midi_out.note_off(note_number, 127)
    return '', 204

@app.route('/instrumentos', methods=['GET'])
def obtener_instrumentos():
    try:
        filename = os.path.join(os.getcwd(), 'instrumentos.json')
        with open(filename, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return str(e), 500

@app.route('/pistas', methods=['GET'])
def pistas():
    try:
        filename = os.path.join(os.getcwd(), 'piano.json')
        with open(filename, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return str(e), 500
    
@app.route('/cambiar_instrumento', methods=['POST'])
def cambiar_instrumento():
    data = request.get_json()
    instrumento = int(data['instrumento'])
    midi_out.set_instrument(instrumento)
    return '', 204

# Ruta para recibir el esquema JSON y reproducir la canción
@app.route('/enviar_pistas', methods=['POST'])
def enviar_pistas():
    global playing
    global notas_activas_set
    if playing:
        return "Already playing"
    data = request.get_json()
    pistas_procesadas = json.loads(data['pistas'])
    if not pistas_procesadas:
        return "Invalid JSON"
    playing = True
    stop_event.clear()
    notas_activas_set.clear()
    threading.Thread(target=play_tracks, args=(pistas_procesadas,)).start()
    return "Playing"

# Función para reproducir las pistas procesadas
def play_tracks(pistas_procesadas):
    global playing 
    slowdown_factor = 3  # Factor de ralentización
    for pista in pistas_procesadas:
        for note in pista['notes']:
            notas_activas_set.add(note['note'])
            if stop_event.is_set():
                playing = False
                return
            if note['type'] == 'note_on':
                play_note(note['note'], note['velocity'])
                
            elif note['type'] == 'note_off':
                stop_note(note['note'])
            #time.sleep(note['time'] / 1000.0)  # Convertir tiempo a segundos
            #print (notas_activas_set)
            time.sleep((note['time'] / 1000.0) * slowdown_factor)
            notas_activas_set.discard(note['note'])
    playing = False
    notas_activas_set.add('-1')
# Función para reproducir una nota
def play_note(note, velocity):  
    midi_out.note_on(note, velocity)

# Función para detener una nota
def stop_note(note):
    midi_out.note_off(note, 0)

# Ruta para detener la reproducción
@app.route('/stop', methods=['GET'])
def stop():
    global notas_activas_set
    notas_activas_set.clear()
    global playing
    if not playing:
        return "Not playing"
    stop_event.set()
    playing = False
    return "Stopped"

if __name__ == '__main__':
    app.run(debug=True)

# Cerrar el dispositivo MIDI al finalizar
def cleanup():
    midi_out.close()
    pygame.midi.quit()
    pygame.quit()

import atexit
atexit.register(cleanup)