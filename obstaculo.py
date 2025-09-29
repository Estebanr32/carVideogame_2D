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