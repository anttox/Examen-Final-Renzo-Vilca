import random
import time
from datetime import datetime
import threading
import queue

# Clase para representar un mensaje en el sistema distribuido
class Message:
    def __init__(self, sender, content, msg_type):
        self.sender = sender  # Remitente del mensaje
        self.content = content  # Contenido del mensaje
        self.timestamp = datetime.now()  # Marca de tiempo del mensaje
        self.msg_type = msg_type  # Tipo de mensaje

    def __repr__(self):
        return f"Mensaje(remitente={self.sender}, content={self.content}, timestamp={self.timestamp}, type={self.msg_type})"

# Clase para representar un nodo en el sistema distribuido
class Node:
    def __init__(self, node_id, total_nodes, network):
        self.node_id = node_id  # Identificador del nodo
        self.total_nodes = total_nodes  # Numero total de nodos en la red
        self.network = network  # Referencia a la red
        self.log = []  # Registro de operaciones
        self.commit_index = -1  # Indice de confirmacion en el registro
        self.current_term = 0  # Termino actual en el algoritmo Raft
        self.voted_for = None  # Nodo por el que se ha votado en el termino actual
        self.state = 'follower'  # Estado del nodo (follower, candidate, leader)
        self.votes_received = 0  # Numero de votos recibidos
        self.participating = True  # Estado de participacion del nodo

    def simulate_network_latency(self):
        latency = random.uniform(0.1, 1.0)  # Simulacion de latencia de red
        time.sleep(latency)

    def send_message(self, receiver, content, msg_type):
        self.simulate_network_latency()
        message = Message(self.node_id, content, msg_type)
        self.network.send_message(self.node_id, receiver, message)

    def receive_message(self, message):
        self.simulate_network_latency()
        if not self.participating:
            return
        print(f"El nodo {self.node_id} recibio {message.msg_type} el mensaje del nodo {message.sender}: {message.content}")
        if message.msg_type == "request_vote":
            self.handle_request_vote(message)
        elif message.msg_type == "vote":
            self.handle_vote(message)
        elif message.msg_type == "append_entries":
            self.handle_append_entries(message)

    def handle_request_vote(self, message):
        if self.voted_for is None or self.voted_for == message.sender:
            self.voted_for = message.sender
            self.send_message(message.sender, "vote_granted", "vote")

    def handle_vote(self, message):
        self.votes_received += 1
        if self.votes_received > self.total_nodes // 2:
            self.state = 'leader'
            self.votes_received = 0
            self.send_heartbeat()

    def handle_append_entries(self, message):
        self.log.append(message.content)
        self.commit_index += 1
        self.send_message(message.sender, "ack", "ack")

    def send_heartbeat(self):
        for node_id in range(self.total_nodes):
            if node_id != self.node_id:
                self.send_message(node_id, "heartbeat", "append_entries")

    def run(self):
        while self.participating:
            if self.state == 'leader':
                self.send_heartbeat()
                time.sleep(1)
            else:
                time.sleep(random.uniform(1, 3))
                if random.random() < 0.1:
                    self.state = 'candidate'
                    self.current_term += 1
                    self.voted_for = self.node_id
                    self.votes_received = 1
                    for node_id in range(self.total_nodes):
                        if node_id != self.node_id:
                            self.send_message(node_id, self.current_term, "request_vote")

    def stop(self):
        self.participating = False

# Clase para manejar la red de nodos
class Network:
    def __init__(self, total_nodes):
        self.total_nodes = total_nodes  # Numero total de nodos en la red
        self.nodes = []  # Lista de nodos en la red
        self.messages = queue.Queue()  # Cola de mensajes
        self.threads = []  # Hilos para la ejecucion de nodos

        for node_id in range(total_nodes):
            node = Node(node_id, total_nodes, self)
            self.nodes.append(node)
            thread = threading.Thread(target=node.run)
            self.threads.append(thread)

    def send_message(self, sender, receiver, message):
        print(f"La red envia un mensaje desde el nodo {sender} al nodo {receiver}: {message.content}")
        self.messages.put((receiver, message))
        self.nodes[receiver].receive_message(message)

    def start(self):
        for thread in self.threads:
            thread.start()

    def stop(self):
        for node in self.nodes:
            node.stop()
        for thread in self.threads:
            thread.join()

# Simulacion de la ejecución del sistema distribuido
network = Network(5)
network.start()

# Detener la red de nodos despues de 30 segundos
time.sleep(30)
network.stop()
