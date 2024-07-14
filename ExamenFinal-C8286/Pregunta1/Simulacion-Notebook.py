import asyncio
import logging
from datetime import datetime
import threading

# Configuracion de Logs
# Configuramos el sistema de registro para manejar errores y eventos informativos
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clase para representar un evento en el sistema
class Event:
    def __init__(self, event_type, priority, content):
        self.event_type = event_type  # Tipo de evento (CELL_EXECUTION, USER_INTERACTION)
        self.priority = priority  # Prioridad del evento (menor valor = mayor prioridad)
        self.content = content  # Contenido del evento (codigo de celda, interaccion del usuario)
        self.timestamp = datetime.now()  # Marca de tiempo del evento

    def __repr__(self):
        # Proporcionamos una representacion legible del evento para fines de depuracion
        return f"Evento(type={self.event_type}, priority={self.priority}, content={self.content}, timestamp={self.timestamp})"

# Clase para simular el manejo de un notebook
class NotebookSimulator:
    def __init__(self):
        self.events = asyncio.PriorityQueue()  # Cola de eventos con prioridad
        self.running = True  # Estado de ejecucion del simulador
        self.lock = asyncio.Lock()  # Bloqueo para manejar concurrencia

    async def add_event(self, event):
        # Añadimos un evento a la cola de eventos de manera segura usando un bloqueo
        async with self.lock:
            await self.events.put((event.priority, event))
            logging.info(f"Evento agregado: {event}")

    async def handle_event(self, event):
        # Manejamos los diferentes tipos de eventos
        if event.event_type == 'CELL_EXECUTION':
            await self.execute_cell(event.content)
        elif event.event_type == 'USER_INTERACTION':
            await self.handle_user_interaction(event.content)
        elif event.event_type == 'ERROR':
            self.log_error(event.content)
        elif event.event_type == 'LOG':
            self.log_info(event.content)

    async def execute_cell(self, cell_code):
        # Ejecutamos el codigo de una celda y manejamos los posibles errores
        try:
            exec(cell_code)
            logging.info(f"Celda ejecutada: {cell_code}")
        except Exception as e:
            await self.add_event(Event('ERROR', 1, str(e)))

    async def handle_user_interaction(self, interaction):
        # Manejamos las interacciones del usuario
        logging.info(f"Interaccion del usuario manejada: {interaction}")

    def log_error(self, error_message):
        # Registramos un mensaje de error
        logging.error(f"Error: {error_message}")

    def log_info(self, message):
        # Registramos un mensaje informativo
        logging.info(f"Log: {message}")

    async def event_loop(self):
        # Bucle principal para manejar los eventos en la cola
        while self.running:
            if not self.events.empty():
                _, event = await self.events.get()
                await self.handle_event(event)
            await asyncio.sleep(0.1)

    def stop(self):
        # Se detiene el simulador
        self.running = False

# Funcion principal que ejecuta el simulador, añade eventos y detiene el simulador despues de un tiempo
async def main():
    simulator = NotebookSimulator()

    # Añadimos eventos de ejemplo
    await simulator.add_event(Event('CELL_EXECUTION', 2, "print('Hola, mundo!')"))
    await simulator.add_event(Event('USER_INTERACTION', 1, "Clicked button"))
    await simulator.add_event(Event('CELL_EXECUTION', 3, "1 / 0"))  # Esto generara un error

    # Iniciamos el bucle de eventos en un hilo separado
    event_loop_thread = threading.Thread(target=lambda: asyncio.run(simulator.event_loop()))
    event_loop_thread.start()

    # Detenemos el simulador despues de 5 segundos
    await asyncio.sleep(5)
    simulator.stop()
    event_loop_thread.join()

# Ejecutamos la simulacion
asyncio.run(main())
