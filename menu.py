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
        titulo = self.font_subtitle.render("INSTRUCTIONS", True, GOLD)
        titulo_rect = titulo.get_rect(center=(self.SCREEN_WIDTH//2, 120))
        self.screen.blit(titulo, titulo_rect)
        
        # Lista de instrucciones
        instrucciones = [
            "🎮 CONTROLS:",
            "  ↑↓ - Change lanes (6 lanes available)",
            "  SPACE - Jump over obstacles",
            "  ENTER - Start game quickly",
            "",
            "🌳 AVL TREE VISUALIZATIONS:",
            "  V - View tree structure in real time",
            "  E - Show tree statistics",
            "  T - Graphical traversals (Inorder/Preorder/Postorder)",
            "  I - Insert obstacles dynamically",
            "  C - Close visualizations",
            "",
            "🎯 OBJECTIVE:",
            "  Reach the end avoiding obstacles",
            "  Obstacles are managed with an AVL Tree",
            "  Watch how it balances automatically!",
            "",
            "💡 The car loses energy when crashing",
            "🏁 Complete 2000m to win",
            "",
            "Click or press ESC to return"
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
                self.dibujar_boton('jugar', self.botones['jugar'], "PLAY")
                self.dibujar_boton('instrucciones', self.botones['instrucciones'], "INSTRUCTIONS")
                self.dibujar_boton('salir', self.botones['salir'], "EXIT")
                
                # Texto informativo
                info = self.font_small.render("Use mouse or ENTER/I/ESC keys", True, SILVER)
                info_rect = info.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT - 30))
                self.screen.blit(info, info_rect)
            else:
                self.dibujar_instrucciones()
            
            pygame.display.flip()
            self.clock.tick(60)