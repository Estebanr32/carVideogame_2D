import pygame

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Tipos de obstáculos y sus efectos en energía
OBSTACULO_CONFIG = {
    'roca': {'color': BROWN, 'energia_perdida': 20},
    'cono': {'color': ORANGE, 'energia_perdida': 10},
    'hueco': {'color': BLACK, 'energia_perdida': 30},
    'aceite': {'color': PURPLE, 'energia_perdida': 15}
}

class Obstaculo:
    """Clase que representa un obstáculo"""
    def __init__(self, x, y, tipo, num_carriles=6, carretera_y=200, carretera_height=200):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.config = OBSTACULO_CONFIG[tipo]
        self.size = 30
        self.area_colision = 40
        self.num_carriles = num_carriles
        self.carretera_y = carretera_y
        self.carretera_height = carretera_height
    
    def get_screen_position(self, carrito_x):
        """Convierte coordenadas del mundo a pantalla"""
        screen_x = self.x - carrito_x + 50  # Restar posición del carrito
        
        # 6 carriles distribuidos uniformemente en la carretera
        carril_height = self.carretera_height // self.num_carriles
        screen_y = self.carretera_y + (self.y * carril_height) + (carril_height // 2)
        
        return screen_x, screen_y
    
    def esta_visible(self, carrito_x, screen_width):
        """Verifica si el obstáculo está visible en pantalla"""
        screen_x, _ = self.get_screen_position(carrito_x)
        return -50 <= screen_x <= screen_width + 50
    
    def colisiona_con_carrito(self, carrito):
        """Verifica colisión con el carrito"""
        if carrito.y != self.y:
            return False
        
        if carrito.saltando and carrito.altura_salto > 20:
            return False  # El carrito puede saltar sobre obstáculos
        
        # Verificar distancia en X
        distancia_x = abs(carrito.x - (self.x - carrito.distancia_recorrida))
        return distancia_x < self.area_colision
    
    def dibujar_roca(self, screen, x, y):
        """Dibuja una roca realista"""
        # Colores de la roca
        color_roca_base = BROWN
        color_roca_claro = (160, 90, 40)
        color_roca_oscuro = (100, 50, 10)
        
        # Cuerpo principal de la roca (forma irregular)
        pygame.draw.circle(screen, color_roca_base, (x, y), self.size//2)
        pygame.draw.circle(screen, color_roca_oscuro, (x-3, y-3), self.size//3)
        pygame.draw.circle(screen, color_roca_claro, (x+2, y+2), self.size//4)
        
        # Texturas y grietas
        pygame.draw.line(screen, color_roca_oscuro, (x-8, y-5), (x-2, y+3), 2)
        pygame.draw.line(screen, color_roca_oscuro, (x+1, y-6), (x+7, y-1), 1)
        
        # Borde para definir la forma
        pygame.draw.circle(screen, WHITE, (x, y), self.size//2, 2)
    
    def dibujar_cono(self, screen, x, y):
        """Dibuja un cono de tráfico"""
        # Colores del cono
        color_cono = ORANGE
        color_reflectivo = WHITE
        color_base = (50, 50, 50)
        
        # Base del cono
        base_width = self.size - 5
        pygame.draw.ellipse(screen, color_base, 
                           (x - base_width//2, y + 8, base_width, 8))
        
        # Cuerpo del cono (triángulo)
        puntos_cono = [
            (x, y - self.size//2 + 5),  # Punta
            (x - self.size//2 + 3, y + 8),  # Base izquierda
            (x + self.size//2 - 3, y + 8)   # Base derecha
        ]
        pygame.draw.polygon(screen, color_cono, puntos_cono)
        
        # Franjas reflectivas
        pygame.draw.line(screen, color_reflectivo, 
                        (x - 6, y - 2), (x + 6, y - 2), 2)
        pygame.draw.line(screen, color_reflectivo, 
                        (x - 8, y + 4), (x + 8, y + 4), 2)
        
        # Borde
        pygame.draw.polygon(screen, WHITE, puntos_cono, 2)
    
    def dibujar_hueco(self, screen, x, y):
        """Dibuja un hueco en la carretera"""
        # Colores del hueco
        color_hueco = BLACK
        color_borde = (80, 80, 80)
        color_interior = (30, 30, 30)
        
        # Hueco principal (elipse para profundidad)
        pygame.draw.ellipse(screen, color_hueco, 
                           (x - self.size//2, y - 8, self.size, 16))
        
        # Efecto de profundidad
        pygame.draw.ellipse(screen, color_interior, 
                           (x - self.size//2 + 3, y - 5, self.size - 6, 10))
        
        # Borde irregular para simular asfalto roto
        for i in range(0, 360, 30):
            import math
            offset_x = int(math.cos(math.radians(i)) * (self.size//2 - 2))
            offset_y = int(math.sin(math.radians(i)) * 6)
            pygame.draw.circle(screen, color_borde, 
                             (x + offset_x, y + offset_y), 2)
        
        # Borde principal
        pygame.draw.ellipse(screen, color_borde, 
                           (x - self.size//2, y - 8, self.size, 16), 2)
    
    def dibujar_aceite(self, screen, x, y):
        """Dibuja una mancha de aceite"""
        # Colores del aceite
        color_aceite = PURPLE
        color_aceite_claro = (160, 50, 160)
        color_aceite_oscuro = (80, 0, 80)
        color_brillo = (200, 100, 200)
        
        # Mancha principal (forma irregular)
        pygame.draw.ellipse(screen, color_aceite, 
                           (x - self.size//2, y - 8, self.size, 16))
        
        # Manchas adicionales para forma irregular
        pygame.draw.ellipse(screen, color_aceite_oscuro, 
                           (x - self.size//2 + 3, y - 5, self.size - 8, 12))
        pygame.draw.ellipse(screen, color_aceite_claro, 
                           (x - 5, y - 3, 10, 8))
        
        # Efectos de brillo (gotas)
        pygame.draw.circle(screen, color_brillo, (x - 3, y - 2), 2)
        pygame.draw.circle(screen, color_brillo, (x + 4, y + 1), 1)
        pygame.draw.circle(screen, color_brillo, (x - 1, y + 3), 1)
        
        # Borde sutil
        pygame.draw.ellipse(screen, (150, 150, 150), 
                           (x - self.size//2, y - 8, self.size, 16), 1)
    
    def draw(self, screen, carrito_x):
        """Dibuja el obstáculo en pantalla con diseño programático"""
        screen_x, screen_y = self.get_screen_position(carrito_x)
        
        # Dibujar cada tipo de obstáculo con su diseño específico
        if self.tipo == 'roca':
            self.dibujar_roca(screen, screen_x, screen_y)
        elif self.tipo == 'cono':
            self.dibujar_cono(screen, screen_x, screen_y)
        elif self.tipo == 'hueco':
            self.dibujar_hueco(screen, screen_x, screen_y)
        elif self.tipo == 'aceite':
            self.dibujar_aceite(screen, screen_x, screen_y)
        else:
            # Fallback: dibujar rectángulo simple
            pygame.draw.rect(screen, self.config['color'], 
                           (screen_x - self.size//2, screen_y - self.size//2, 
                            self.size, self.size))