class CheneyCollector:
    def __init__(self, size):
        # Iniciamos el tamaño de los espacios de memoria y los dos espacios de memoria
        self.size = size
        self.from_space = [None] * size
        self.to_space = [None] * size
        # Iniciamos el conjunto raiz y el puntero libre
        self.root_set = []
        self.free_ptr = 0

    def allocate(self, obj):
        # Asignamos memoria para un objeto en el from_space
        if self.free_ptr >= self.size:
            # Si no hay espacio, realizamos la recolección de basura
            self.collect()
            if self.free_ptr >= self.size:
                # Si aun no hay espacio despues de la recoleccion, lanzar un error de memoria
                raise MemoryError("Out of memory")
        addr = self.free_ptr
        self.from_space[addr] = obj
        self.free_ptr += 1
        return addr

    def collect(self):
        # Iniciamos el proceso de recolección de basura
        self.to_space = [None] * self.size
        to_space_ptr = 0

        # Copiamos los objetos del conjunto raíz al to_space
        for i, root in enumerate(self.root_set):
            addr = root['addr']
            to_space_ptr = self.copy(addr, to_space_ptr)
            self.root_set[i]['addr'] = to_space_ptr - 1

        # Procesamos los objetos copiados
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

    def copy(self, addr, to_space_ptr):
        # Copiamos un objeto del from_space al to_space si aun no ha sido copiado
        obj = self.from_space[addr]
        if obj is not None and obj not in self.to_space:
            self.to_space[to_space_ptr] = obj
            self.from_space[addr] = None
            to_space_ptr += 1
        return to_space_ptr

    def add_root(self, addr):
        # Agregamos una dirección al conjunto raiz
        self.root_set.append({'addr': addr})

# Ejemplo de uso
collector = CheneyCollector(10)
root1 = collector.allocate({'name': 'obj1', 'ref': None})
root2 = collector.allocate({'name': 'obj2', 'ref': root1})
collector.add_root(root1)
collector.add_root(root2)
print("Antes de la recoleccion:")
print("from_space:", collector.from_space)
collector.collect()
print("Después de la recoleccion:")
print("from_space:", collector.from_space)
