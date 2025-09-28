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
    
    def dibujar_carrito_programatico(self, screen, x, y):
        """Dibuja un carrito detallado programáticamente"""
        # Colores
        color_cuerpo = self.color_actual
        color_rueda = (50, 50, 50)
        color_llanta = (30, 30, 30)
        color_parabrisas = (100, 150, 255)
        color_faro = (255, 255, 150)
        color_detalle = (200, 200, 200)
        
        # Dimensiones
        ancho = self.size
        alto = int(self.size * 0.7)
        half_w = ancho // 2
        half_h = alto // 2
        
        # 1. Cuerpo principal del auto
        cuerpo_rect = (x - half_w + 3, y - half_h + 5, ancho - 6, alto - 10)
        pygame.draw.rect(screen, color_cuerpo, cuerpo_rect)
        pygame.draw.rect(screen, WHITE, cuerpo_rect, 2)
        
        # 2. Capó (parte delantera)
        capo_rect = (x + half_w - 8, y - half_h + 7, 6, alto - 14)
        pygame.draw.rect(screen, color_cuerpo, capo_rect)
        pygame.draw.rect(screen, WHITE, capo_rect, 1)
        
        # 3. Parabrisas
        parabrisas_rect = (x - half_w + 8, y - half_h + 8, ancho - 20, 8)
        pygame.draw.rect(screen, color_parabrisas, parabrisas_rect)
        
        # 4. Ruedas
        # Rueda trasera
        rueda_trasera_pos = (x - half_w + 8, y + half_h - 3)
        pygame.draw.circle(screen, color_rueda, rueda_trasera_pos, 6)
        pygame.draw.circle(screen, color_llanta, rueda_trasera_pos, 4)
        
        # Rueda delantera
        rueda_delantera_pos = (x + half_w - 8, y + half_h - 3)
        pygame.draw.circle(screen, color_rueda, rueda_delantera_pos, 6)
        pygame.draw.circle(screen, color_llanta, rueda_delantera_pos, 4)
        
        # 5. Faros delanteros
        faro1_pos = (x + half_w - 2, y - 3)
        faro2_pos = (x + half_w - 2, y + 3)
        pygame.draw.circle(screen, color_faro, faro1_pos, 2)
        pygame.draw.circle(screen, color_faro, faro2_pos, 2)
        
        # 6. Detalles adicionales
        # Línea central
        pygame.draw.line(screen, color_detalle, 
                        (x - half_w + 5, y), (x + half_w - 5, y), 1)
        
        # Ventanas laterales
        ventana_izq = (x - half_w + 5, y - half_h + 10, 4, alto - 22)
        ventana_der = (x + half_w - 9, y - half_h + 10, 4, alto - 22)
        pygame.draw.rect(screen, color_parabrisas, ventana_izq)
        pygame.draw.rect(screen, color_parabrisas, ventana_der)
        
        # 7. Efectos especiales cuando salta
        if self.saltando:
            # Estela de salto
            for i in range(3):
                pygame.draw.rect(screen, (255, 255, 0, 100), 
                               (x - half_w + 3 - i*2, y - half_h + 5 + i, 
                                ancho - 6, alto - 10), 1)
    
    def draw(self, screen):
        """Dibuja el carrito en pantalla"""
        x, y = self.get_screen_position()
        
        # Dibujar carrito programáticamente (¡mucho mejor que un cuadrado!)
        self.dibujar_carrito_programatico(screen, x, y)