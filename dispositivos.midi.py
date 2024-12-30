import pygame.midi

pygame.midi.init()

# Mostrar todos los dispositivos MIDI disponibles
for i in range(pygame.midi.get_count()):
    info = pygame.midi.get_device_info(i)
    name = info[1].decode('utf-8')  # El nombre del dispositivo
    print(f"Dispositivo {i}: {name}")

pygame.midi.quit()
