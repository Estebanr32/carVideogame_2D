import pygame

# Colores para el carrito
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Mapeo de colores
COLOR_MAP = {
    'azul': BLUE,
    'rojo': RED,
    'verde': (0, 255, 0),
    'amarillo': (255, 255, 0),
    'blanco': WHITE
}

class Carrito:
    """Clase que representa el carrito del jugador"""
    def __init__(self, config, num_carriles=6):
        self.x = 50  # Posición fija en X (borde izquierdo)
        self.y = 2   # Carril Y (0-5, empezar en el centro)
        self.energia = 100
        self.color_original = COLOR_MAP.get(config['color_carrito'], BLUE)
        self.color_actual = self.color_original
        self.saltando = False
        self.altura_salto = 0
        self.salto_altura_max = config['salto_altura']
        self.size = 40
        self.num_carriles = num_carriles
        
        # Variables de movimiento automático
        self.distancia_recorrida = 0
        self.velocidad = config['velocidad']
        
        # Variables de salto
        self.salto_velocidad = 0
        self.en_salto = False
    
    def get_screen_position(self, carretera_y=200, carretera_height=200):
        """Convierte la posición lógica a coordenadas de pantalla"""
        screen_x = self.x
        
        # 6 carriles distribuidos uniformemente en la carretera
        # Carril 0: más arriba, Carril 5: más abajo
        carril_height = carretera_height // self.num_carriles
        screen_y = carretera_y + (self.y * carril_height) + (carril_height // 2)
        
        # Aplicar altura de salto
        if self.saltando:
            screen_y -= self.altura_salto
        
        return screen_x, screen_y
    
    def mover_arriba(self):
        """Mueve el carrito hacia arriba siguiendo la mecánica especificada"""
        if self.y > 0:
            self.y -= 1
    
    def mover_abajo(self):
        """Mueve el carrito hacia abajo siguiendo la mecánica especificada"""
        if self.y < (self.num_carriles - 1):  # 0-5, máximo carril 5
            self.y += 1
    
    def saltar(self):
        """Inicia el salto del carrito"""
        if not self.saltando:
            self.saltando = True
            self.salto_velocidad = 15  # Velocidad inicial del salto
            self.color_actual = RED  # Cambiar color durante el salto
    
    def actualizar_salto(self):
        """Actualiza la física del salto"""
        if self.saltando:
            self.altura_salto += self.salto_velocidad
            self.salto_velocidad -= 1  # Gravedad
            
            # Si toca el suelo, termina el salto
            if self.altura_salto <= 0:
                self.altura_salto = 0
                self.saltando = False
                self.salto_velocidad = 0
                self.color_actual = self.color_original
    
    def recibir_dano(self, dano):
        """Aplica daño al carrito"""
        self.energia = max(0, self.energia - dano)
    
    def esta_vivo(self):
        """Verifica si el carrito aún tiene energía"""
        return self.energia > 0
    
    def draw(self, screen):
        """Dibuja el carrito en pantalla"""
        x, y = self.get_screen_position()
        
        # Dibujar carrito como rectángulo
        pygame.draw.rect(screen, self.color_actual, 
                        (x - self.size//2, y - self.size//2, self.size, self.size))
        
        # Borde blanco
        pygame.draw.rect(screen, WHITE, 
                        (x - self.size//2, y - self.size//2, self.size, self.size), 2)