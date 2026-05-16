class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None  # puntero al próximo nodo

# ── TDA COLA (FIFO) — solicitudes en espera ──────────────────
class Cola:
    def __init__(self):
        self.frente = None   # primer nodo en salir
        self.fin = None      # último nodo encolado
        self.tamanio = 0

    def esta_vacia(self): return self.frente is None

    def encolar(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.frente = self.fin = nuevo
        else:
            self.fin.siguiente = nuevo   # enlaza al final
            self.fin = nuevo             # fin avanza al nuevo
        self.tamanio += 1

    def encolar_al_frente(self, dato):   # reingresa solicitud urgente
        nuevo = Nodo(dato)
        nuevo.siguiente = self.frente    # nuevo apunta al antiguo frente
        self.frente = nuevo
        if self.fin is None: self.fin = nuevo
        self.tamanio += 1

    def desencolar(self):
        if self.esta_vacia(): return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente  # frente avanza al siguiente
        if self.frente is None: self.fin = None
        self.tamanio -= 1
        return dato

    def mostrar(self):
        if self.esta_vacia(): print("  (Cola vacía)"); return
        actual = self.frente; pos = 1
        while actual:
            s = actual.dato
            print(f"  [{pos}] #{s.id_solicitud} {s.zona_origen}->{s.zona_destino} | {s.tipo}")
            actual = actual.siguiente; pos += 1

# ── TDA PILA (LIFO) — auditoría de acciones ──────────────────
class Pila:
    def __init__(self, capacidad=10):
        self.tope = None       # nodo en la cima de la pila
        self.tamanio = 0
        self.capacidad = capacidad  # limitamos para no crecer infinito

    def esta_vacia(self): return self.tope is None

    def apilar(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self.tope   # nuevo apunta al antiguo tope
        self.tope = nuevo             # tope sube al nuevo nodo
        self.tamanio += 1
        # Si supera la capacidad, descartamos el elemento más antiguo
        if self.tamanio > self.capacidad:
            self._recortar()

    def _recortar(self):
        # Recorre hasta el penúltimo y elimina el último (el más viejo)
        actual = self.tope
        while actual.siguiente and actual.siguiente.siguiente:
            actual = actual.siguiente
        actual.siguiente = None
        self.tamanio -= 1

    def desapilar(self):
        if self.esta_vacia(): return None
        dato = self.tope.dato
        self.tope = self.tope.siguiente   # tope baja al nodo anterior
        self.tamanio -= 1
        return dato

    def mostrar(self):
        if self.esta_vacia(): print("  (Pila vacía)"); return
        actual = self.tope; i = 1
        while actual:
            print(f"  [{i}] {actual.dato}")
            actual = actual.siguiente; i += 1

# ── TDA LISTA ENLAZADA — historial de servicios ──────────────
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None   # primer nodo
        self.tamanio = 0

    def esta_vacia(self): return self.cabeza is None

    def agregar_al_final(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:        # avanza hasta el último nodo
                actual = actual.siguiente
            actual.siguiente = nuevo       # enlaza el nuevo al final
        self.tamanio += 1

# ── TDA ÁRBOL BST — conductores ordenados por cédula ─────────
class NodoBST:
    def __init__(self, conductor):
        self.dato = conductor
        self.izquierda = None   # subárbol con cédulas menores
        self.derecha = None     # subárbol con cédulas mayores

class ArbolBST:
    def __init__(self):
        self.raiz = None   # raíz del árbol

    def insertar(self, conductor):
        self.raiz = self._insertar(self.raiz, conductor)

    def _insertar(self, nodo, conductor):
        if nodo is None:
            return NodoBST(conductor)          # posición encontrada
        if conductor.cedula < nodo.dato.cedula:
            nodo.izquierda = self._insertar(nodo.izquierda, conductor)  # va a la izquierda
        elif conductor.cedula > nodo.dato.cedula:
            nodo.derecha = self._insertar(nodo.derecha, conductor)      # va a la derecha
        return nodo

    def buscar(self, cedula):
        return self._buscar(self.raiz, cedula)

    def _buscar(self, nodo, cedula):
        if nodo is None: return None           # no encontrado
        if cedula == nodo.dato.cedula: return nodo.dato
        if cedula < nodo.dato.cedula:
            return self._buscar(nodo.izquierda, cedula)   # busca izquierda
        return self._buscar(nodo.derecha, cedula)          # busca derecha

    def inorden(self):
        # Recorre izquierda → raíz → derecha: devuelve conductores en orden de cédula
        resultados = []
        self._inorden(self.raiz, resultados)
        return resultados

    def _inorden(self, nodo, resultados):
        if nodo is None: return
        self._inorden(nodo.izquierda, resultados)   # subárbol izquierdo primero
        resultados.append(nodo.dato)                # luego la raíz
        self._inorden(nodo.derecha, resultados)     # luego el derecho

    def conductor_disponible_para(self, tipo):
        # Recorre in-orden hasta encontrar uno disponible y habilitado para el tipo
        conductores = self.inorden()
        for c in conductores:
            if c.disponible and tipo in c.servicios:
                return c
        return None

# ── TDA GRAFO — mapa de zonas y vías ─────────────────────────
class NodoVia:   # arista de la lista de adyacencia
    def __init__(self, zona_destino, distancia):
        self.zona_destino = zona_destino
        self.distancia = distancia
        self.activa = True     # False = vía cerrada
        self.siguiente = None

class NodoZona:  # vértice del grafo
    def __init__(self, nombre):
        self.nombre = nombre
        self.lista_vias = None   # inicio de la lista de adyacencia
        self.siguiente = None

class Grafo:
    def __init__(self):
        self.primer_zona = None

    def _buscar_zona(self, nombre):
        actual = self.primer_zona
        while actual:
            if actual.nombre == nombre: return actual
            actual = actual.siguiente
        return None

    def agregar_zona(self, nombre):
        nuevo = NodoZona(nombre)
        nuevo.siguiente = self.primer_zona
        self.primer_zona = nuevo

    def agregar_via(self, zona_a, zona_b, distancia):
        nodo_a = self._buscar_zona(zona_a)
        nodo_b = self._buscar_zona(zona_b)
        via_ab = NodoVia(zona_b, distancia); via_ab.siguiente = nodo_a.lista_vias; nodo_a.lista_vias = via_ab
        via_ba = NodoVia(zona_a, distancia); via_ba.siguiente = nodo_b.lista_vias; nodo_b.lista_vias = via_ba

    def cambiar_via(self, zona_a, zona_b, abrir):
        for nombre_zona, nombre_destino in [(zona_a, zona_b), (zona_b, zona_a)]:
            via = self._buscar_zona(nombre_zona).lista_vias
            while via:
                if via.zona_destino == nombre_destino: via.activa = abrir; break
                via = via.siguiente
        print(f"  Vía {zona_a}<->{zona_b}: {'ABIERTA ✓' if abrir else 'CERRADA ✗'}")

    def lista_zonas(self):
        nombres = []; actual = self.primer_zona
        while actual: nombres.append(actual.nombre); actual = actual.siguiente
        return nombres

    def dijkstra(self, origen):
        INF = float('inf')
        zonas = self.lista_zonas()
        distancias   = [[z, INF]  for z in zonas]
        predecesores = [[z, None] for z in zonas]
        visitadas = []

        def get_dist(z):
            for p in distancias:
                if p[0] == z: return p[1]
            return INF
        def set_dist(z, v):
            for p in distancias:
                if p[0] == z: p[1] = v; return
        def set_pred(z, ant):
            for p in predecesores:
                if p[0] == z: p[1] = ant; return

        set_dist(origen, 0)
        for _ in range(len(zonas)):
            zona_actual = None; dist_min = INF
            for p in distancias:
                if p[0] not in visitadas and p[1] < dist_min:
                    dist_min = p[1]; zona_actual = p[0]
            if not zona_actual: break
            visitadas.append(zona_actual)
            via = self._buscar_zona(zona_actual).lista_vias
            while via:
                if via.activa and via.zona_destino not in visitadas:
                    nueva_dist = get_dist(zona_actual) + via.distancia
                    if nueva_dist < get_dist(via.zona_destino):
                        set_dist(via.zona_destino, nueva_dist)
                        set_pred(via.zona_destino, zona_actual)
                via = via.siguiente
        return distancias, predecesores

    def ruta_mas_corta(self, origen, destino):
        if origen == destino: return 0, origen
        distancias, predecesores = self.dijkstra(origen)
        distancia_final = next((p[1] for p in distancias if p[0] == destino), float('inf'))
        if distancia_final == float('inf'): return None, None
        camino = []; zona_actual = destino
        while zona_actual:
            camino.append(zona_actual)
            zona_actual = next((p[1] for p in predecesores if p[0] == zona_actual), None)
        camino.reverse()
        return distancia_final, " -> ".join(camino)

    def mostrar(self):
        zona = self.primer_zona
        while zona:
            print(f"\n  Zona: {zona.nombre}")
            via = zona.lista_vias
            while via:
                estado = "✓" if via.activa else "✗ CERRADA"
                print(f"    -> {via.zona_destino:12s} {via.distancia:>6} m [{estado}]")
                via = via.siguiente
            zona = zona.siguiente

# ── CLASES DE DATOS ──────────────────────────────────────────
class Solicitud:
    _contador = 1
    def __init__(self, zona_origen, zona_destino, tipo):
        self.id_solicitud = Solicitud._contador; Solicitud._contador += 1
        self.zona_origen = zona_origen
        self.zona_destino = zona_destino
        self.tipo = tipo
    def __str__(self):
        return f"#{self.id_solicitud} {self.zona_origen}->{self.zona_destino} [{self.tipo}]"

class Conductor:
    def __init__(self, cedula, nombre, zona, servicios):
        self.cedula = cedula
        self.nombre = nombre
        self.zona = zona
        self.servicios = servicios   # "Estándar,Baúl,Mascotas"
        self.disponible = True
    def __str__(self):
        estado = "Disponible" if self.disponible else "En servicio"
        return f"C.C.{self.cedula} | {self.nombre:15s} | {self.zona:12s} | {self.servicios:25s} | {estado}"

# ── TARIFAS Y TIEMPOS ────────────────────────────────────────
def calcular_tarifa(distancia_metros):
    # Base $5.000 + recargo según rango
    distancia_km = distancia_metros / 1000
    if distancia_km <= 1:    recargo = 2000
    elif distancia_km <= 3:  recargo = 4000
    elif distancia_km <= 6:  recargo = 7000
    elif distancia_km <= 10: recargo = 10000
    else:                    recargo = 12000
    return 5000 + recargo

def calcular_tiempo(distancia_al_origen, misma_zona):
    return 5 if misma_zona else 5 + distancia_al_origen // 500

# ── HELPERS DE MENÚ — siempre se elige por número ────────────
def elegir_opcion(titulo, opciones):
    print(f"\n  {titulo}")
    for i, opcion in enumerate(opciones): print(f"  {i+1}. {opcion}")
    while True:
        entrada = input(f"  Opción (1-{len(opciones)}): ").strip()
        if entrada.isdigit() and 1 <= int(entrada) <= len(opciones):
            return int(entrada) - 1
        print("  [!] Número inválido, intente de nuevo.")

def elegir_zona(grafo, titulo):
    zonas = grafo.lista_zonas()
    indice = elegir_opcion(titulo, zonas)
    print(f"  → {zonas[indice]}")
    return zonas[indice]

# ── SISTEMA PRINCIPAL ────────────────────────────────────────
class SistemaTaxi:
    def __init__(self):
        self.cola_solicitudes = Cola()
        self.arbol_conductores = ArbolBST()
        self.historial = ListaEnlazada()
        self.pila_auditoria = Pila(capacidad=10)
        self.grafo = Grafo()
        self._cargar_datos()

    def _cargar_datos(self):
        for zona in ["Norte","Centro","Sur","Oriente","Occidente","Aeropuerto"]:
            self.grafo.agregar_zona(zona)
        for za, zb, dist in [
            ("Norte","Centro",1200),   ("Centro","Sur",800),
            ("Centro","Oriente",2500), ("Norte","Occidente",3000),
            ("Sur","Aeropuerto",4500), ("Oriente","Aeropuerto",6200),
            ("Occidente","Centro",1800)]:
            self.grafo.agregar_via(za, zb, dist)
        for cedula, nombre, zona, servicios in [
            (10001,"Carlos Pérez","Norte","Estándar,Baúl"),
            (10002,"María López","Centro","Estándar,Mascotas"),
            (10003,"Juan García","Sur","Estándar"),
            (10004,"Ana Martínez","Aeropuerto","Estándar,Baúl,Mascotas"),
            (10005,"Luis Torres","Occidente","Estándar,Baúl")]:
            self.arbol_conductores.insertar(Conductor(cedula, nombre, zona, servicios))
        print("  ✓ Sistema listo.\n")

    def registrar_solicitud(self):
        print("\n== REGISTRAR SOLICITUD ==")
        zona_origen  = elegir_zona(self.grafo, "Zona de ORIGEN:")
        zona_destino = elegir_zona(self.grafo, "Zona de DESTINO:")
        idx = elegir_opcion("Tipo de servicio:", [
            "Estándar (vehículo regular)",
            "Baúl     (maletero grande)",
            "Mascotas (apto para animales)"])
        tipo = ["Estándar","Baúl","Mascotas"][idx]
        solicitud = Solicitud(zona_origen, zona_destino, tipo)
        self.cola_solicitudes.encolar(solicitud)
        self.pila_auditoria.apilar(f"REGISTRÓ solicitud {solicitud}")
        print(f"  ✓ {solicitud} en cola. Posición: {self.cola_solicitudes.tamanio}")

    def atender_solicitud(self):
        print("\n== ATENDER SOLICITUD ==")
        if self.cola_solicitudes.esta_vacia():
            print("  [!] No hay solicitudes en espera."); return
        solicitud = self.cola_solicitudes.desencolar()
        print(f"  Procesando: {solicitud}")
        # Buscar en el BST (in-orden) un conductor disponible para el tipo
        conductor = self.arbol_conductores.conductor_disponible_para(solicitud.tipo)
        if not conductor:
            print("  [!] Sin conductor disponible. Solicitud reingresada.")
            self.cola_solicitudes.encolar_al_frente(solicitud)
            self.pila_auditoria.apilar(f"SIN CONDUCTOR para {solicitud}")
            return
            
        # Calcular distancia del conductor al origen del cliente
        distancia_al_origen = 0
        if conductor.zona != solicitud.zona_origen:
            distancia_al_origen, _ = self.grafo.ruta_mas_corta(conductor.zona, solicitud.zona_origen)
            if distancia_al_origen is None:
                print("  [!] Conductor sin ruta al origen."); return

        # Calcular ruta del viaje (origen → destino del cliente)
        distancia_viaje, ruta_viaje = self.grafo.ruta_mas_corta(solicitud.zona_origen, solicitud.zona_destino)
        if distancia_viaje is None:
            print("  [!] No hay ruta habilitada para el destino."); return
        tarifa = calcular_tarifa(distancia_viaje)
        tiempo_llegada = calcular_tiempo(distancia_al_origen, conductor.zona == solicitud.zona_origen)
        conductor.disponible = False
        conductor.zona = solicitud.zona_destino
        registro = (solicitud, conductor.nombre, distancia_viaje, tarifa, ruta_viaje, tiempo_llegada)
        self.historial.agregar_al_final(registro)
        self.pila_auditoria.apilar(f"ATENDIÓ {solicitud} → conductor {conductor.nombre}")
        conductor.disponible = True
        print(f"  ✓ Conductor : {conductor.nombre} (C.C. {conductor.cedula})")
        print(f"  ✓ Ruta      : {ruta_viaje}")
        print(f"  ✓ Distancia : {distancia_viaje} m | Tarifa: ${tarifa:,.0f} | Llegada: ~{tiempo_llegada} min")

    def gestionar_via(self):
        print("\n== GESTIÓN DE VÍAS ==")
        zona_a = elegir_zona(self.grafo, "Zona A de la vía:")
        zona_b = elegir_zona(self.grafo, "Zona B de la vía:")
        idx = elegir_opcion("Acción:", ["Cerrar vía (bloqueo)", "Abrir vía (levantar bloqueo)"])
        abrir = (idx == 1)
        self.grafo.cambiar_via(zona_a, zona_b, abrir)
        accion = "ABRIÓ" if abrir else "CERRÓ"
        self.pila_auditoria.apilar(f"{accion} vía {zona_a}<->{zona_b}")

    def ver_historial(self):
        print("\n== HISTORIAL DE SERVICIOS ==")
        if self.historial.esta_vacia():
            print("  (Sin servicios aún)")
        else:
            nodo = self.historial.cabeza; i = 1
            while nodo:
                solicitud, conductor, distancia, tarifa, ruta, tiempo = nodo.dato
                print(f"\n  [{i}] {solicitud} | Conductor: {conductor}")
                print(f"      Ruta: {ruta} | {distancia} m | ${tarifa:,.0f} | ~{tiempo} min")
                nodo = nodo.siguiente; i += 1
        print("\n  -- Últimas acciones (Pila de Auditoría) --")
        self.pila_auditoria.mostrar()

    def ver_cola(self):
        print(f"\n== COLA DE ESPERA ({self.cola_solicitudes.tamanio} solicitudes) ==")
        self.cola_solicitudes.mostrar()

    def ver_conductores(self):
        print("\n== CONDUCTORES (in-orden por cédula) ==")
        conductores = self.arbol_conductores.inorden()
        if not conductores:
            print("  (Sin conductores)"); return
        for i, c in enumerate(conductores, 1):
            print(f"  {i}. {c}")
        print()
        idx = elegir_opcion("¿Qué desea hacer?", ["Buscar conductor por cédula", "Volver al menú"])
        if idx == 0:
            cedula_str = input("  Ingrese la cédula a buscar: ").strip()
            if cedula_str.isdigit():
                resultado = self.arbol_conductores.buscar(int(cedula_str))
                if resultado: print(f"\n  Encontrado: {resultado}")
                else: print("  [!] Cédula no encontrada en el árbol.")
            else:
                print("  [!] La cédula debe ser numérica.")

    def ver_mapa(self):
        print("\n== MAPA DE ZONAS Y VÍAS ==")
        self.grafo.mostrar()

# ── MENÚ PRINCIPAL ───────────────────────────────────────────
def main():
    sistema = SistemaTaxi()
    opciones = ["Registrar Solicitud","Atender Solicitud","Gestionar Vía",
                "Historial y Auditoría","Cola de Espera",
                "Conductores (BST)","Mapa","Salir"]
    acciones = [sistema.registrar_solicitud, sistema.atender_solicitud,
                sistema.gestionar_via, sistema.ver_historial,
                sistema.ver_cola, sistema.ver_conductores, sistema.ver_mapa]
    while True:
        print("\n" + "="*50)
        print("   COOPERATIVA DE TAXIS — SISTEMA MULTIZONA")
        print("="*50)
        for i, opcion in enumerate(opciones): print(f"  {i+1}. {opcion}")
        print("-"*50)
        entrada = input("  Opción (1-8): ").strip()
        if entrada == "8": print("\n  ¡Hasta luego!\n"); break
        if entrada.isdigit() and 1 <= int(entrada) <= 7:
            acciones[int(entrada)-1]()
        else:
            print("  [!] Opción inválida.")
        input("\n  [ENTER para continuar...]")

if __name__ == "__main__":
    main()
