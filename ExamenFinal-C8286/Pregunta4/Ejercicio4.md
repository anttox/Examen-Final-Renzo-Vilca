# PARTE1

## Class Message

**__init__:**

- Establece el identificador del remitente (sender).
- Establece el contenido del mensaje (content).
- Establece la marca de tiempo actual (timestamp) en el momento en que se crea el mensaje.
- Establece el tipo de mensaje (msg_type), que puede ser por ejemplo "request_vote", "vote", "append_entries", etc.

![imagen](https://github.com/user-attachments/assets/74b42485-088d-4799-a079-3daf9ca10c96)

**__repr__:**

- Devuelve una cadena de texto que representa el mensaje, incluyendo el remitente, el contenido, la marca de tiempo y el tipo de mensaje.

![imagen](https://github.com/user-attachments/assets/ad5d9558-1156-4868-99fa-ab57a04362e3)

## Class Node

**__init__:**

- Establece los atributos del nodo, incluyendo su identificador (node_id), el número total de nodos (total_nodes), y la referencia a la red (network).
- Inicializa el log de operaciones (log), el índice de confirmación (commit_index), el término actual (current_term), el nodo por el que se ha votado (voted_for), el estado del nodo (state), el número de votos recibidos (votes_received), y el estado de participación (participating).

![imagen](https://github.com/user-attachments/assets/ba9a250f-32ec-4a9a-8560-91f5d609d5f0)

**simulate_network_latency:**

- Genera un retraso aleatorio entre 0.1 y 1.0 segundos.
- Hace que el hilo actual duerma durante ese tiempo para simular la latencia de red.

![imagen](https://github.com/user-attachments/assets/42f5883a-d8ab-4090-b59c-8920388aa820)

**send_message:**

- Llama a simulate_network_latency para añadir un retraso antes de enviar el mensaje.
- Crea una instancia de Message con el remitente, contenido y tipo de mensaje.
- Utiliza el método send_message de la red para enviar el mensaje al nodo receptor.

![imagen](https://github.com/user-attachments/assets/5a079c2e-40e0-4cea-b8a5-216e6e42aead)

**receive_message:**

- Llama a simulate_network_latency para añadir un retraso antes de procesar el mensaje.
- Si el nodo no está participando (participating es False), simplemente retorna.
- Dependiendo del tipo de mensaje, llama al método correspondiente (handle_request_vote, handle_vote, handle_append_entries).

![imagen](https://github.com/user-attachments/assets/d56a1a4a-084c-4776-b2c3-f78e321876ec)

**handle_request_vote:**

- Si el nodo no ha votado por nadie (voted_for es None) o ha votado por el nodo solicitante, concede el voto.
- Envía un mensaje de voto concedido al nodo solicitante.

![imagen](https://github.com/user-attachments/assets/b951c70a-15a3-4442-913f-113f4ad6f08c)

**handle_vote:**

- Incrementa el contador de votos recibidos.
- Si el nodo recibe más de la mitad de los votos, se convierte en líder.
- Envía mensajes de latido (heartbeats) para mantener la consistencia como líder.

![imagen](https://github.com/user-attachments/assets/ee21d4ac-dc57-498c-8295-aa9070f88b60)

**handle_append_entries:**

- Añade la entrada recibida al log del nodo.
- Incrementa el índice de confirmación (commit_index).
- Envía un mensaje de reconocimiento al nodo remitente.

![imagen](https://github.com/user-attachments/assets/a27b5db2-55cb-4348-8d3c-a5637a2882aa)

**send_heartbeat:**

- Envía un mensaje de latido (append_entries) a todos los otros nodos.

![imagen](https://github.com/user-attachments/assets/00b86abe-6548-487a-a301-7afdc428580d)

**run:**

- Mantiene un bucle de ejecución continuo mientras el nodo esté participando.
- Si el nodo es líder, envía mensajes de latido periódicos.
- Si el nodo es seguidor, puede convertirse en candidato y participar en elecciones, solicitando votos.

![imagen](https://github.com/user-attachments/assets/2919cd26-6735-471a-84e6-e5162f1630d3)

**stop:**

- Establece el estado de participación (participating) a False.

![imagen](https://github.com/user-attachments/assets/a99a621c-b7ec-4c68-86e0-f1720c56fc45)

# Class Network

**__init__:**

- Establece el número total de nodos en la red (total_nodes).
- Inicializa una lista vacía para almacenar las instancias de los nodos (nodes).
- Inicializa una cola de mensajes (messages) para gestionar la comunicación entre nodos.
- Inicializa una lista de hilos (threads) para la ejecución concurrente de los nodos.
- Crea instancias de la clase Node para cada nodo en la red, las agrega a la lista de nodos y crea hilos para ejecutar cada nodo.

![imagen](https://github.com/user-attachments/assets/09e11c41-60ae-4640-ae03-51e62b7b2456)

**send_message:**

- Imprime un mensaje de depuración indicando que la red está enviando un mensaje desde un nodo a otro.
- Coloca el mensaje en la cola de mensajes (messages).
- Llama al método receive_message del nodo receptor para procesar el mensaje.

![imagen](https://github.com/user-attachments/assets/61f0c8ef-a3b4-485d-b00b-2456baca24c6)

**start:**

- Recorre la lista de hilos (threads) y llama al método start en cada hilo para comenzar la ejecución concurrente de los nodos.

![imagen](https://github.com/user-attachments/assets/b3368914-a6f7-46e3-bc77-ae16b9d16f89)

**stop:**

- Recorre la lista de nodos (nodes) y llama al método stop en cada nodo para detener su ejecución.
- Recorre la lista de hilos (threads) y llama al método join en cada hilo para esperar a que todos los hilos terminen su ejecución.

![imagen](https://github.com/user-attachments/assets/38c701ce-fe87-4798-9177-f9a129796e11)

# PARTE2

**1. Consistencia (C):**

La consistencia se gestiona mediante el algoritmo de consenso Raft. Este algoritmo asegura que todos los nodos en la red acuerden el mismo estado de los datos.

- Elección de Líder: Los nodos participan en elecciones para elegir un líder. El líder es responsable de replicar entradas de log a otros nodos y asegurar la consistencia.

![imagen](https://github.com/user-attachments/assets/13dc3f4b-0872-4dba-91e5-873b99377708)

- Replicación de Entradas de Log: El líder envía mensajes de latido (heartbeats) periódicamente para mantener la consistencia y replicar entradas de log a otros nodos.

![imagen](https://github.com/user-attachments/assets/584ecd59-cdb4-4534-a115-113c7b82869e)

**2. Disponibilidad (A):**

La disponibilidad se asegura manteniendo los nodos en ejecución y respondiendo a las solicitudes incluso si algunos nodos fallan.

- Nodo en Ejecución: Cada nodo tiene un bucle de ejecución en el método run que lo mantiene activo y participando en el consenso y otras operaciones.

![imagen](https://github.com/user-attachments/assets/79c71595-b609-40dc-9f1b-07a39e6c2c3a)

- Manejo de Fallos Aleatorios: Los nodos pueden experimentar fallos aleatorios y recuperarse. Esto se simula en el código ajustando la probabilidad de que un nodo se convierta en candidato.

![imagen](https://github.com/user-attachments/assets/506d0b4e-a6b2-44e8-9991-c59d61aa3479)

**3. Tolerancia a Particiones (P):**

La tolerancia a particiones se simula permitiendo que los nodos continúen operando y participando en elecciones incluso si algunos nodos no están disponibles debido a fallos de red.

- Simulación de Latencia de Red: La latencia de red se simula añadiendo retrasos aleatorios en la comunicación entre nodos.

![imagen](https://github.com/user-attachments/assets/e08808bb-781e-419a-a5ca-a427ca7866e4)

- Manejo de Fallos en Nodos: Los nodos pueden dejar de participar en la red debido a fallos simulados. Esto se maneja mediante el método stop.

![imagen](https://github.com/user-attachments/assets/492c3288-8861-4ceb-96b1-173745240572)

# PARTE3

**Salida:**

- Inicio:

  - La red se inicializa y cada nodo comienza a ejecutarse en un hilo separado.
  - Los nodos envían y reciben mensajes, sincronizan relojes y participan en el algoritmo de consenso Raft.

- Ciclo de Vida de los Nodos:

  - Los nodos solicitan acceso a recursos compartidos utilizando Raft.
  - Una vez obtenidos los recursos, los nodos realizan una tarea científica simulada.
  - Después de completar la tarea, los nodos liberan los recursos.
  - Los nodos realizan recolección de basura periódicamente para gestionar la memoria.
  - Los nodos continúan sincronizando sus relojes para mantener una vista consistente del tiempo en el sistema distribuido.

- Terminación:

  - Después de 30 segundos, la red de nodos se detiene.
  - Los nodos envían mensajes de terminación para notificar a otros nodos y cerrar la ejecución ordenadamente.
 
![imagen](https://github.com/user-attachments/assets/185b47c4-fbb5-4fab-9c92-1cb2da2ab58d)
