import threading
import queue
import time
from datetime import datetime

# Clase para representar un mensaje en el sistema distribuido
class Message:
    def __init__(self, sender, content):
        self.sender = sender  # Remitente del mensaje
        self.content = content  # Contenido del mensaje
        self.timestamp = datetime.now()  # Marca de tiempo del mensaje

    def __repr__(self):
        return f"Mensaje(remitente={self.sender}, contenido={self.content}, timestamp={self.timestamp})"

# Clase para representar un nodo en el sistema distribuido
class Node:
    def __init__(self, node_id, total_nodes, network):
        self.node_id = node_id  # Identificador del nodo
        self.total_nodes = total_nodes  # Numero total de nodos en la red
        self.network = network  # Referencia a la red
        self.clock = 0  # Reloj logico del nodo
        self.request_queue = queue.PriorityQueue()  # Cola de solicitudes para Ricart-Agrawala
        self.replies_needed = 0  # Contador de respuestas necesarias para Ricart-Agrawala
        self.ricart_agrawala_lock = threading.Lock()  # Bloqueo para la exclusion mutua
        self.dijkstra_scholten_parent = None  # Nodo padre en Dijkstra-Scholten
        self.dijkstra_scholten_children = []  # Nodos hijos en Dijkstra-Scholten
        self.dijkstra_scholten_active = False  # Estado de actividad de Dijkstra-Scholten
        self.memory = []  # Memoria del nodo
        self.gc = CheneyCollector(100)  # Recolector de basura Alogitmo Cheney
        self.gc.add_root(0)  # Añadimos la raiz al recolector de basura
        self.running = True  # Estado de ejecucion del nodo

    def send_message(self, receiver, content):
        # Enviamos un mensaje a otro nodo
        message = Message(self.node_id, content)
        print(f"El nodo {self.node_id} envia un mensaje al nodo {receiver}: {content}")
        self.network.send_message(self.node_id, receiver, message)

    def receive_message(self, message):
        # Recibimos un mensaje de otro nodo
        print(f"El nodo {self.node_id} recibio un mensaje del nodo {message.sender}: {message.content}")
        self.clock = max(self.clock, message.timestamp.timestamp()) + 1
        if message.content.startswith("REQUEST"):
            self.request_queue.put((message.timestamp.timestamp(), message))
            self.send_message(message.sender, "REPLY")
        elif message.content == "REPLY":
            self.replies_needed -= 1
        elif message.content == "TERMINATE":
            self.dijkstra_scholten_terminate(message.sender)
        elif message.content == "START":
            self.dijkstra_scholten_start()

    def request_resource(self):
        # Solicitamos acceso a un recurso compartido (Ricart-Agrawala)
        self.ricart_agrawala_lock.acquire()
        self.clock += 1
        self.replies_needed = self.total_nodes - 1
        print(f"El nodo {self.node_id} solicita recurso en el momento {self.clock}")
        for node_id in range(self.total_nodes):
            if node_id != self.node_id:
                self.send_message(node_id, f"REQUEST:{self.clock}")
        while self.replies_needed > 0:
            time.sleep(0.1)
        self.ricart_agrawala_lock.release()

    def release_resource(self):
        # Liberamos el recurso compartido (Ricart-Agrawala)
        print(f"El nodo {self.node_id} libera recurso")
        while not self.request_queue.empty():
            _, message = self.request_queue.get()
            self.send_message(message.sender, "REPLY")

    def synchronize_clock(self):
        # Sincronizamos el reloj logico con otros nodos
        print(f"El nodo {self.node_id} sincroniza el reloj")
        for node_id in range(self.total_nodes):
            if node_id != self.node_id:
                self.send_message(node_id, "SYNC")

    def dijkstra_scholten_start(self):
        # Iniciamos la deteccion de terminacion de procesos (Dijkstra-Scholten)
        print(f"El nodo {self.node_id} inicia la deteccion de terminacion Dijkstra-Scholten")
        self.dijkstra_scholten_active = True
        for node_id in range(self.total_nodes):
            if node_id != self.node_id:
                self.send_message(node_id, "START")

    def dijkstra_scholten_terminate(self, sender):
        # Manejamos la terminacion de un proceso (Dijkstra-Scholten)
        print(f"El nodo {self.node_id} maneja la terminacion del nodo {sender}")
        if self.dijkstra_scholten_parent is None:
            self.dijkstra_scholten_parent = sender
        else:
            self.dijkstra_scholten_children.append(sender)
        if not self.dijkstra_scholten_children:
            self.send_message(self.dijkstra_scholten_parent, "TERMINATE")
            self.dijkstra_scholten_active = False

    def garbage_collect(self):
        # Realizamos la recoleccion de basura (Cheney)
        print(f"El nodo {self.node_id} realiza la recoleccion de basura")
        self.gc.collect()

    def run(self):
        # Ejecutamos el nodo
        while self.running:
            time.sleep(1)
            self.garbage_collect()
            self.synchronize_clock()
            self.request_resource()
            # Simulamos la ejecucion de una tarea cientifica
            print(f"El nodo {self.node_id} esta realizando una tarea cientifica")
            time.sleep(2)
            self.release_resource()

    def stop(self):
        # Detenemos la ejecucion del nodo
        self.running = False
        self.send_message(self.node_id, "TERMINATE")

# Implementamos el algoritmo de recolección de basura Cheney
class CheneyCollector:
    def __init__(self, size):
        self.size = size
        self.from_space = [None] * size
        self.to_space = [None] * size
        self.root_set = []
        self.free_ptr = 0

    def allocate(self, obj):
        # Asignamos memoria para un objeto
        if self.free_ptr >= self.size:
            self.collect()
            if self.free_ptr >= self.size:
                raise MemoryError("Out of memory")
        addr = self.free_ptr
        self.from_space[addr] = obj
        self.free_ptr += 1
        return addr

    def collect(self):
        # Realizamos la recoleccion de basura
        print("Se inicio la recoleccion de basura")
        self.to_space = [None] * self.size
        to_space_ptr = 0

        # Copiamos objetos del conjunto raiz al to_space
        for i, root in enumerate(self.root_set):
            addr = root['addr']
            to_space_ptr = self.copy(addr, to_space_ptr)
            self.root_set[i]['addr'] = to_space_ptr - 1

        # Procesamos objetos copiados
        scan = 0
        while scan < to_space_ptr:
            obj = self.to_space[scan]
            if isinstance(obj, dict):
                for key, ref in obj.items():
                    if isinstance(ref, int):
                        to_space_ptr = self.copy(ref, to_space_ptr)
                        obj[key] = to_space_ptr - 1
            scan += 1

        # Intercambiamos los espacios de memoria
        self.from_space, self.to_space = self.to_space, self.from_space
        self.free_ptr = to_space_ptr
        print("Recoleccion de basura copletada")

    def copy(self, addr, to_space_ptr):
        # Copiamos un objeto del from_space al to_space si aun no ha sido copiado
        obj = self.from_space[addr]
        if obj is not None and obj not in self.to_space:
            self.to_space[to_space_ptr] = obj
            self.from_space[addr] = None
            to_space_ptr += 1
        return to_space_ptr

    def add_root(self, addr):
        # Agregamos una direccion al conjunto raiz
        self.root_set.append({'addr': addr})

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
        # Enviamos un mensaje a un nodo especifico
        print(f"La red envia un mensaje desde el nodo {sender} al nodo {receiver}: {message.content}")
        self.messages.put((receiver, message))
        self.nodes[receiver].receive_message(message)

    def start(self):
        # Iniciamos la red de nodos
        for thread in self.threads:
            thread.start()

    def stop(self):
        # Detenemos la red de nodos
        for node in self.nodes:
            node.stop()
        for thread in self.threads:
            thread.join()

# Simulacion de la ejecucion de tareas cientificas
network = Network(5)
network.start()

# Deteneos la red de nodos despuus de 10 segundos
time.sleep(10)
network.stop()
