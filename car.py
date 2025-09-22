"""
Módulo del carrito del juego
Maneja el comportamiento, movimiento y renderizado del carrito
"""
import pygame

class Car:
    def __init__(self, config):
        """Inicializa el carrito con la configuración dada"""
        self.config = config
        
        # Posición del carrito
        self.x = config.car_x_position  # Posición fija en pantalla
        self.y = config.get_lane_y_position(1)  # Empieza en el carril medio
        self.world_x = 0  # Posición real en el mundo del juego
        
        # Dimensiones
        self.width = config.car_width
        self.height = config.car_height
        
        # Estado del carrito
        self.current_lane = 1  # 0=arriba, 1=medio, 2=abajo
        self.energy = 100
        self.is_jumping = False
        self.jump_velocity = 0
        self.ground_y = self.y
        
        # Colores
        self.normal_color = config.car_initial_color
        self.jump_color = config.car_jump_color
        self.current_color = self.normal_color
        
        # Movimiento vertical
        self.target_y = self.y
        self.moving_up = False
        self.moving_down = False
    
    def update(self, dt):
        """Actualiza el estado del carrito"""
        # Actualizar posición en el mundo
        self.world_x += self.config.car_speed
        
        # Manejar salto
        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity += self.config.gravity
            
            # Verificar si ha aterrizado
            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False
                self.jump_velocity = 0
                self.current_color = self.normal_color
    
    def move_up(self):
        """Mueve el carrito al carril superior (instantáneo)"""
        if self.current_lane == 1 and not self.is_jumping:  # Si está en carril inferior
            self.current_lane = 0
            self.y = self.config.get_lane_y_position(self.current_lane)
            self.ground_y = self.y
    
    def move_down(self):
        """Mueve el carrito al carril inferior (instantáneo)"""
        if self.current_lane == 0 and not self.is_jumping:  # Si está en carril superior
            self.current_lane = 1
            self.y = self.config.get_lane_y_position(self.current_lane)
            self.ground_y = self.y
    
    def jump(self):
        """Hace saltar al carrito"""
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = -self.config.jump_height // 5  # Velocidad inicial hacia arriba
            self.current_color = self.jump_color
    
    def get_rect(self):
        """Retorna el rectángulo de colisión del carrito"""
        return pygame.Rect(self.x - self.width // 2, 
                          self.y - self.height // 2, 
                          self.width, 
                          self.height)
    
    def draw(self, screen):
        """Dibuja el carrito en la pantalla"""
        # Dibujar el cuerpo principal del carrito
        car_rect = self.get_rect()
        pygame.draw.rect(screen, self.current_color, car_rect)
        pygame.draw.rect(screen, (0, 0, 0), car_rect, 2)
        
        # Dibujar detalles del carrito
        # Ventanas
        window_width = self.width // 3
        window_height = self.height // 3
        window_x = car_rect.x + window_width
        window_y = car_rect.y + window_height // 2
        
        pygame.draw.rect(screen, (200, 220, 255), 
                        (window_x, window_y, window_width, window_height))
        
        # Ruedas
        wheel_radius = 6
        wheel_y = car_rect.bottom - wheel_radius
        
        # Rueda delantera
        pygame.draw.circle(screen, (50, 50, 50), 
                         (car_rect.right - wheel_radius - 5, wheel_y), wheel_radius)
        
        # Rueda trasera
        pygame.draw.circle(screen, (50, 50, 50), 
                         (car_rect.left + wheel_radius + 5, wheel_y), wheel_radius)
    
    def get_progress_percentage(self):
        """Retorna el porcentaje de progreso en la carretera"""
        return min(100, (self.world_x / self.config.total_distance) * 100)
    
    def has_reached_goal(self):
        """Verifica si el carrito ha alcanzado la meta"""
        return self.world_x >= self.config.total_distance
    
    def is_alive(self):
        """Verifica si el carrito aún tiene energía"""
        return self.energy > 0