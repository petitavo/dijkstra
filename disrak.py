import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

# Función para generar la matriz simétrica aleatoria con aristas esparsas
def generar_matriz_esparcida(n, densidad=0.5):
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < densidad:
                valor = np.random.randint(1, 10)
                A[i, j] = valor
                A[j, i] = valor  # Simetría
    np.fill_diagonal(A, 0)  # Asegurar que la diagonal tenga ceros
    return A

# Función para que el usuario ingrese manualmente la matriz
def ingresar_matriz(n):
    A = np.zeros((n, n), dtype=int)
    print("Ingrese los elementos de la matriz simétrica:")
    for i in range(n):
        for j in range(i + 1, n):  # Solo se pide la mitad superior de la matriz
            while True:
                try:
                    valor = int(input(f"Elemento [{i+1},{j+1}]: "))
                    if valor >= 0:
                        A[i, j] = valor
                        A[j, i] = valor  # Simetría
                        break
                    else:
                        print("Por favor, ingrese un valor no negativo.")
                except ValueError:
                    print("Entrada inválida. Ingrese un número entero no negativo.")
    return A

# Entrada del tamaño de la matriz
while True:
    try:
        n = int(input("Ingrese el tamaño de la matriz (n entre 8 y 16): "))
        if 8 <= n <= 16:
            break
        else:
            print("El tamaño de la matriz debe estar entre 8 y 16.")
    except ValueError:
        print("Entrada inválida. Ingrese un número entero.")

# Decisión del usuario: aleatoria o manual
opcion = input("¿Desea generar la matriz aleatoriamente? (s/n): ").strip().lower()

if opcion == 's':
    A = generar_matriz_esparcida(n)  # Usamos densidad fija (0.5)
else:
    A = ingresar_matriz(n)

print("\nMatriz de adyacencia simétrica:")
print(A)

# Crear un grafo no dirigido
G = nx.Graph()

# Agregar nodos y aristas al grafo
for i in range(n):
    for j in range(i + 1, n):  # Solo parte superior para evitar duplicados
        if A[i, j] != 0:  # Si hay una arista con peso
            G.add_edge(i, j, weight=A[i, j])

# Mostrar información del grafo
print("\nGrafo etiquetado (aristas con pesos):")
for u, v, data in G.edges(data=True):
    print(f"({chr(u + 65)} -- {chr(v + 65)}) con peso {data['weight']}")

# Ajustar el tamaño de la figura para mejor visibilidad
plt.figure(figsize=(10, 10) if n >= 11 else (8, 8))

# Disposición circular del grafo
if n >= 11:
    pos = nx.circular_layout(G, scale=2)  # Mayor espaciado para n >= 11
else:
    pos = nx.spring_layout(G, seed=42)  # Normalizar la distribución de los nodos

# Dibujar nodos y etiquetas de nodos
nx.draw(G, pos, with_labels=True, labels={i: chr(i + 65) for i in range(n)},
        node_color='lightblue', node_size=1500, font_size=14, font_weight='bold',
        font_color='black', edgecolors='black', linewidths=1.5)

# Etiquetas de pesos en las aristas
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)

# Mostrar el gráfico
plt.title("Visualización del Grafo")
plt.show()
