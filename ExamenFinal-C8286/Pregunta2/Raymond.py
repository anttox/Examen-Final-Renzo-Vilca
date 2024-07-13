# Clase para el algoritmo de Raymond
class Raymond:
    def __init__(self, nodes, initial_token_holder):
        # Iniciamos los nodos, el poseedor inicial del token y la cola de solicitudes
        self.nodes = nodes
        self.token_holder = initial_token_holder
        self.request_queue = {node: [] for node in nodes}
        self.token = {initial_token_holder: True}

    # Solicitamos el token
    def request(self, node):
        if not self.token.get(node, False):
            self.request_queue[self.token_holder].append(node)
            self.pass_token()

    # Pasamos el token al siguiente nodo en la cola de solicitudes
    def pass_token(self):
        if self.request_queue[self.token_holder]:
            next_node = self.request_queue[self.token_holder].pop(0)
            self.token[next_node] = True
            self.token[self.token_holder] = False
            self.token_holder = next_node

# Ejemplo de uso
nodes = ['Node1', 'Node2', 'Node3']
raymond = Raymond(nodes, 'Node1')
raymond.request('Node2')
raymond.pass_token()
print(raymond.token)
