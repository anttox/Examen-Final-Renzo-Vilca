# PARTE1

## 1. Clase Message

La clase Message representa un mensaje que se envía entre nodos en el sistema distribuido. Contiene información sobre el remitente, el contenido del mensaje y la marca de tiempo en la que se envió el mensaje.

![imagen](https://github.com/user-attachments/assets/779531a5-6bc0-4eab-9330-ab318ec39604)

## 2. Clase Node

La clase Node representa un nodo en el sistema distribuido. Cada nodo puede enviar y recibir mensajes, manejar solicitudes de exclusión mutua, detectar la terminación de procesos distribuidos y realizar recolección de basura.

**__init__:**

- Asigna valores a los atributos del nodo.
- Configura el reloj lógico, la cola de solicitudes, el contador de respuestas necesarias, los bloques de Ricart-Agrawala y Dijkstra-Scholten, la memoria del nodo y el recolector de basura.
- Inicializa el estado de ejecución del nodo.

![imagen](https://github.com/user-attachments/assets/b4fe12df-a70c-4090-a235-7ed5de964103)

**send_message:**

- Crea una instancia de Message con el remitente (el nodo actual), el contenido del mensaje y la marca de tiempo actual.
- Imprime un mensaje de depuración para indicar que se está enviando un mensaje.
- Llama al método send_message de la red para enviar el mensaje al nodo receptor.

![imagen](https://github.com/user-attachments/assets/7a1cda5e-fa4a-4125-b42f-3c2f4580b0ac)

**receive_message:**
    
- Imprime un mensaje de depuración para indicar que se ha recibido un mensaje.
- Actualiza el reloj lógico del nodo basado en la marca de tiempo del mensaje.
- Procesa el contenido del mensaje:
  - Si el mensaje es una solicitud (REQUEST), lo agrega a la cola de solicitudes y envía una respuesta (REPLY).
  - Si el mensaje es una respuesta (REPLY), decrementa el contador de respuestas necesarias.
  - Si el mensaje es de terminación (TERMINATE), maneja la terminación del proceso (Dijkstra-Scholten).
  - Si el mensaje es de inicio (START), inicia la detección de terminación del proceso (Dijkstra-Scholten).
  
![imagen](https://github.com/user-attachments/assets/a6e0dea8-f6df-4d7f-b3c5-ea5e04575f2f)

**request_resource:**
    
- Adquiere el bloqueo de Ricart-Agrawala.
- Incrementa el reloj lógico del nodo.
- Establece el contador de respuestas necesarias al número de nodos menos uno.
- Imprime un mensaje de depuración indicando que se está solicitando el recurso.
- Envía solicitudes de acceso al recurso a todos los otros nodos.
- Espera hasta recibir todas las respuestas necesarias.
- Libera el bloqueo de Ricart-Agrawala.

![imagen](https://github.com/user-attachments/assets/75c0c7ce-3efb-4f79-978d-cbacb96b205e)

**release_resource:**

- Imprime un mensaje de depuración indicando que se está liberando el recurso.
- Responde a todas las solicitudes en la cola de solicitudes enviando respuestas (REPLY).

![imagen](https://github.com/user-attachments/assets/2dd160cd-d00b-4e64-b605-1ec87d504a6e)

**synchronize_clock:**

- Imprime un mensaje de depuración indicando que se está sincronizando el reloj.
- Envía un mensaje de sincronización (SYNC) a todos los otros nodos.

![imagen](https://github.com/user-attachments/assets/26d589f0-09b9-42f5-9a06-f2a43b32e44e)

**dijkstra_scholten_start:**

- Imprime un mensaje de depuración indicando que se está iniciando la detección de terminación.
- Establece el estado de Dijkstra-Scholten a activo.
- Envía un mensaje de inicio (START) a todos los otros nodos.

![imagen](https://github.com/user-attachments/assets/1e3ccc79-1aa0-41eb-8bec-419f07551a0a)

**dijkstra_scholten_terminate:**
    
- Imprime un mensaje de depuración indicando que se está manejando la terminación desde otro nodo.
- Si el nodo padre es None, establece el nodo remitente como padre.
- Si ya tiene un nodo padre, agrega el nodo remitente a la lista de hijos.
- Si la lista de hijos está vacía, envía un mensaje de terminación (TERMINATE) al nodo padre y establece el estado de Dijkstra-Scholten a inactivo.

![imagen](https://github.com/user-attachments/assets/9421cfbf-0a5e-453c-a58d-569403f81b74)

**garbage_collect:**

- Imprime un mensaje de depuración indicando que se está realizando la recolección de basura.
- Llama al método collect del recolector de basura (CheneyCollector) para realizar la recolección.

![imagen](https://github.com/user-attachments/assets/9c953f17-ae4f-4499-8183-aef80323b346)

**run:**

- Mientras el nodo esté en ejecución (running):
  - Duerme por 1 segundo.
  - Realiza la recolección de basura.
  - Sincroniza el reloj lógico con otros nodos.
  - Solicita acceso a un recurso compartido.
  - Imprime un mensaje de depuración indicando que se está realizando una tarea científica.
  - Duerme por 2 segundos simulando la ejecución de la tarea científica.
  - Libera el recurso compartido.

![imagen](https://github.com/user-attachments/assets/cfa940d6-471a-4e31-890f-4e4ccdaecc04)

**stop:**

- Establece el estado de ejecución del nodo a False.
- Envía un mensaje de terminación (TERMINATE) a sí mismo para notificar a otros nodos.

![imagen](https://github.com/user-attachments/assets/04e15baa-b0c0-48ee-8e5d-e2a7c7656eda)

## Class CheneyCollector

**__init__:**

- Establece el tamaño de los espacios de memoria (from_space y to_space).
- Inicializa ambos espacios (from_space y to_space) con None para indicar que están vacíos.
- Inicializa el conjunto raíz (root_set) como una lista vacía.
- Establece el puntero libre (free_ptr) en 0 para indicar la próxima posición libre en el from_space.

![imagen](https://github.com/user-attachments/assets/f8aa3a64-11dd-4813-8e29-3d8a24527157)

**allocate:**

- Verifica si hay suficiente espacio en from_space para asignar el objeto.
- Si no hay suficiente espacio, llama al método collect para realizar la recolección de basura y liberar espacio.
- Si después de la recolección de basura aún no hay suficiente espacio, lanza un error de memoria.
- Si hay suficiente espacio, asigna el objeto en la posición indicada por free_ptr en from_space.
- Incrementa free_ptr para apuntar a la siguiente posición libre.
- Devuelve la dirección donde se asignó el objeto.

![imagen](https://github.com/user-attachments/assets/3ffb0af9-b3cf-42d0-a687-6c257ccd5c74)

**collect:**

- Imprime un mensaje indicando que se ha iniciado la recolección de basura.
- Inicializa to_space con None y establece to_space_ptr en 0 para empezar a copiar objetos en el to_space.
- Copia todos los objetos accesibles del root_set al to_space, actualizando sus direcciones en el root_set.
- Procesa cada objeto en el to_space, copiando los objetos referenciados por estos objetos.}
- Intercambia from_space y to_space, de modo que to_space se convierte en el nuevo espacio activo.
- Actualiza free_ptr al valor de to_space_ptr para indicar la próxima posición libre.
- Imprime un mensaje indicando que se ha completado la recolección de basura.

![imagen](https://github.com/user-attachments/assets/c53f1b59-18cb-41ac-b08e-910e835b94d7)

**copy:**

- Obtiene el objeto en la dirección addr en el from_space.
- Verifica si el objeto no es None y si aún no ha sido copiado al to_space.
- Copia el objeto al to_space en la posición indicada por to_space_ptr.
- Establece la dirección en from_space a None para indicar que el objeto ha sido copiado.
- Incrementa to_space_ptr para apuntar a la siguiente posición libre en to_space.
- Devuelve to_space_ptr actualizado.

![imagen](https://github.com/user-attachments/assets/9d73e44e-5af1-4def-9c44-17c4928cae93)

**add_root:**

- Agrega un diccionario con la dirección (addr) al root_set.

![imagen](https://github.com/user-attachments/assets/c1fa9f53-0b55-4ab5-8d7e-3ce55636729b)

## Class Network

**__init__:**

- Establece el número total de nodos en la red (total_nodes).
- Inicializa una lista vacía para almacenar las instancias de los nodos (nodes).
- Inicializa una cola de mensajes (messages) para gestionar la comunicación entre nodos.
- Inicializa una lista de hilos (threads) para la ejecución concurrente de los nodos.
- Crea instancias de la clase Node para cada nodo en la red, las agrega a la lista de nodos y crea hilos para ejecutar cada nodo.

![imagen](https://github.com/user-attachments/assets/c69ca593-4e76-4ace-bee5-9ec84b062f27)

**send_message:**

- Imprime un mensaje de depuración indicando que la red está enviando un mensaje desde un nodo a otro.
- Coloca el mensaje en la cola de mensajes (messages).
- Llama al método receive_message del nodo receptor para procesar el mensaje.

![imagen](https://github.com/user-attachments/assets/89c50047-fbf9-4627-a652-1db16af1927c)

**start:**

- Recorre la lista de hilos (threads) y llama al método start en cada hilo para comenzar la ejecución concurrente de los nodos.

![imagen](https://github.com/user-attachments/assets/3661b15e-0f32-43a3-8ad1-a6cce085310e)

**stop:**

- Recorre la lista de nodos (nodes) y llama al método stop en cada nodo para detener su ejecución.
- Recorre la lista de hilos (threads) y llama al método join en cada hilo para esperar a que todos los hilos terminen su ejecución.

![imagen](https://github.com/user-attachments/assets/c1d5a46a-7d33-4f6e-97b3-1963489e318e)

# PARTE2

**Salida:**

- Inicio:
  - La red se inicializa y cada nodo comienza a ejecutarse en un hilo separado.
  - Los nodos sincronizan sus relojes lógicos.

- Ciclo de Vida de los Nodos:
  - Los nodos solicitan acceso a recursos compartidos utilizando Ricart-Agrawala.
  - Una vez obtenidos los recursos, los nodos realizan una tarea científica simulada.
  - Después de completar la tarea, los nodos liberan los recursos.
  - Los nodos realizan recolección de basura periódicamente para gestionar la memoria.
  - Los nodos continúan sincronizando sus relojes para mantener una vista consistente del tiempo en el sistema distribuido.

- Terminación:
  - Después de 10 segundos, la red de nodos se detiene.
  - Los nodos envían mensajes de terminación para notificar a otros nodos y cerrar la ejecución ordenadamente.

![imagen](https://github.com/user-attachments/assets/47a09e59-6da0-4586-89a1-028081112d83)

