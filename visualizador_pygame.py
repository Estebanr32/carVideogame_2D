"""
Visualizador AVL integrado en pygame
Muestra el árbol directamente en la ventana del juego
"""

import pygame
import math

class VisualizadorAVLPygame:
    def __init__(self, pantalla, ancho, alto):
        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        
        # Colores
        self.COLOR_NODO = (100, 150, 255)
        self.COLOR_TEXTO = (255, 255, 255)
        self.COLOR_LINEA = (80, 80, 80)
        self.COLOR_FONDO = (30, 30, 30)
        self.COLOR_ALTURA = (255, 200, 100)
        
        # Fuentes
        try:
            self.font_nodo = pygame.font.Font(None, 20)
            self.font_titulo = pygame.font.Font(None, 32)
            self.font_info = pygame.font.Font(None, 24)
        except:
            self.font_nodo = pygame.font.SysFont('Arial', 16)
            self.font_titulo = pygame.font.SysFont('Arial', 24)
            self.font_info = pygame.font.SysFont('Arial', 20)
        
        self.mostrar_arbol = False
        self.mostrar_estadisticas = False
        self.mostrar_recorridos = False
        self.tipo_recorrido_actual = "inorden"  # inorden, preorden, postorden
    
    def toggle_arbol(self):
        """Alterna la visualización del árbol"""
        self.mostrar_arbol = not self.mostrar_arbol
        return self.mostrar_arbol
    
    def toggle_estadisticas(self):
        """Alterna la visualización de estadísticas"""
        self.mostrar_estadisticas = not self.mostrar_estadisticas
        return self.mostrar_estadisticas
    
    def toggle_recorridos(self):
        """Alterna la visualización de recorridos y cambia el tipo"""
        if not self.mostrar_recorridos:
            self.mostrar_recorridos = True
            self.tipo_recorrido_actual = "inorden"
        else:
            # Rotar entre tipos de recorrido
            tipos = ["inorden", "preorden", "postorden"]
            indice_actual = tipos.index(self.tipo_recorrido_actual)
            siguiente_indice = (indice_actual + 1) % len(tipos)
            
            if siguiente_indice == 0:  # Volver a inorden significa cerrar
                self.mostrar_recorridos = False
            else:
                self.tipo_recorrido_actual = tipos[siguiente_indice]
        
        return self.mostrar_recorridos, self.tipo_recorrido_actual
    
    def dibujar_overlay_arbol(self, arbol_avl):
        """Dibuja el árbol como overlay sobre el juego"""
        if not self.mostrar_arbol or not arbol_avl.raiz:
            return
        
        # Crear superficie semi-transparente
        overlay = pygame.Surface((self.ancho, self.alto))
        overlay.set_alpha(220)
        overlay.fill(self.COLOR_FONDO)
        
        # Título
        titulo = self.font_titulo.render("🌳 Árbol AVL - Obstáculos", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.ancho//2, 30))
        overlay.blit(titulo, titulo_rect)
        
        # Calcular posiciones de nodos
        posiciones = {}
        self._calcular_posiciones(arbol_avl.raiz, self.ancho//2, 80, 
                                 self.ancho//4, posiciones)
        
        # Dibujar líneas (conexiones)
        self._dibujar_conexiones(overlay, arbol_avl.raiz, posiciones)
        
        # Dibujar nodos
        self._dibujar_nodos(overlay, arbol_avl.raiz, posiciones)
        
        # Información adicional
        self._dibujar_info_arbol(overlay, arbol_avl)
        
        # Instrucciones
        instrucciones = [
            "V: Ocultar árbol",
            "E: Ver estadísticas", 
            "Auto-eliminación: ON ♻️"
        ]
        
        for i, instruccion in enumerate(instrucciones):
            texto = self.font_info.render(instruccion, True, (200, 200, 200))
            overlay.blit(texto, (10, self.alto - 80 + i * 25))
        
        self.pantalla.blit(overlay, (0, 0))
    
    def dibujar_overlay_estadisticas(self, arbol_avl):
        """Dibuja estadísticas como overlay"""
        if not self.mostrar_estadisticas or not arbol_avl.raiz:
            return
        
        # Crear superficie semi-transparente
        overlay = pygame.Surface((400, 300))
        overlay.set_alpha(230)
        overlay.fill((40, 40, 60))
        
        # Borde
        pygame.draw.rect(overlay, (100, 100, 150), overlay.get_rect(), 3)
        
        # Título
        titulo = self.font_titulo.render("📊 Estadísticas AVL", True, (255, 255, 255))
        overlay.blit(titulo, (20, 20))
        
        # Obtener estadísticas
        altura = arbol_avl.obtener_altura()
        total_nodos = arbol_avl.contar_nodos()
        altura_ideal = max(1, total_nodos.bit_length() - 1) if total_nodos > 0 else 1
        eficiencia = (altura_ideal / altura * 100) if altura > 0 else 100
        
        # Mostrar estadísticas
        stats = [
            f"Altura actual: {altura}",
            f"Total nodos: {total_nodos}",
            f"Altura ideal: {altura_ideal}",
            f"Eficiencia: {eficiencia:.1f}%",
            f"Estado: {'✅ Balanceado' if eficiencia > 70 else '⚠️ Puede mejorar'}"
        ]
        
        y_pos = 60
        for stat in stats:
            color = (150, 255, 150) if "✅" in stat else (255, 255, 150) if "⚠️" in stat else (255, 255, 255)
            texto = self.font_info.render(stat, True, color)
            overlay.blit(texto, (20, y_pos))
            y_pos += 30
        
        # Gráfico de barras simple
        bar_y = 200
        bar_height = 20
        max_width = 300
        
        # Barra de altura actual
        altura_width = min(altura * 30, max_width)
        pygame.draw.rect(overlay, (255, 100, 100), 
                        (20, bar_y, altura_width, bar_height))
        
        # Barra de altura ideal
        ideal_width = min(altura_ideal * 30, max_width)
        pygame.draw.rect(overlay, (100, 255, 100), 
                        (20, bar_y + 30, ideal_width, bar_height))
        
        # Etiquetas
        label1 = self.font_info.render("Altura actual", True, (255, 255, 255))
        label2 = self.font_info.render("Altura ideal", True, (255, 255, 255))
        overlay.blit(label1, (330, bar_y))
        overlay.blit(label2, (330, bar_y + 30))
        
        # Posicionar en la esquina superior derecha
        pos_x = self.ancho - 420
        pos_y = 20
        
        self.pantalla.blit(overlay, (pos_x, pos_y))
    
    def dibujar_overlay_recorridos(self, arbol_avl):
        """Dibuja la visualización de recorridos como overlay"""
        if not self.mostrar_recorridos or not arbol_avl.raiz:
            return
        
        # Crear superficie para recorridos
        overlay = pygame.Surface((600, 400))
        overlay.set_alpha(240)
        overlay.fill((20, 20, 40))
        
        # Borde
        pygame.draw.rect(overlay, (100, 150, 255), overlay.get_rect(), 3)
        
        # Título según el tipo de recorrido
        titulos = {
            "inorden": "📋 Recorrido INORDEN (Izq → Raíz → Der)",
            "preorden": "📋 Recorrido PREORDEN (Raíz → Izq → Der)", 
            "postorden": "📋 Recorrido POSTORDEN (Izq → Der → Raíz)"
        }
        
        titulo = self.font_titulo.render(titulos[self.tipo_recorrido_actual], True, (255, 255, 255))
        overlay.blit(titulo, (20, 20))
        
        # Obtener el recorrido según el tipo
        if self.tipo_recorrido_actual == "inorden":
            recorrido = arbol_avl.recorrido_inorden()
        elif self.tipo_recorrido_actual == "preorden":
            recorrido = arbol_avl.recorrido_preorden()
        else:  # postorden
            recorrido = arbol_avl.recorrido_postorden()
        
        # Mostrar elementos del recorrido
        y_pos = 70
        elementos_por_fila = 2
        for i, obs in enumerate(recorrido):
            if i >= 12:  # Limitar a 12 elementos para que quepan
                texto_mas = self.font_info.render(f"... y {len(recorrido) - i} más", True, (200, 200, 200))
                overlay.blit(texto_mas, (20, y_pos))
                break
            
            # Color según el tipo de obstáculo
            colores_tipo = {
                'roca': (255, 100, 100),
                'cono': (255, 200, 100), 
                'hueco': (150, 100, 255),
                'aceite': (100, 200, 100)
            }
            color = colores_tipo.get(obs['tipo'], (255, 255, 255))
            
            # Texto del elemento
            texto = f"{i+1}. ({obs['x']},{obs['y']}) {obs['tipo'].upper()}"
            texto_surface = self.font_info.render(texto, True, color)
            
            # Posición en columnas
            x_pos = 20 + (i % elementos_por_fila) * 280
            if i % elementos_por_fila == 0 and i > 0:
                y_pos += 30
            
            overlay.blit(texto_surface, (x_pos, y_pos))
        
        # Instrucciones
        instrucciones = [
            "T: Cambiar tipo de recorrido",
            "Inorden → Preorden → Postorden → Cerrar"
        ]
        
        for i, instruccion in enumerate(instrucciones):
            texto = self.font_info.render(instruccion, True, (200, 200, 200))
            overlay.blit(texto, (20, 320 + i * 25))
        
        # Posicionar en el centro-derecha
        pos_x = self.ancho - 620
        pos_y = 100
        
        self.pantalla.blit(overlay, (pos_x, pos_y))
    
    def _calcular_posiciones(self, nodo, x, y, separacion, posiciones):
        """Calcula las posiciones de todos los nodos recursivamente"""
        if not nodo:
            return
        
        posiciones[id(nodo)] = (x, y)
        
        # Calcular posiciones de hijos
        if nodo.izquierdo:
            self._calcular_posiciones(nodo.izquierdo, x - separacion, y + 60,
                                    separacion * 0.7, posiciones)
        
        if nodo.derecho:
            self._calcular_posiciones(nodo.derecho, x + separacion, y + 60,
                                    separacion * 0.7, posiciones)
    
    def _dibujar_conexiones(self, superficie, nodo, posiciones):
        """Dibuja las líneas que conectan los nodos"""
        if not nodo:
            return
        
        x, y = posiciones[id(nodo)]
        
        # Conexión al hijo izquierdo
        if nodo.izquierdo:
            x_hijo, y_hijo = posiciones[id(nodo.izquierdo)]
            pygame.draw.line(superficie, self.COLOR_LINEA, (x, y), (x_hijo, y_hijo), 2)
            self._dibujar_conexiones(superficie, nodo.izquierdo, posiciones)
        
        # Conexión al hijo derecho
        if nodo.derecho:
            x_hijo, y_hijo = posiciones[id(nodo.derecho)]
            pygame.draw.line(superficie, self.COLOR_LINEA, (x, y), (x_hijo, y_hijo), 2)
            self._dibujar_conexiones(superficie, nodo.derecho, posiciones)
    
    def _dibujar_nodos(self, superficie, nodo, posiciones):
        """Dibuja todos los nodos del árbol"""
        if not nodo:
            return
        
        x, y = posiciones[id(nodo)]
        
        # Dibujar círculo del nodo
        radio = 25
        pygame.draw.circle(superficie, self.COLOR_NODO, (int(x), int(y)), radio)
        pygame.draw.circle(superficie, (255, 255, 255), (int(x), int(y)), radio, 2)
        
        # Texto del nodo (coordenadas x,y del obstáculo)
        obs = nodo.obstaculo
        texto_principal = f"({obs['x']},{obs['y']})"
        texto_surface = self.font_nodo.render(texto_principal, True, self.COLOR_TEXTO)
        texto_rect = texto_surface.get_rect(center=(x, y - 5))
        superficie.blit(texto_surface, texto_rect)
        
        # Altura del nodo
        altura_texto = f"h={nodo.altura}"
        altura_surface = self.font_nodo.render(altura_texto, True, self.COLOR_ALTURA)
        altura_rect = altura_surface.get_rect(center=(x, y + 8))
        superficie.blit(altura_surface, altura_rect)
        
        # Tipo de obstáculo (abreviado)
        tipo_abrev = obs['tipo'][:3].upper()
        tipo_surface = self.font_nodo.render(tipo_abrev, True, (200, 200, 255))
        tipo_rect = tipo_surface.get_rect(center=(x, y + 35))
        superficie.blit(tipo_surface, tipo_rect)
        
        # Dibujar hijos recursivamente
        if nodo.izquierdo:
            self._dibujar_nodos(superficie, nodo.izquierdo, posiciones)
        
        if nodo.derecho:
            self._dibujar_nodos(superficie, nodo.derecho, posiciones)
    
    def _dibujar_info_arbol(self, superficie, arbol_avl):
        """Dibuja información adicional del árbol"""
        # Información en la parte inferior
        altura = arbol_avl.obtener_altura()
        total_nodos = arbol_avl.contar_nodos()
        
        info_texto = f"Altura: {altura} | Nodos: {total_nodos} | Auto-limpieza activa ♻️"
        info_surface = self.font_info.render(info_texto, True, (255, 255, 255))
        info_rect = info_surface.get_rect(center=(self.ancho//2, self.alto - 120))
        superficie.blit(info_surface, info_rect)
        
        # Estado del balance
        altura_ideal = max(1, total_nodos.bit_length() - 1) if total_nodos > 0 else 1
        balance_ok = altura <= 2 * altura_ideal
        estado_texto = "✅ Árbol bien balanceado" if balance_ok else "⚠️ Árbol puede optimizarse"
        color_estado = (150, 255, 150) if balance_ok else (255, 255, 150)
        
        estado_surface = self.font_info.render(estado_texto, True, color_estado)
        estado_rect = estado_surface.get_rect(center=(self.ancho//2, self.alto - 95))
        superficie.blit(estado_surface, estado_rect)
    
    def cerrar_visualizaciones(self):
        """Cierra todas las visualizaciones"""
        self.mostrar_arbol = False
        self.mostrar_estadisticas = False
        self.mostrar_recorridos = False
        print("🔄 Visualizaciones cerradas")