# 🚖 Sistema de Gestión de Servicios — Cooperativa de Taxis Multizona

Solución interactiva por consola desarrollada en Python para la asignación y control operativo en tiempo real de una flota de taxis multizona. El proyecto destaca por la implementación manual y desde cero de Estructuras de Datos Avanzadas utilizando objetos autoreferenciados (nodos y punteros), evitando colecciones nativas de Python como almacenamiento principal de la lógica del negocio.

Este sistema fue desarrollado bajo los lineamientos académicos de la **Universidad Cooperativa de Colombia (2026)**.

---

## 🚀 Características Principales

* **Asignación en Orden de Llegada:** Cola de solicitudes gestionada bajo el principio FIFO.
* **Búsqueda e Indexación Optimizada:** Directorio de conductores indexado jerárquicamente por número de cédula en un Árbol Binario de Búsqueda (BST).
* **Simulación Vial Dinámica:** Modelado geográfico de la ciudad mediante un Grafo ponderado con soporte para apertura y cierre de calles en tiempo real.
* **Rutas Mínimas Automáticas:** Implementación del Algoritmo de Dijkstra para evadir bloqueos de tránsito y optimizar rutas.
* **Trazabilidad Inversa:** Registro elástico de logs del operador mediante una Pila con tope de control de memoria.

---

## 🛠️ Requisitos Previos

El sistema está diseñado utilizando únicamente módulos de la biblioteca estándar de Python, por lo que **no requiere la instalación de librerías de terceros (pip)**.

* **Intérprete:** Python 3.8 o superior.
* **Sistema Operativo:** Compatible con entornos Unix/Linux, macOS y Windows (incluye soporte adaptado para la limpieza automática de la terminal).

---

## ⚙️ Instrucciones de Instalación y Ejecución

1. **Clonar o descargar el repositorio** asegurándote de ubicar en la misma carpeta el script de control y este archivo.
2. **Abrir una terminal** de comandos en la ruta del proyecto.
3. **Ejecutar el script principal** con el siguiente comando:

```bash
python3 sistema_de_taxi.py
