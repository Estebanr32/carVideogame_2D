import pygame
import math
import sys

# Colores para el menú
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (25, 25, 112)
LIGHT_BLUE = (173, 216, 230)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
DARK_GREEN = (0, 100, 0)

class MenuPrincipal:
    """Menú principal del juego con interfaz atractiva"""
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Obtener dimensiones de pantalla
        self.SCREEN_WIDTH = screen.get_width()
        self.SCREEN_HEIGHT = screen.get_height()
        
        # Fuentes
        self.font_title = pygame.font.Font(None, 80)
        self.font_subtitle = pygame.font.Font(None, 40)
        self.font_button = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Animaciones
        self.tiempo = 0
        self.pulso_titulo = 0
        
        # Botones
        self.botones = {
            'jugar': pygame.Rect(self.SCREEN_WIDTH//2 - 120, 300, 240, 60),
            'instrucciones': pygame.Rect(self.SCREEN_WIDTH//2 - 120, 380, 240, 60),
            'salir': pygame.Rect(self.SCREEN_WIDTH//2 - 120, 460, 240, 60)
        }
        
        self.boton_hover = None
        self.mostrar_instrucciones = False
    
    def manejar_eventos(self):
        """Maneja eventos del menú"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Detectar hover en botones
        self.boton_hover = None
        for nombre, rect in self.botones.items():
            if rect.collidepoint(mouse_pos):
                self.boton_hover = nombre
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'salir'
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.mostrar_instrucciones:
                        self.mostrar_instrucciones = False
                    else:
                        return 'salir'
                elif event.key == pygame.K_RETURN:
                    return 'jugar'
                elif event.key == pygame.K_i:
                    self.mostrar_instrucciones = not self.mostrar_instrucciones
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    if self.mostrar_instrucciones:
                        self.mostrar_instrucciones = False
                    else:
                        for nombre, rect in self.botones.items():
                            if rect.collidepoint(mouse_pos):
                                if nombre == 'jugar':
                                    return 'jugar'
                                elif nombre == 'instrucciones':
                                    self.mostrar_instrucciones = True
                                elif nombre == 'salir':
                                    return 'salir'
        
        return 'menu'
    
    def dibujar_fondo_animado(self):
        """Dibuja un fondo animado con efectos"""
        # Fondo base
        self.screen.fill(DARK_BLUE)
        
        # Estrellas animadas
        for i in range(50):
            x = (i * 37 + self.tiempo * 0.5) % self.SCREEN_WIDTH
            y = (i * 23 + self.tiempo * 0.3) % self.SCREEN_HEIGHT
            brillo = abs(math.sin(self.tiempo * 0.01 + i)) * 255
            color = (int(brillo), int(brillo), int(brillo))
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 2)
        
        # Líneas de carretera decorativas
        for i in range(6):
            y = 150 + i * 50
            for x in range(0, self.SCREEN_WIDTH, 40):
                offset_x = (x + self.tiempo * 2) % 80
                pygame.draw.rect(self.screen, WHITE, (offset_x, y, 20, 4))
    
    def dibujar_titulo(self):
        """Dibuja el título con efecto de pulso"""
        self.pulso_titulo = math.sin(self.tiempo * 0.05) * 10
        
        # Sombra del título
        titulo_shadow = self.font_title.render("CARRITO AVL", True, BLACK)
        shadow_rect = titulo_shadow.get_rect(center=(self.SCREEN_WIDTH//2 + 3, 120 + 3))
        self.screen.blit(titulo_shadow, shadow_rect)
        
        # Título principal con efecto de pulso
        titulo = self.font_title.render("CARRITO AVL", True, GOLD)
        titulo_rect = titulo.get_rect(center=(self.SCREEN_WIDTH//2, 120 + self.pulso_titulo))
        self.screen.blit(titulo, titulo_rect)
        
        # Subtítulo
        subtitulo = self.font_subtitle.render("Obstáculos Dinámicos con Árbol AVL", True, SILVER)
        subtitulo_rect = subtitulo.get_rect(center=(self.SCREEN_WIDTH//2, 160))
        self.screen.blit(subtitulo, subtitulo_rect)
    
    def dibujar_boton(self, nombre, rect, texto):
        """Dibuja un botón con efectos hover"""
        # Color base del botón
        if self.boton_hover == nombre:
            color_fondo = GOLD
            color_texto = BLACK
            # Efecto de brillo
            pygame.draw.rect(self.screen, WHITE, rect.inflate(4, 4))
        else:
            color_fondo = DARK_GREEN
            color_texto = WHITE
        
        # Dibujar botón
        pygame.draw.rect(self.screen, color_fondo, rect)
        pygame.draw.rect(self.screen, WHITE, rect, 3)
        
        # Texto del botón
        texto_render = self.font_button.render(texto, True, color_texto)
        texto_rect = texto_render.get_rect(center=rect.center)
        self.screen.blit(texto_render, texto_rect)
    
    def dibujar_instrucciones(self):
        """Dibuja la pantalla de instrucciones"""
        # Overlay semi-transparente
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Panel de instrucciones
        panel_rect = pygame.Rect(100, 80, self.SCREEN_WIDTH-200, self.SCREEN_HEIGHT-160)
        pygame.draw.rect(self.screen, DARK_BLUE, panel_rect)
        pygame.draw.rect(self.screen, GOLD, panel_rect, 4)
        
        # Título de instrucciones
        titulo = self.font_subtitle.render("INSTRUCCIONES", True, GOLD)
        titulo_rect = titulo.get_rect(center=(self.SCREEN_WIDTH//2, 120))
        self.screen.blit(titulo, titulo_rect)
        
        # Lista de instrucciones
        instrucciones = [
            "🎮 CONTROLES:",
            "  ↑↓ - Cambiar de carril (6 carriles disponibles)",
            "  ESPACIO - Saltar obstáculos",
            "  ENTER - Iniciar juego rápido",
            "",
            "🌳 VISUALIZACIONES DEL ÁRBOL AVL:",
            "  V - Ver estructura del árbol en tiempo real",
            "  E - Mostrar estadísticas del árbol",
            "  T - Recorridos gráficos (Inorden/Preorden/Postorden)",
            "  I - Insertar obstáculos dinámicamente",
            "  C - Cerrar visualizaciones",
            "",
            "🎯 OBJETIVO:",
            "  Llegar al final evitando obstáculos",
            "  Los obstáculos se gestionan con un Árbol AVL",
            "  ¡Observa cómo se balancea automáticamente!",
            "",
            "💡 El carrito pierde energía al chocar",
            "🏁 Completa los 2000m para ganar",
            "",
            "Haz click o presiona ESC para volver"
        ]
        
        y_start = 160
        for i, linea in enumerate(instrucciones):
            if linea.startswith("🎮") or linea.startswith("🌳") or linea.startswith("🎯"):
                color = GOLD
                font = self.font_button
            elif linea.startswith("💡") or linea.startswith("🏁"):
                color = (255, 255, 0)  # YELLOW
                font = self.font_small
            else:
                color = WHITE
                font = self.font_small
            
            texto = font.render(linea, True, color)
            self.screen.blit(texto, (120, y_start + i * 22))
    
    def ejecutar(self):
        """Bucle principal del menú"""
        while True:
            self.tiempo += 1
            resultado = self.manejar_eventos()
            
            if resultado != 'menu':
                return resultado
            
            # Dibujar todo
            self.dibujar_fondo_animado()
            self.dibujar_titulo()
            
            if not self.mostrar_instrucciones:
                # Dibujar botones
                self.dibujar_boton('jugar', self.botones['jugar'], "JUGAR")
                self.dibujar_boton('instrucciones', self.botones['instrucciones'], "INSTRUCCIONES")
                self.dibujar_boton('salir', self.botones['salir'], "SALIR")
                
                # Texto informativo
                info = self.font_small.render("Usa el mouse o las teclas ENTER/I/ESC", True, SILVER)
                info_rect = info.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT - 30))
                self.screen.blit(info, info_rect)
            else:
                self.dibujar_instrucciones()
            
            pygame.display.flip()
            self.clock.tick(60)