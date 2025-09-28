"""
🚗 Carrito AVL - Juego de Obstáculos Dinámicos con Árbol AVL 🌳

Archivo principal que coordina todos los módulos del juego.
Arquitectura modular para mejor mantenimiento y organización del código.
"""

import pygame
import sys
from menu import MenuPrincipal
from juego import JuegoCarrito

# Constantes globales
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Inicializar pygame
pygame.init()

def main():
    """
    Función principal que maneja el ciclo completo del programa:
    Menú Principal → Juego → Menú Principal (loop continuo)
    """
    # Crear pantalla principal
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🚗 Carrito AVL - Obstáculos Dinámicos 🌳")
    
    print("🎮 Iniciando Carrito AVL...")
    print("📁 Arquitectura modular cargada:")
    print("   - menu.py: Interfaz de menú principal")
    print("   - juego.py: Lógica principal del juego")
    print("   - carrito.py: Clase del carrito jugador")
    print("   - obstaculo.py: Clase de obstáculos")
    print("   - avl_tree.py: Implementación del Árbol AVL")
    print("   - visualizador_pygame.py: Visualizaciones integradas")
    
    # Bucle principal del programa
    while True:
        # Mostrar menú principal
        menu = MenuPrincipal(screen)
        resultado = menu.ejecutar()
        
        if resultado == 'salir':
            print("👋 ¡Gracias por jugar Carrito AVL!")
            break
        elif resultado == 'jugar':
            # Iniciar juego
            print("🎯 Iniciando juego...")
            juego = JuegoCarrito()
            juego.run()
            print("🔙 Regresando al menú principal...")
            # Después del juego, volver al menú automáticamente
    
    # Limpiar recursos
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()