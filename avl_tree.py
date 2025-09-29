"""
Implementación del Árbol AVL para gestionar obstáculos dinámicamente
"""

class NodoAVL:
    def __init__(self, obstaculo):
        self.obstaculo = obstaculo
        self.altura = 1
        self.izquierdo = None
        self.derecho = None
    
    def __str__(self):
        return f"Obstáculo(x={self.obstaculo['x']}, y={self.obstaculo['y']}, tipo={self.obstaculo['tipo']})"

class ArbolAVL:
    def __init__(self):
        self.raiz = None
    
    def altura(self, nodo):
        """Obtiene la altura de un nodo"""
        if not nodo:
            return 0
        return nodo.altura
    
    def factor_balance(self, nodo):
        """Calcula el factor de balance de un nodo"""
        if not nodo:
            return 0
        return self.altura(nodo.izquierdo) - self.altura(nodo.derecho)
    
    def actualizar_altura(self, nodo):
        """Actualiza la altura de un nodo"""
        if nodo:
            nodo.altura = 1 + max(self.altura(nodo.izquierdo), self.altura(nodo.derecho))
    
    def rotar_derecha(self, y):
        """Rotación simple a la derecha"""
        x = y.izquierdo
        T2 = x.derecho
        
        # Realizar rotación
        x.derecho = y
        y.izquierdo = T2
        
        # Actualizar alturas
        self.actualizar_altura(y)
        self.actualizar_altura(x)
        
        return x
    
    def rotar_izquierda(self, x):
        """Rotación simple a la izquierda"""
        y = x.derecho
        T2 = y.izquierdo
        
        # Realizar rotación
        y.izquierdo = x
        x.derecho = T2
        
        # Actualizar alturas
        self.actualizar_altura(x)
        self.actualizar_altura(y)
        
        return y
    
    def insertar(self, obstaculo):
        """Inserta un obstáculo en el árbol AVL"""
        self.raiz = self._insertar_recursivo(self.raiz, obstaculo)
    
    def _insertar_recursivo(self, nodo, obstaculo):
        """Función recursiva para insertar en el árbol"""
        # Paso 1: Inserción normal de BST
        if not nodo:
            return NodoAVL(obstaculo)
        
        # Comparar primero por x, luego por y en caso de empate
        if obstaculo['x'] < nodo.obstaculo['x']:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, obstaculo)
        elif obstaculo['x'] > nodo.obstaculo['x']:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, obstaculo)
        else:  # x es igual, comparar por y
            if obstaculo['y'] < nodo.obstaculo['y']:
                nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, obstaculo)
            elif obstaculo['y'] > nodo.obstaculo['y']:
                nodo.derecho = self._insertar_recursivo(nodo.derecho, obstaculo)
            else:
                # No se permiten coordenadas repetidas
                return nodo
        
        # Paso 2: Actualizar altura del nodo actual
        self.actualizar_altura(nodo)
        
        # Paso 3: Obtener factor de balance
        balance = self.factor_balance(nodo)
        
        # Paso 4: Si el nodo está desbalanceado, hay 4 casos
        
        # Caso Izquierda-Izquierda
        if balance > 1 and ((obstaculo['x'] < nodo.izquierdo.obstaculo['x']) or 
                           (obstaculo['x'] == nodo.izquierdo.obstaculo['x'] and 
                            obstaculo['y'] < nodo.izquierdo.obstaculo['y'])):
            return self.rotar_derecha(nodo)
        
        # Caso Derecha-Derecha
        if balance < -1 and ((obstaculo['x'] > nodo.derecho.obstaculo['x']) or 
                            (obstaculo['x'] == nodo.derecho.obstaculo['x'] and 
                             obstaculo['y'] > nodo.derecho.obstaculo['y'])):
            return self.rotar_izquierda(nodo)
        
        # Caso Izquierda-Derecha
        if balance > 1 and ((obstaculo['x'] > nodo.izquierdo.obstaculo['x']) or 
                           (obstaculo['x'] == nodo.izquierdo.obstaculo['x'] and 
                            obstaculo['y'] > nodo.izquierdo.obstaculo['y'])):
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)
        
        # Caso Derecha-Izquierda
        if balance < -1 and ((obstaculo['x'] < nodo.derecho.obstaculo['x']) or 
                            (obstaculo['x'] == nodo.derecho.obstaculo['x'] and 
                             obstaculo['y'] < nodo.derecho.obstaculo['y'])):
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)
        
        # Retornar nodo sin cambios
        return nodo
    
    def eliminar(self, x, y):
        """Elimina un obstáculo del árbol por coordenadas"""
        self.raiz = self._eliminar_recursivo(self.raiz, x, y)
    
    def _eliminar_recursivo(self, nodo, x, y):
        """Función recursiva para eliminar del árbol"""
        if not nodo:
            return nodo
        
        # Buscar el nodo a eliminar
        if x < nodo.obstaculo['x']:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, x, y)
        elif x > nodo.obstaculo['x']:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, x, y)
        else:  # x es igual
            if y < nodo.obstaculo['y']:
                nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, x, y)
            elif y > nodo.obstaculo['y']:
                nodo.derecho = self._eliminar_recursivo(nodo.derecho, x, y)
            else:
                # Este es el nodo a eliminar
                if not nodo.izquierdo:
                    return nodo.derecho
                elif not nodo.derecho:
                    return nodo.izquierdo
                
                # Nodo con dos hijos - obtener sucesor
                temp = self._obtener_minimo(nodo.derecho)
                nodo.obstaculo = temp.obstaculo
                nodo.derecho = self._eliminar_recursivo(nodo.derecho, 
                                                       temp.obstaculo['x'], 
                                                       temp.obstaculo['y'])
        
        # Actualizar altura y rebalancear
        self.actualizar_altura(nodo)
        balance = self.factor_balance(nodo)
        
        # Rebalancear si es necesario
        if balance > 1 and self.factor_balance(nodo.izquierdo) >= 0:
            return self.rotar_derecha(nodo)
        
        if balance > 1 and self.factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)
        
        if balance < -1 and self.factor_balance(nodo.derecho) <= 0:
            return self.rotar_izquierda(nodo)
        
        if balance < -1 and self.factor_balance(nodo.derecho) > 0:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)
        
        return nodo
    
    def _obtener_minimo(self, nodo):
        """Obtiene el nodo con valor mínimo"""
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return nodo
    
    def buscar_en_rango(self, x_min, x_max, y_min, y_max):
        """Busca obstáculos dentro de un rango de coordenadas"""
        obstaculos = []
        self._buscar_en_rango_recursivo(self.raiz, x_min, x_max, y_min, y_max, obstaculos)
        return obstaculos
    
    def _buscar_en_rango_recursivo(self, nodo, x_min, x_max, y_min, y_max, obstaculos):
        """Función recursiva para buscar en rango"""
        if not nodo:
            return
        
        # Si el obstáculo está en el rango, agregarlo
        if (x_min <= nodo.obstaculo['x'] <= x_max and 
            y_min <= nodo.obstaculo['y'] <= y_max):
            obstaculos.append(nodo.obstaculo)
        
        # Buscar en subárboles si es necesario
        if x_min <= nodo.obstaculo['x']:
            self._buscar_en_rango_recursivo(nodo.izquierdo, x_min, x_max, y_min, y_max, obstaculos)
        
        if x_max >= nodo.obstaculo['x']:
            self._buscar_en_rango_recursivo(nodo.derecho, x_min, x_max, y_min, y_max, obstaculos)
    
    def obtener_obstaculos_visibles(self, carrito_x, pantalla_ancho):
        """Obtiene obstáculos visibles en pantalla"""
        x_min = max(0, carrito_x - pantalla_ancho // 4)
        x_max = carrito_x + pantalla_ancho
        y_min = 0
        y_max = 600  # Altura de pantalla
        
        return self.buscar_en_rango(x_min, x_max, y_min, y_max)
    
    def recorrido_inorden(self):
        """Recorrido en orden del árbol para mostrar obstáculos ordenados"""
        obstaculos = []
        self._inorden_recursivo(self.raiz, obstaculos)
        return obstaculos
    
    def _inorden_recursivo(self, nodo, obstaculos):
        """Función recursiva para recorrido en orden"""
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, obstaculos)
            obstaculos.append(nodo.obstaculo)
            self._inorden_recursivo(nodo.derecho, obstaculos)
    
    def mostrar_estructura(self, nodo=None, nivel=0, prefijo="Raíz: "):
        """Muestra la estructura del árbol para debugging"""
        if nodo is None:
            nodo = self.raiz
        
        if nodo is not None:
            print(" " * (nivel * 4) + prefijo + str(nodo.obstaculo) + f" (h={nodo.altura}, b={self.factor_balance(nodo)})")
            if nodo.izquierdo or nodo.derecho:
                if nodo.izquierdo:
                    self.mostrar_estructura(nodo.izquierdo, nivel + 1, "I--- ")
                else:
                    print(" " * ((nivel + 1) * 4) + "I--- None")
                
                if nodo.derecho:
                    self.mostrar_estructura(nodo.derecho, nivel + 1, "D--- ")
                else:
                    print(" " * ((nivel + 1) * 4) + "D--- None")
    
    def obtener_altura(self):
        """Obtiene la altura total del árbol"""
        return self.altura(self.raiz)
    
    def contar_nodos(self):
        """Cuenta el total de nodos en el árbol"""
        return self._contar_recursivo(self.raiz)
    
    def _contar_recursivo(self, nodo):
        """Función recursiva para contar nodos"""
        if not nodo:
            return 0
        return 1 + self._contar_recursivo(nodo.izquierdo) + self._contar_recursivo(nodo.derecho)
    
    def recorrido_preorden(self):
        """Recorrido en preorden del árbol (Raíz -> Izquierda -> Derecha)"""
        obstaculos = []
        self._preorden_recursivo(self.raiz, obstaculos)
        return obstaculos
    
    def _preorden_recursivo(self, nodo, obstaculos):
        """Función recursiva para recorrido en preorden"""
        if nodo:
            obstaculos.append(nodo.obstaculo)  # Visitar raíz primero
            self._preorden_recursivo(nodo.izquierdo, obstaculos)
            self._preorden_recursivo(nodo.derecho, obstaculos)
    
    def recorrido_postorden(self):
        """Recorrido en postorden del árbol (Izquierda -> Derecha -> Raíz)"""
        obstaculos = []
        self._postorden_recursivo(self.raiz, obstaculos)
        return obstaculos
    
    def _postorden_recursivo(self, nodo, obstaculos):
        """Función recursiva para recorrido en postorden"""
        if nodo:
            self._postorden_recursivo(nodo.izquierdo, obstaculos)
            self._postorden_recursivo(nodo.derecho, obstaculos)
            obstaculos.append(nodo.obstaculo)  # Visitar raíz al final