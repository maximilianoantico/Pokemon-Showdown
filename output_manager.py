# - librerias - #
import gamelib
import file_manager

# - constantes - #
PANTALLA_CARGA = 'imgs/pantalla_carga_720.gif'
PANTALLA_EQUIPOS = 'imgs/vista_equipos_720.gif'
ARENA = 'imgs/vista_arena_720.gif'
ENTRENADOR_1 = 'imgs/ash.gif'
ENTRENADOR_2 = 'imgs/misty.gif'
ENTRENADOR_1_BATALLA = 'imgs/trainer2.gif'
ENTRENADOR_2_BATALLA = 'imgs/trainer1.gif'
POKEBOLA_ON = 'imgs/pokeball.gif'
POKEBOLA_OFF = 'imgs/pokeball_gray.gif'
PANTALLA_ARENA = 0
IMG_POKEMON_X = 840
IMG_POKEMON_Y = 60
NOM_POKEMON_X = 0
NOM_POKEMON_X =0
TIPO_POKEMON_X = 0
TIPO_POKEMON_Y =0
SEPARACION = 96
ALTURA_BARRA = 18



def vista(vista_actual):
    if vista_actual == 'equipos':
        gamelib.draw_image(PANTALLA_EQUIPOS, 0, 0)
    elif vista_actual == 'loading':
        gamelib.draw_image(PANTALLA_CARGA, 0, 0)
    elif vista_actual == 'arena':
        gamelib.draw_image(ARENA, 0, 0)

def solicitar(mensaje):
    return gamelib.input(mensaje)

def imprimir_mensaje(mensaje):
    gamelib.say(mensaje)

def mostrar_entrenador(n):
    if n == 1:
        gamelib.draw_image(ENTRENADOR_1, IMG_POKEMON_X, IMG_POKEMON_Y)
    else:
        gamelib.draw_image(ENTRENADOR_2, IMG_POKEMON_X, IMG_POKEMON_Y)
    
def mostrar_equipo(nombre_equipo, pokemones_equipo):
    gamelib.draw_text(nombre_equipo,565, 64, font= 'Calibri', size = 40, bold=False, fill = 'black')
    gamelib.draw_text(nombre_equipo,568, 64, font= 'Calibri', size = 40, bold=False, fill = 'white')
    linea_a_imprimir = 0
        
    for pokemon, movimientos in pokemones_equipo.items():
        gamelib.draw_text(pokemon, 252, 134 + (linea_a_imprimir * SEPARACION), font= 'Calibri', size = 20, bold=True, fill = 'black')
        gamelib.draw_text(movimientos, 252, 177 + (linea_a_imprimir * SEPARACION), font= 'Calibri', size = 15, bold=True, fill = 'blue')
        linea_a_imprimir += 1
        
def no_hay_equipos_aun():
    gamelib.draw_text('NO HAY EQUIPOS AUN', 565, 64, font= 'Calibri', size = 20, bold=False, fill = 'black')
    gamelib.draw_text('NO HAY EQUIPOS AUN', 568, 64, font= 'Calibri', size = 20, bold=False, fill = 'white')
    
def mostrar_entrenadores(entrenador_1, entrenador_2):
    # Nombre - Entrenador 1
    gamelib.draw_text(entrenador_1.nombre_entrenador, 310, 442)  
    # Imagen - Entrenador 1 
    gamelib.draw_image(ENTRENADOR_1_BATALLA, 255, 458)
    # Pokebolas - Entrenador 1
    for n_pokemon, pokemon in enumerate(entrenador_1.pokemones.values()):
        gamelib.draw_image(POKEBOLA_ON if pokemon.hp > 0 else POKEBOLA_OFF, 235, 458 - 20 * n_pokemon)
        
    # Nombre - Entrenador 2
    gamelib.draw_text(entrenador_2.nombre_entrenador, 971, 442)  
    # Imagen - Entrenador 2 
    gamelib.draw_image(ENTRENADOR_2_BATALLA, 910, 458)
    # Pokebolas - Entrenador 2
    for n_pokemon, pokemon in enumerate(entrenador_2.pokemones.values()):
        gamelib.draw_image(POKEBOLA_ON if pokemon.hp > 0 else POKEBOLA_OFF, 1020, 458 - 20 * n_pokemon)
    
def mostrar_pokemones(pokemon1, pokemon2):
    # Nombre - Pokemon 1
    gamelib.draw_text(pokemon1.nombre, 465, 387, bold = True, size = 15)
    # Imagen - Pokemon 1
    gamelib.draw_image(pokemon1.imagen, 365, 435)
    # Vida - Pokemon 1
    gamelib.draw_rectangle(365, 405, 565, 420, fill = 'white', outline = 'black')
    gamelib.draw_rectangle(365, 405, 365 + 200 * (pokemon1.hp / pokemon1.hp_max), 420, fill = 'green')

    # Nombre - Pokemon 2
    gamelib.draw_text(pokemon2.nombre, 810, 387, bold = True, size = 15)
    # Imagen - Pokemon 2
    gamelib.draw_image(pokemon2.imagen, 710, 435)
    # Vida - Pokemon 2
    gamelib.draw_rectangle(710, 405, 910, 420, fill = 'white', outline = 'black')
    gamelib.draw_rectangle(710, 405, 710 + 200 * (pokemon2.hp / pokemon2.hp_max), 420, fill = 'green')