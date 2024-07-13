# Clase para relojes vectoriales
class VectorClock:
    def __init__(self, nodes):
        # Iniciamos los nodos y sus relojes
        self.nodes = nodes
        self.clock = {node: [0]*len(nodes) for node in nodes}

    # Registramos un evento en un nodo
    def event(self, node):
        index = self.nodes.index(node)
        self.clock[node][index] += 1

    # Enviamos un mensaje de un nodo a otro
    def send_message(self, sender, receiver):
        index_sender = self.nodes.index(sender)
        index_receiver = self.nodes.index(receiver)
        self.clock[receiver] = [max(self.clock[sender][i], self.clock[receiver][i]) for i in range(len(self.nodes))]
        self.clock[receiver][index_receiver] += 1

# Ejemplo de uso
nodes = ['Node1', 'Node2', 'Node3']
vector_clock = VectorClock(nodes)
vector_clock.event('Node1')
vector_clock.send_message('Node1', 'Node2')
print(vector_clock.clock)
