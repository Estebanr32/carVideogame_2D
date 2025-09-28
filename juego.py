import pygame
import sys
import json
import time
from avl_tree import ArbolAVL
from visualizador_pygame import VisualizadorAVLPygame
from carrito import Carrito
from obstaculo import Obstaculo

# Constantes del juego
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CARRIL_WIDTH = 120  # Ancho de cada carril
NUM_CARRILES = 6     # 3 carriles por cada lado
CARRETERA_Y = 200    # Posición Y de la carretera
CARRETERA_HEIGHT = 200  # Altura de la carretera

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_BLUE = (25, 25, 112)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

class JuegoCarrito:
    """Clase principal del juego de carrito con obstáculos dinámicos"""
    
    def __init__(self):
        # Usar pantalla existente del menú
        self.screen = pygame.display.get_surface()
        if self.screen is None:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🚗 Juego de Carrito con Obstáculos Dinámicos - Árbol AVL 🌳")
        
        # Cargar configuración
        self.cargar_configuracion()
        
        # Inicializar componentes
        self.carrito = Carrito(self.config['config'])
        self.arbol_obstaculos = ArbolAVL()
        self.cargar_obstaculos()
        
        # Variables de juego
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.ultimo_avance = time.time()
        self.juego_terminado = False
        self.victoria = False
        
        # Variables para controlar el movimiento automático
        self.ultimo_movimiento = time.time()
        self.intervalo_movimiento = self.config['config']['refresco_ms'] / 1000.0
        
        # Variables para inserción de obstáculos
        self.modo_insercion = False
        self.datos_insercion = {'x': '', 'y': '', 'tipo': 'roca'}
        self.campo_activo = 'x'  # 'x', 'y', o 'tipo'
        self.tipos_disponibles = ['roca', 'cono', 'hueco', 'aceite']
        self.indice_tipo = 0
        
        # Visualizador del árbol AVL integrado en pygame
        self.visualizador = VisualizadorAVLPygame(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        print("✅ Visualizador AVL pygame inicializado")
    
    def cargar_configuracion(self):
        """Carga la configuración desde el archivo JSON"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("Error: No se encontró el archivo config.json")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: El archivo config.json no es válido")
            sys.exit(1)
    
    def cargar_obstaculos(self):
        """Carga obstáculos desde la configuración al árbol AVL"""
        print("\n=== Cargando obstáculos en el Árbol AVL ===")
        for obstaculo_data in self.config['obstaculos']:
            self.arbol_obstaculos.insertar(obstaculo_data)
            print(f"Insertado: {obstaculo_data}")
        
        print("\n=== Estructura del Árbol AVL ===")
        self.arbol_obstaculos.mostrar_estructura()
        
        print("\n=== Recorrido en orden ===")
        obstaculos_ordenados = self.arbol_obstaculos.recorrido_inorden()
        for obs in obstaculos_ordenados:
            print(f"x={obs['x']}, y={obs['y']}, tipo={obs['tipo']}")
    
    def reiniciar_juego(self):
        """Reinicia el juego al estado inicial"""
        # Reinicializar carrito
        self.carrito = Carrito(self.config['config'])
        
        # Reinicializar árbol de obstáculos
        self.arbol_obstaculos = ArbolAVL()
        self.cargar_obstaculos()
        
        # Reinicializar variables de juego
        self.juego_terminado = False
        self.victoria = False
        self.ultimo_movimiento = time.time()
        
        print("🔄 Juego reiniciado")
    
    def handle_events(self):
        """Maneja los eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                # Si estamos en modo inserción, manejar esos eventos primero
                if self.modo_insercion:
                    self.manejar_entrada_insercion(event)
                else:
                    # Controles normales del juego
                    if event.key == pygame.K_UP:
                        self.carrito.mover_arriba()
                    elif event.key == pygame.K_DOWN:
                        self.carrito.mover_abajo()
                    elif event.key == pygame.K_SPACE:
                        self.carrito.saltar()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r and self.juego_terminado:
                        self.reiniciar_juego()
                    elif event.key == pygame.K_v:
                        self.mostrar_visualizacion_arbol()
                    elif event.key == pygame.K_e:
                        self.mostrar_estadisticas_arbol()
                    elif event.key == pygame.K_c:
                        self.cerrar_ventanas_matplotlib()
                    elif event.key == pygame.K_t:
                        self.mostrar_recorridos_arbol()
                    elif event.key == pygame.K_i:
                        self.alternar_modo_insercion()
        
        return True
    
    def actualizar_juego(self):
        """Actualiza la lógica del juego"""
        if self.juego_terminado:
            return
        
        tiempo_actual = time.time()
        
        # Movimiento automático del carrito
        if tiempo_actual - self.ultimo_movimiento >= self.intervalo_movimiento:
            self.carrito.distancia_recorrida += self.config['config']['velocidad']
            self.ultimo_movimiento = tiempo_actual
            
            # Verificar si llegó al final
            if self.carrito.distancia_recorrida >= self.config['config']['distancia_total']:
                self.victoria = True
                self.juego_terminado = True
        
        # Actualizar salto
        self.carrito.actualizar_salto()
        
        # Verificar colisiones con obstáculos visibles
        self.verificar_colisiones()
        
        # Eliminar obstáculos que han salido de la pantalla
        self.limpiar_obstaculos_fuera_pantalla()
        
        # Verificar si el carrito perdió toda su energía
        if not self.carrito.esta_vivo():
            self.juego_terminado = True
    
    def verificar_colisiones(self):
        """Verifica colisiones usando el árbol AVL"""
        obstaculos_visibles = self.arbol_obstaculos.obtener_obstaculos_visibles(
            self.carrito.distancia_recorrida, SCREEN_WIDTH)
        
        for obs_data in obstaculos_visibles:
            obstaculo = Obstaculo(obs_data['x'], obs_data['y'], obs_data['tipo'])
            
            if obstaculo.colisiona_con_carrito(self.carrito):
                dano = obstaculo.config['energia_perdida']
                self.carrito.recibir_dano(dano)
                
                print(f"¡Colisión con {obs_data['tipo']}! Energía perdida: {dano}")
                print(f"Energía restante: {self.carrito.energia}")
                
                # Eliminar obstáculo del árbol
                self.arbol_obstaculos.eliminar(obs_data['x'], obs_data['y'])
                print("💡 Presiona 'V' para ver cómo cambió el árbol AVL")
                break
    
    def limpiar_obstaculos_fuera_pantalla(self):
        """Elimina obstáculos que han salido de la pantalla"""
        posicion_limite = self.carrito.distancia_recorrida - 100
        
        # Buscar obstáculos fuera de rango
        obstaculos_a_eliminar = []
        obstaculos_actuales = self.arbol_obstaculos.recorrido_inorden()
        
        for obs in obstaculos_actuales:
            if obs['x'] < posicion_limite:
                obstaculos_a_eliminar.append(obs)
        
        # Eliminar obstáculos encontrados
        if obstaculos_a_eliminar:
            print(f"🧹 Limpiando {len(obstaculos_a_eliminar)} obstáculos fuera de pantalla")
            for obs in obstaculos_a_eliminar:
                self.arbol_obstaculos.eliminar(obs['x'], obs['y'])
                print(f"   Eliminado: x={obs['x']}, y={obs['y']}, tipo={obs['tipo']}")
            print("💡 Presiona 'V' para ver cómo se rebalanceó el árbol automáticamente")
    
    def draw_carretera(self):
        """Dibuja la carretera con líneas divisorias"""
        # Dibujar fondo de carretera
        pygame.draw.rect(self.screen, GRAY, (0, CARRETERA_Y, SCREEN_WIDTH, CARRETERA_HEIGHT))
        
        # Líneas divisorias entre carriles
        for i in range(1, NUM_CARRILES):
            y = CARRETERA_Y + (i * CARRETERA_HEIGHT // NUM_CARRILES)
            for x in range(0, SCREEN_WIDTH, 40):
                pygame.draw.line(self.screen, WHITE, (x, y), (x + 20, y), 2)
    
    def draw_ui(self):
        """Dibuja la interfaz de usuario"""
        # Barra de energía
        energia_width = int((self.carrito.energia / 100) * 200)
        energia_color = GREEN if self.carrito.energia > 50 else (YELLOW if self.carrito.energia > 25 else RED)
        
        pygame.draw.rect(self.screen, RED, (10, 10, 200, 20))
        pygame.draw.rect(self.screen, energia_color, (10, 10, energia_width, 20))
        pygame.draw.rect(self.screen, WHITE, (10, 10, 200, 20), 2)
        
        # Texto de energía
        energia_text = self.font_small.render(f"Energía: {self.carrito.energia}%", True, WHITE)
        self.screen.blit(energia_text, (220, 12))
        
        # Distancia recorrida
        distancia_text = self.font_small.render(
            f"Distancia: {self.carrito.distancia_recorrida}/{self.config['config']['distancia_total']}m", 
            True, WHITE)
        self.screen.blit(distancia_text, (10, 40))
        
        # Carril actual
        carril_text = self.font_small.render(f"Carril: {self.carrito.y + 1}/6", True, WHITE)
        self.screen.blit(carril_text, (10, 65))
        
        # Información del árbol AVL
        altura = self.arbol_obstaculos.altura(self.arbol_obstaculos.raiz)
        total = self.arbol_obstaculos.contar_nodos()
        arbol_text = self.font_small.render(f"Árbol AVL - Altura: {altura} | Nodos: {total}", True, WHITE)
        self.screen.blit(arbol_text, (SCREEN_WIDTH - 300, 12))
        
        # Instrucciones de controles
        if not self.juego_terminado:
            instrucciones = [
                "↑↓: Carriles",
                "ESPACIO: Saltar",
                "V: Ver Árbol AVL",
                "E: Estadísticas",
                "T: Recorridos",
                "I: Insertar obstáculo",
                "C: Cerrar ventanas",
                "ESC: Salir"
            ]
            for i, instruccion in enumerate(instrucciones):
                text = self.font_small.render(instruccion, True, WHITE)
                self.screen.blit(text, (SCREEN_WIDTH - 170, 10 + i * 20))
    
    def draw_obstaculos(self):
        """Dibuja los obstáculos visibles"""
        obstaculos_visibles = self.arbol_obstaculos.obtener_obstaculos_visibles(
            self.carrito.distancia_recorrida, SCREEN_WIDTH)
        
        for obs_data in obstaculos_visibles:
            obstaculo = Obstaculo(obs_data['x'], obs_data['y'], obs_data['tipo'])
            obstaculo.draw(self.screen, self.carrito.distancia_recorrida)
    
    def draw_game_over(self):
        """Dibuja la pantalla de game over"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        if self.victoria:
            titulo = "¡VICTORIA!"
            mensaje = f"¡Completaste el recorrido de {self.config['config']['distancia_total']}m!"
            color = GREEN
        else:
            titulo = "GAME OVER"
            mensaje = "Te quedaste sin energía"
            color = RED
        
        titulo_text = self.font.render(titulo, True, color)
        titulo_rect = titulo_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(titulo_text, titulo_rect)
        
        mensaje_text = self.font_small.render(mensaje, True, WHITE)
        mensaje_rect = mensaje_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10))
        self.screen.blit(mensaje_text, mensaje_rect)
        
        reiniciar_text = self.font_small.render("R: Reiniciar | ESC: Menú Principal | Q: Salir", True, WHITE)
        reiniciar_rect = reiniciar_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
        self.screen.blit(reiniciar_text, reiniciar_rect)
    
    def dibujar_interfaz_insercion(self):
        """Dibuja la interfaz para insertar obstáculos"""
        # Panel de fondo
        panel_width = 400
        panel_height = 200
        panel_x = SCREEN_WIDTH - panel_width - 10
        panel_y = 10
        
        # Fondo semi-transparente
        overlay = pygame.Surface((panel_width, panel_height))
        overlay.set_alpha(220)
        overlay.fill(DARK_BLUE)
        self.screen.blit(overlay, (panel_x, panel_y))
        
        # Borde
        pygame.draw.rect(self.screen, GOLD, (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Título
        titulo = self.font_small.render("🔧 INSERTAR OBSTÁCULO", True, GOLD)
        self.screen.blit(titulo, (panel_x + 10, panel_y + 10))
        
        # Campos de entrada
        y_offset = 40
        campos = [
            ('X (coordenada)', self.datos_insercion['x']),
            ('Y (carril 0-5)', self.datos_insercion['y']),
            ('Tipo', self.datos_insercion['tipo'])
        ]
        
        for i, (etiqueta, valor) in enumerate(campos):
            y_pos = panel_y + y_offset + i * 30
            
            # Destacar campo activo
            campo_nombre = ['x', 'y', 'tipo'][i]
            color_texto = YELLOW if self.campo_activo == campo_nombre else WHITE
            
            # Etiqueta
            etiqueta_text = self.font_small.render(f"{etiqueta}:", True, color_texto)
            self.screen.blit(etiqueta_text, (panel_x + 10, y_pos))
            
            # Valor
            valor_mostrar = valor if valor else "_"
            if campo_nombre == self.campo_activo:
                valor_mostrar += "|"  # Cursor
            
            valor_text = self.font_small.render(valor_mostrar, True, color_texto)
            self.screen.blit(valor_text, (panel_x + 150, y_pos))
        
        # Instrucciones
        instrucciones = [
            "TAB: Cambiar campo",
            "←→: Cambiar tipo (en Tipo)",  
            "ENTER: Insertar",
            "ESC: Cancelar"
        ]
        
        for i, instruccion in enumerate(instrucciones):
            y_pos = panel_y + 130 + i * 16
            texto = pygame.font.Font(None, 20).render(instruccion, True, SILVER)
            self.screen.blit(texto, (panel_x + 10, y_pos))
    
    def draw(self):
        """Dibuja todos los elementos del juego"""
        self.screen.fill(GREEN)  # Césped
        
        # Dibujar carretera
        self.draw_carretera()
        
        # Dibujar obstáculos
        self.draw_obstaculos()
        
        # Dibujar carrito
        self.carrito.draw(self.screen)
        
        # Dibujar UI
        self.draw_ui()
        
        # Dibujar game over si es necesario
        if self.juego_terminado:
            self.draw_game_over()
        
        # Dibujar visualizaciones del árbol AVL (overlays)
        if self.visualizador:
            self.visualizador.dibujar_overlay_arbol(self.arbol_obstaculos)
            self.visualizador.dibujar_overlay_estadisticas(self.arbol_obstaculos)  
            self.visualizador.dibujar_overlay_recorridos(self.arbol_obstaculos)
        
        # Dibujar interfaz de inserción si está activa
        if self.modo_insercion:
            self.dibujar_interfaz_insercion()
        
        pygame.display.flip()
    
    # Métodos de visualización y funcionalidad AVL
    def mostrar_visualizacion_arbol(self):
        """Activa/desactiva la visualización del árbol"""
        if self.visualizador:
            estado = self.visualizador.toggle_arbol()
            print(f"🌳 Visualización del árbol: {'ACTIVADA' if estado else 'DESACTIVADA'}")
    
    def mostrar_estadisticas_arbol(self):
        """Activa/desactiva las estadísticas del árbol"""
        if self.visualizador:
            estado = self.visualizador.toggle_estadisticas()
            print(f"📊 Estadísticas del árbol: {'ACTIVADAS' if estado else 'DESACTIVADAS'}")
    
    def mostrar_recorridos_arbol(self):
        """Activa/desactiva los recorridos del árbol"""
        if self.visualizador:
            estado, tipo = self.visualizador.toggle_recorridos()
            if estado:
                print(f"📋 Recorridos del árbol: ACTIVADOS - Mostrando: {tipo.upper()}")
            else:
                print("📋 Recorridos del árbol: DESACTIVADOS")
    
    def cerrar_ventanas_matplotlib(self):
        """Cierra visualizaciones"""
        if self.visualizador:
            self.visualizador.cerrar_overlays()
        print("🔧 Visualizaciones cerradas")
    
    # Métodos de inserción de obstáculos
    def alternar_modo_insercion(self):
        """Activa/desactiva el modo de inserción de obstáculos"""
        self.modo_insercion = not self.modo_insercion
        if self.modo_insercion:
            # Sugerir valores útiles
            x_sugerido = str(int(self.carrito.distancia_recorrida) + 200)
            
            # Reinicializar datos de inserción
            self.datos_insercion = {'x': '', 'y': '', 'tipo': 'roca'}
            self.campo_activo = 'x'
            self.indice_tipo = 0  # Asegurar que empiece en 'roca'
            
            print("\n🔧 MODO INSERCIÓN ACTIVADO")
            print("   Ingresa las coordenadas y tipo del obstáculo:")
            print("   TAB: Cambiar campo | ENTER: Insertar | ESC: Cancelar")
            print(f"   Campo activo: {self.campo_activo.upper()}")
            print(f"   Posición actual del carrito: {self.carrito.distancia_recorrida}")
            print(f"   💡 Sugerencia X (mayor a posición actual): {x_sugerido}")
            print(f"   💡 Sugerencia Y (carriles 0-5): 2 (centro)")
        else:
            print("🔧 Modo inserción desactivado")
    
    def manejar_entrada_insercion(self, event):
        """Maneja la entrada de datos para insertar obstáculos"""
        print(f"🔧 Tecla presionada en modo inserción: {pygame.key.name(event.key)}")
        
        if event.key == pygame.K_ESCAPE:
            self.modo_insercion = False
            print("🔧 Inserción cancelada")
            return
        
        elif event.key == pygame.K_TAB:
            # Cambiar campo activo
            campos = ['x', 'y', 'tipo']
            indice_actual = campos.index(self.campo_activo)
            self.campo_activo = campos[(indice_actual + 1) % len(campos)]
            print(f"📝 Campo activo: {self.campo_activo.upper()}")
            return
        
        elif event.key == pygame.K_RETURN:
            print("🔧 Intentando insertar obstáculo...")
            self.intentar_insertar_obstaculo()
            return
        
        # Manejar entrada de texto
        if self.campo_activo == 'tipo':
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # Cambiar tipo de obstáculo con flechas
                if event.key == pygame.K_LEFT:
                    self.indice_tipo = (self.indice_tipo - 1) % len(self.tipos_disponibles)
                else:
                    self.indice_tipo = (self.indice_tipo + 1) % len(self.tipos_disponibles)
                self.datos_insercion['tipo'] = self.tipos_disponibles[self.indice_tipo]
                print(f"🎯 Tipo seleccionado: {self.datos_insercion['tipo']}")
        
        elif self.campo_activo in ['x', 'y']:
            if event.key == pygame.K_BACKSPACE:
                # Borrar último carácter
                if len(self.datos_insercion[self.campo_activo]) > 0:
                    self.datos_insercion[self.campo_activo] = self.datos_insercion[self.campo_activo][:-1]
                    print(f"🔙 Borrado - {self.campo_activo.upper()}: '{self.datos_insercion[self.campo_activo]}'")
            elif event.unicode and event.unicode.isdigit():
                # Agregar dígito
                self.datos_insercion[self.campo_activo] += event.unicode
                print(f"➕ Agregado - {self.campo_activo.upper()}: '{self.datos_insercion[self.campo_activo]}'")
            elif event.unicode:
                print(f"❌ Carácter no válido: '{event.unicode}' - Solo números permitidos")
    
    def intentar_insertar_obstaculo(self):
        """Intenta insertar el obstáculo con los datos ingresados"""
        try:
            # Verificar que tengamos datos
            if not self.datos_insercion['x'] or not self.datos_insercion['y']:
                print("❌ Error: Debes ingresar valores para X e Y")
                print(f"   X actual: '{self.datos_insercion['x']}'")
                print(f"   Y actual: '{self.datos_insercion['y']}'")
                return
            
            # Validar datos
            x = int(self.datos_insercion['x'])
            y = int(self.datos_insercion['y'])
            tipo = self.datos_insercion['tipo']
            
            print(f"🔍 Validando: X={x}, Y={y}, Tipo={tipo}")
            print(f"   Posición actual del carrito: {self.carrito.distancia_recorrida}")
            
            # Validar rango de Y (0-5 para 6 carriles)
            if not (0 <= y <= 5):
                print(f"❌ Error: Y debe estar entre 0 y 5 (carriles disponibles)")
                print(f"   Valor ingresado: {y}")
                return
            
            # Validar que X sea mayor a la posición actual del carrito
            if x <= self.carrito.distancia_recorrida:
                print(f"❌ Error: X debe ser mayor a {self.carrito.distancia_recorrida} (posición actual)")
                print(f"   Valor ingresado: {x}")
                return
            
            # Crear obstáculo
            nuevo_obstaculo = {
                'x': x,
                'y': y,
                'tipo': tipo,
                'id': int(time.time() * 1000)  # ID único basado en timestamp
            }
            
            # Insertar en el árbol
            self.arbol_obstaculos.insertar(nuevo_obstaculo)
            
            print(f"✅ Obstáculo insertado exitosamente:")
            print(f"   X: {x}, Y: {y}, Tipo: {tipo}")
            print(f"🌳 Árbol rebalanceado automáticamente")
            
            # Resetear modo inserción
            self.modo_insercion = False
            self.datos_insercion = {'x': '', 'y': '', 'tipo': 'roca'}
            
        except ValueError as e:
            print(f"❌ Error: X e Y deben ser números enteros")
            print(f"   X: '{self.datos_insercion['x']}', Y: '{self.datos_insercion['y']}'")
        except Exception as e:
            print(f"❌ Error al insertar obstáculo: {e}")
    
    def run(self):
        """Bucle principal del juego"""
        clock = pygame.time.Clock()
        running = True
        
        print("\n=== INICIANDO JUEGO ===")
        print("Controles:")
        print("- Flechas ↑↓: Cambiar de carril")
        print("- ESPACIO: Saltar")
        print("- V: Visualizar Árbol AVL 🌳")
        print("- E: Mostrar estadísticas 📊")
        print("- T: Ver recorridos (Inorden/Preorden/Postorden) 📋")
        print("- I: Insertar obstáculos dinámicamente 🔧")
        print("- C: Cerrar visualizaciones")
        print("- ESC: Regresar al menú")
        print("- R: Reiniciar (cuando termine el juego)")
        print("\n🎮 ¡Presiona 'V' durante el juego para ver el árbol en tiempo real!")
        print("♻️  Los obstáculos se eliminan automáticamente al chocar o salir de pantalla")
        
        while running:
            running = self.handle_events()
            self.actualizar_juego()
            self.draw()
            clock.tick(60)  # 60 FPS
        
        # No cerrar pygame, solo regresar al menú
        print("🔙 Regresando al menú principal...")