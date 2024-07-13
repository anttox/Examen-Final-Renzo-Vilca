# PARTE1

1. La clase ChandyLamport inicializa los robots, su estado, los canales y los marcadores recibidos.

![imagen](https://github.com/user-attachments/assets/07f7088f-2a84-416d-9396-bea69d58a3d6)

2. El método send_marker envía un marcador a todos los vecinos de un robot.

![imagen](https://github.com/user-attachments/assets/64340ca0-766e-4c3d-8d07-7c2e03920184)

3. El método receive_marker captura el estado del robot si es la primera vez que recibe un marcador y luego envía marcadores a sus vecinos.

![imagen](https://github.com/user-attachments/assets/b608c366-9f77-48b0-b061-b4d303f58d9a)

4. El método capture_state captura y devuelve el estado del robot.

![imagen](https://github.com/user-attachments/assets/caf8e176-f24f-48d7-9833-be77a363b4b4)

5. El método initiate_snapshot inicia el proceso de toma de instantánea desde un robot iniciador.

![imagen](https://github.com/user-attachments/assets/978e54ad-e557-4425-bae5-1a41cef9c0ec)

**Salida:**

La salida muestra los estados capturados de cada robot después de recibir los marcadores. La toma de instantáneas garantiza que los estados se capturen de manera coherente en un sistema distribuido.

![imagen](https://github.com/user-attachments/assets/e3d8bd18-3819-4de0-bb2f-f35ead932b50)

# PARTE2

1. La clase Raymond inicializa los nodos, el poseedor inicial del token y la cola de solicitudes.

![imagen](https://github.com/user-attachments/assets/711298e0-2071-4500-8139-1a712774b9c7)

2. El método request agrega un nodo a la cola de solicitudes del poseedor actual del token si el nodo no tiene el token.

![imagen](https://github.com/user-attachments/assets/587fa14b-3c2f-48c6-993e-c3df0be329d3)

3. El método pass_token pasa el token al siguiente nodo en la cola de solicitudes y actualiza el poseedor del token.

![imagen](https://github.com/user-attachments/assets/67633581-dd8f-431a-84d9-b6ac784df02b)

**Salida:**

El algoritmo de Raymond se usa para gestionar la exclusión mutua en un sistema distribuido. En este caso, Node2 solicita el token y Node1 lo pasa a Node2. La salida muestra que Node2 ahora tiene el token (True), lo que le permite acceder a los recursos compartidos. Este mecanismo garantiza que solo un nodo tenga acceso a los recursos compartidos a la vez.

![imagen](https://github.com/user-attachments/assets/0fe6c8d1-1509-4898-9217-54d5e28cd9ac)

# PARTE3

1. La clase VectorClock inicializa los nodos y sus relojes.

![imagen](https://github.com/user-attachments/assets/fbc57a3f-7f98-4490-a5e6-d3ca45cc9e48)

2. El método event incrementa el contador de eventos en el reloj del nodo correspondiente.

![imagen](https://github.com/user-attachments/assets/8b0436c6-567c-4e7c-83e7-ba6b8c17de9f)

3. El método send_message actualiza el reloj del receptor con el máximo de los valores actuales del emisor y del receptor, e incrementa el contador del receptor.

![imagen](https://github.com/user-attachments/assets/fed7a5ba-32fe-442a-bbb5-cef728dfe208)

**Salida:**

Los relojes vectoriales se utilizan para capturar el orden parcial de eventos en sistemas distribuidos. En este caso, Node1 registra un evento y luego envía un mensaje a Node2. Los relojes se actualizan para reflejar estos eventos. La salida muestra los relojes vectoriales actualizados para cada nodo, ayudando a detectar violaciones de causalidad.

![imagen](https://github.com/user-attachments/assets/8dafe17f-a9a0-4452-aaa9-b33dde4a75dd)

# PARTE4

1. La clase CheneyCollector configura el tamaño de los espacios de memoria y los inicializa, junto con el conjunto raíz y el puntero libre.

![imagen](https://github.com/user-attachments/assets/19bfb222-86ee-40b6-8d9d-60768c2ee7b2)

2. El método allocate asigna memoria para un objeto en el from_space. Si no hay suficiente espacio, se inicia la recolección de basura.

![imagen](https://github.com/user-attachments/assets/f9513adf-459e-4d61-8cd4-1de0055f59c0)

3. El método collect copia los objetos accesibles desde el from_space al to_space. Actualiza las referencias en el conjunto raíz y en los objetos copiados, y finalmente intercambia los espacios.

![imagen](https://github.com/user-attachments/assets/bd211531-dfc7-4825-9b8e-ed18d0bc278b)

4. El método copy maneja la copia de objetos desde el from_space al to_space.

![imagen](https://github.com/user-attachments/assets/5cea2d0a-15fe-44e1-ad04-bda3a2b8edf0)

5. El método add_root agrega una dirección al conjunto raíz para asegurarse de que estos objetos sean accesibles durante la recolección.

![imagen](https://github.com/user-attachments/assets/b1900843-b3c6-4854-8ce0-cc43ca146ada)

**Salida:**

- Antes de la recolección: Muestra el contenido del from_space antes de iniciar la recolección de basura.
- Después de la recolección: Muestra el contenido del from_space después de copiar los objetos accesibles al to_space y de intercambiar los espacios.

![imagen](https://github.com/user-attachments/assets/6d7c5dc5-2bb1-4530-8cf1-397f05edbc0d)


