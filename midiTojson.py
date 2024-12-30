import mido
import json
import os

def midi_to_json(filepath):
    mid = mido.MidiFile(filepath)
    pistas_procesadas = []
    for i, track in enumerate(mid.tracks):
        pista = {
            'track': i,
            'notes': []
        }
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                print(msg);
                pista['notes'].append({
                    'type': msg.type,
                    'note': msg.note,
                    'velocity': msg.velocity,
                    'time': msg.time
                })

        pistas_procesadas.append(pista)
    return pistas_procesadas

def save_json(data, filepath):
    json_path = filepath.replace('.mid', '.json')
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == '__main__':
    midi_filepath = r'C:\Code\mid\ray_charles_style.mid'
    pistas_procesadas = midi_to_json(midi_filepath)
    save_json(pistas_procesadas, midi_filepath)
    print(f"Archivo JSON guardado en {midi_filepath.replace('.mid', '.json')}")