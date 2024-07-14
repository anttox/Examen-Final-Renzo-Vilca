# PARTE1

## Configuración de Logs

Configurar el registro de logs para manejar errores y eventos informativos.

![imagen](https://github.com/user-attachments/assets/51a2a7df-3c69-43bc-a576-874969ceb5e5)

## Class Event

**__init__:**

- Establece el tipo de evento (event_type), que puede ser una ejecución de celda, una interacción de usuario, un error, etc.
- Establece la prioridad del evento (priority), que determina el orden en el que los eventos serán manejados (menor valor significa mayor prioridad).
- Establece el contenido del evento (content), que puede ser el código de la celda a ejecutar, la descripción de la interacción del usuario, el mensaje de error, etc.
- Establece la marca de tiempo (timestamp) en el momento en que se crea el evento, para registrar cuándo ocurrió.

![imagen](https://github.com/user-attachments/assets/49aab736-450b-4467-9510-d3714d763ee4)

**__repr__:**

- Devuelve una cadena de texto que representa el evento, incluyendo su tipo, prioridad, contenido y marca de tiempo.

![imagen](https://github.com/user-attachments/assets/21ded17c-6f06-432a-94a5-a80e8ab75ce5)

## Class 

**__init__:**

- Inicializa una cola de eventos con prioridad (PriorityQueue).
- Establece el estado de ejecución del simulador (running) como True.
- Crea un bloqueo (lock) para manejar la concurrencia de manera segura.

![imagen](https://github.com/user-attachments/assets/711f9222-2b3c-4e82-b28f-828c0d54d354)

**add_event:**

- Usa un bloqueo (lock) para asegurar que la operación de añadir el evento a la cola sea segura en términos de concurrencia.
- Añade el evento a la cola de eventos.
- Registra un mensaje informativo sobre el evento añadido.

![imagen](https://github.com/user-attachments/assets/f35aaefa-a5e8-4bc9-bdea-e023ff32a32c)

**handle_event:**

- Dependiendo del tipo de evento (event_type), llama al método correspondiente para manejar el evento:
  - CELL_EXECUTION -> execute_cell
  - USER_INTERACTION -> handle_user_interaction
  - ERROR -> log_error
  - LOG -> log_info

![imagen](https://github.com/user-attachments/assets/c5715167-d0e6-4f93-a7f9-0208f2a1d71a)

**execute_cell:**

- Intenta ejecutar el código de la celda usando exec.
- Si ocurre una excepción, añade un evento de error a la cola de eventos.

![imagen](https://github.com/user-attachments/assets/374c3bab-17bf-4e77-96a0-c395a0034733)

**handle_user_interaction:**

- Registra un mensaje informativo sobre la interacción del usuario.

![imagen](https://github.com/user-attachments/assets/74a0fffc-178f-4e45-a112-c5e674c91e05)

**log_error:**

- Usa el módulo logging para registrar un mensaje de error.

![imagen](https://github.com/user-attachments/assets/cb61a093-4617-4897-bad8-cdebe620132d)

**log_info:**

- Usa el módulo logging para registrar un mensaje informativo.

![imagen](https://github.com/user-attachments/assets/db7a6a4c-8f2f-4b4f-8fa0-715e46b333ba)

**event_loop:**

- Mientras el simulador esté en ejecución (running):
  - Si la cola de eventos no está vacía, obtiene el evento con mayor prioridad y lo maneja llamando a handle_event.
  - Espera 0.1 segundos antes de revisar la cola nuevamente.

![imagen](https://github.com/user-attachments/assets/f4980bf7-40f3-43c2-a4c7-8be8af9ff366)

**stop:**

- Establece el estado de ejecución del simulador (running) como False.

![imagen](https://github.com/user-attachments/assets/5fdcabba-2622-4c91-84a9-967238fdc36b)

**async def main():**

La función async def main() es la función principal que ejecuta el simulador de notebook, añade eventos y detiene el simulador después de un tiempo. Esta función organiza la secuencia de acciones necesarias para inicializar y ejecutar el simulador, incluyendo la adición de eventos de ejemplo y la gestión del bucle de eventos en un hilo separado.

![imagen](https://github.com/user-attachments/assets/f1f8a0e3-b7c8-4c9e-b26e-e76ad29b5533)

# PARTE2 

**Salida:**

La salida del código proporciona información detallada sobre cada paso del proceso de simulación, incluyendo la adición y manejo de eventos, la ejecución de celdas, las interacciones de usuario y cualquier error que ocurra durante la ejecución. Esto facilita la depuración y el seguimiento del estado del simulador en tiempo real.

![imagen](https://github.com/user-attachments/assets/cabff4d7-b44a-463e-add5-29d1c9b50f08)
