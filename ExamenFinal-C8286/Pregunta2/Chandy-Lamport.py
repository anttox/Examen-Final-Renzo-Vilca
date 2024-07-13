import threading
import time

# Clase para el algoritmo de Chandy-Lamport
class ChandyLamport:
    def __init__(self, robots):
        # Iniciamos los robots, el estado, los canales y los marcadores recibidos
        self.robots = robots
        self.state = {robot: None for robot in robots}
        self.channels = {robot: {} for robot in robots}
        self.marker_received = {robot: False for robot in robots}

    # Enviamos un marcador a los vecinos del robot actual
    def send_marker(self, robot):
        for neighbor in self.robots[robot]:
            self.channels[neighbor][robot] = 'marker'
            if not self.marker_received[neighbor]:
                self.receive_marker(neighbor)

    # Recibimos un marcador y capturamos el estado si es el primer marcador recibido
    def receive_marker(self, robot):
        if not self.marker_received[robot]:
            self.marker_received[robot] = True
            self.state[robot] = self.capture_state(robot)
            self.send_marker(robot)

    # Capturamos el estado del robot
    def capture_state(self, robot):
        return f"Estado de {robot} capturado"

    # Iniciamos la toma de instantanea desde un robot iniciador
    def initiate_snapshot(self, initiator):
        self.receive_marker(initiator)

# Ejemplo de uso
robots = {
    'Robot1': ['Robot2', 'Robot3'],
    'Robot2': ['Robot1', 'Robot3'],
    'Robot3': ['Robot1', 'Robot2']
}
chandy_lamport = ChandyLamport(robots)
chandy_lamport.initiate_snapshot('Robot1')
print(chandy_lamport.state)
