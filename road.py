"""
Módulo de la carretera del juego
Maneja el renderizado y comportamiento de la carretera
"""
import pygame

class Road:
    def __init__(self, config):
        """Inicializa la carretera con la configuración dada"""
        self.config = config
        self.camera_x = 0  # Posición de la cámara en el mundo
        
        # Colores
        self.road_color = (80, 80, 80)
        self.lane_line_color = (255, 255, 255)
        self.grass_color = (34, 139, 34)
        self.sky_color = (135, 206, 235)
        self.finish_line_color = (255, 0, 0)
        
        # Configuración de líneas divisorias
        self.line_width = 3
        self.dash_length = 30
        self.dash_gap = 20
        self.dash_offset = 0
    
    def update(self, car_world_x, dt):
        """Actualiza la posición de la cámara para seguir al carrito"""
        # La cámara sigue al carrito manteniendo una posición fija en pantalla
        self.camera_x = car_world_x
        
        # Actualizar animación de líneas divisorias
        self.dash_offset += self.config.car_speed
        if self.dash_offset >= self.dash_length + self.dash_gap:
            self.dash_offset = 0
    
    def world_to_screen_x(self, world_x):
        """Convierte coordenada mundial X a coordenada de pantalla"""
        return world_x - self.camera_x + self.config.car_x_position
    
    def screen_to_world_x(self, screen_x):
        """Convierte coordenada de pantalla X a coordenada mundial"""
        return screen_x + self.camera_x - self.config.car_x_position
    
    def draw(self, screen, car):
        """Dibuja la carretera y elementos del entorno"""
        # Dibujar cielo
        sky_height = self.config.window_height - self.config.road_height
        pygame.draw.rect(screen, self.sky_color, 
                        (0, 0, self.config.window_width, sky_height))
        
        # Dibujar césped
        grass_y = self.config.window_height - self.config.road_height
        pygame.draw.rect(screen, self.grass_color,
                        (0, grass_y, self.config.window_width, self.config.road_height))
        
        # Dibujar carretera
        road_y = grass_y + 20  # Dejar un poco de césped arriba
        road_height = self.config.road_height - 40  # Dejar césped arriba y abajo
        
        pygame.draw.rect(screen, self.road_color,
                        (0, road_y, self.config.window_width, road_height))
        
        # Dibujar líneas divisorias de carriles
        self.draw_lane_lines(screen, road_y, road_height)
        
        # Dibujar indicadores de progreso
        self.draw_progress_indicators(screen, car)
        
        # Dibujar línea de meta si está cerca
        self.draw_finish_line(screen, car)
    
    def draw_lane_lines(self, screen, road_y, road_height):
        """Dibuja las líneas divisorias de los carriles"""
        # Para 2 carriles, solo necesitamos 1 línea divisoria en el medio
        # Línea divisoria central entre los 2 carriles
        middle_y = road_y + (road_height // 2)
        
        # Dibujar línea discontinua central
        dash_x = -self.dash_offset
        while dash_x < self.config.window_width:
            if dash_x + self.dash_length > 0:
                start_x = max(0, dash_x)
                end_x = min(self.config.window_width, dash_x + self.dash_length)
                
                pygame.draw.line(screen, self.lane_line_color,
                               (start_x, middle_y), (end_x, middle_y), self.line_width)
            
            dash_x += self.dash_length + self.dash_gap
        
        # Líneas de borde de la carretera (superior e inferior)
        pygame.draw.line(screen, self.lane_line_color,
                        (0, road_y), (self.config.window_width, road_y), self.line_width)
        pygame.draw.line(screen, self.lane_line_color,
                        (0, road_y + road_height), (self.config.window_width, road_y + road_height), self.line_width)
    
    def draw_progress_indicators(self, screen, car):
        """Dibuja indicadores de progreso del juego"""
        font = pygame.font.Font(None, 36)
        
        # Distancia recorrida
        distance_text = f"Distancia: {int(car.world_x)}m / {self.config.total_distance}m"
        distance_surface = font.render(distance_text, True, (255, 255, 255))
        screen.blit(distance_surface, (10, 10))
        
        # Porcentaje de progreso
        progress = car.get_progress_percentage()
        progress_text = f"Progreso: {progress:.1f}%"
        progress_surface = font.render(progress_text, True, (255, 255, 255))
        screen.blit(progress_surface, (10, 50))
        
        # Energía
        energy_text = f"Energía: {car.energy}%"
        energy_color = (0, 255, 0) if car.energy > 50 else (255, 255, 0) if car.energy > 25 else (255, 0, 0)
        energy_surface = font.render(energy_text, True, energy_color)
        screen.blit(energy_surface, (10, 90))
        
        # Carril actual
        lane_names = ["Superior", "Inferior"]
        lane_text = f"Carril: {lane_names[car.current_lane]}"
        lane_surface = font.render(lane_text, True, (255, 255, 255))
        screen.blit(lane_surface, (10, 130))
        
        # Barra de progreso visual
        progress_bar_width = 300
        progress_bar_height = 20
        progress_bar_x = self.config.window_width - progress_bar_width - 20
        progress_bar_y = 20
        
        # Fondo de la barra
        pygame.draw.rect(screen, (100, 100, 100),
                        (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
        
        # Progreso actual
        progress_width = int((progress / 100) * progress_bar_width)
        pygame.draw.rect(screen, (0, 255, 0),
                        (progress_bar_x, progress_bar_y, progress_width, progress_bar_height))
        
        # Borde
        pygame.draw.rect(screen, (255, 255, 255),
                        (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
    
    def draw_finish_line(self, screen, car):
        """Dibuja la línea de meta cuando está cerca"""
        finish_world_x = self.config.total_distance
        finish_screen_x = self.world_to_screen_x(finish_world_x)
        
        # Solo dibujar si la línea de meta está visible en pantalla
        if -50 <= finish_screen_x <= self.config.window_width + 50:
            road_y = self.config.window_height - self.config.road_height + 20
            road_height = self.config.road_height - 40
            
            # Dibujar patrón de tablero de ajedrez para la meta
            square_size = 20
            for y in range(int(road_y), int(road_y + road_height), square_size):
                for row in range(square_size):
                    if ((y - int(road_y)) // square_size) % 2 == 0:
                        color = self.finish_line_color if row % 2 == 0 else (255, 255, 255)
                    else:
                        color = (255, 255, 255) if row % 2 == 0 else self.finish_line_color
                    
                    if y + row < road_y + road_height:
                        pygame.draw.line(screen, color,
                                       (finish_screen_x - 5, y + row),
                                       (finish_screen_x + 5, y + row), 2)
    
    def is_position_visible(self, world_x):
        """Verifica si una posición mundial está visible en pantalla"""
        screen_x = self.world_to_screen_x(world_x)
        return -100 <= screen_x <= self.config.window_width + 100