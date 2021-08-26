# - librerias - #
import gamelib
import csv
from time import sleep
import random

# - modulos - #
import output_manager
import file_manager
import input_manager
import fight_manager

# - constantes - #
ANCHO_VENTANA = 1280
ALTO_VENTANA = 720
TIEMPO_CARGA = 3
TITULO_VENTANA = 'Pokedex'

def main():
    gamelib.title(TITULO_VENTANA)
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    gamelib.play_sound('arena.wav')
    
    equipos = [] # Contiene a los objetos de la clase 'Equipo' que fueron creados en base a 'equipo.csv'
    
    gestor_archivos = file_manager.FileManager()
    gestor_archivos.cargar_pokemones()
    gestor_archivos.cargar_detalle_movimientos()
    gestor_archivos.cargar_tabla_tipos()
    gestor_archivos.cargar_equipos_desde_archivo(equipos)
    
    state = {
        'vista_actual' : 'loading',
        'equipo_actual' : 0,
        'cantidad_equipos' : len(equipos),
        'elegir_equipos' : False,
        'generar_entrenadores' : False,
        'equipos_seleccionados' : [],       # Contiene a los objetos de la clase 'Equipo' que fueron seleccionados (max = 2)
        'entrenador_1' : None,
        'entrenador_2' : None,              # Contiene a los objetos de la clase 'Entrenadores' que contienen a los objetos de la clase 'Pokemons' que se utilizaran para pelear
    }

    
    
    while gamelib.is_alive():
    
        gamelib.draw_begin()

        # Imprime la vista actual 
        output_manager.vista(state['vista_actual'])

        if state['vista_actual'] == 'loading':
            sleep(TIEMPO_CARGA)
            state['vista_actual'] = 'equipos'
        
        # Muestra el equipo actual si la vista actual es equipos
        if state['vista_actual'] == 'equipos':
            if len(state['equipos_seleccionados']) == 0:
                output_manager.mostrar_entrenador(1)
            else:
                output_manager.mostrar_entrenador(2)

            if len(equipos) == 0:
                output_manager.no_hay_equipos_aun()
            else:
                output_manager.mostrar_equipo(equipos[state['equipo_actual']].nombre_equipo ,equipos[state['equipo_actual']].obtener_pokemones())
              
        # Ejecuta la pelea si la vista actual es arena
        if state['vista_actual'] == 'arena':    
            entrenador_1 = state['entrenador_1']
            entrenador_2 = state['entrenador_2']
            
            # Determina el ganador si alguno de los equipos se ha quedado sin pokemones
            if not entrenador_1.hay_pokemones_vivos():
                output_manager.imprimir_mensaje(f"Felicitaciones el ganador de la pelea es el equipo {entrenador_2.nombre_entrenador}.")
                state['vista_actual'] = 'equipos'
                state['equipos_seleccionados'] = []
                state['entrenador_1'] = None
                state['entrenador_2'] = None
                continue
            elif not entrenador_2.hay_pokemones_vivos():
                output_manager.imprimir_mensaje(f"Felicitaciones, el ganador de la pelea es el equipo {entrenador_1.nombre_entrenador}.")
                state['vista_actual'] = 'equipos'
                state['equipos_seleccionados'] = []
                state['entrenador_1'] = None
                state['entrenador_2'] = None
                continue
            
            if entrenador_1.pokemon_activo is None or entrenador_1.pokemon_activo.hp <= 0:
                fight_manager.seleccionar_pokemon_activo(entrenador_1)
            
            # Hace que en el caso de no tenerlo, el entrenador 2 seleccione un pokemon activo 
            if entrenador_2.pokemon_activo is None or entrenador_2.pokemon_activo.hp <= 0:
                fight_manager.seleccionar_pokemon_activo(entrenador_2)
                
            output_manager.mostrar_pokemones(entrenador_1.pokemon_activo, entrenador_2.pokemon_activo)
            output_manager.mostrar_entrenadores(entrenador_1, entrenador_2)
            
            # Hace que el pokemon seleccionado del entrenador 1, indique el movimiento a realizar en este turno
            fight_manager.seleccionar_movimiento(entrenador_1)
                
            # Hace que el pokemon seleccionado del entrenador 1, indique el movimiento a realizar en este turno
            fight_manager.seleccionar_movimiento(entrenador_2)
                
            fight_manager.ejecutar_turno(entrenador_1, entrenador_2, gestor_archivos)
            
            output_manager.mostrar_pokemones(entrenador_1.pokemon_activo, entrenador_2.pokemon_activo)
            output_manager.mostrar_entrenadores(entrenador_1, entrenador_2)

        
        # Permite al usuario seleccionar un equipo. Una vez que se alcanzan los 2 equipos seleccionados se pasa a generar_entrenadores
        if state['elegir_equipos'] == True:
            if len(state['equipos_seleccionados']) < 2:
                equipo_ingresado = output_manager.solicitar(f"Ingrese el nombre del {'primer' if len(state['equipos_seleccionados']) == 0 else 'segundo'} equipo que desea utilizar, los equipos disponibles son: \n {[equipo.nombre_equipo for equipo in equipos]}")
                for equipo in equipos:
                    if equipo.nombre_equipo == equipo_ingresado:
                        state['equipos_seleccionados'].append(equipo)
                        output_manager.imprimir_mensaje(f'Agregaste al equipo {equipo_ingresado}')
                        break
                else:
                    output_manager.imprimir_mensaje(f'No se ha encontrado al equipo {equipo_ingresado}')
            
            if len(state['equipos_seleccionados']) == 2:
                state['generar_entrenadores'] = True
            
            state['elegir_equipos'] = False
        
        # Crea un entrenador con sus respectivos pokemones por cada uno de los equipos seleccionados
        if state['generar_entrenadores'] == True:
            for equipo in state['equipos_seleccionados']:
                entrenador = file_manager.Entrenador(equipo.nombre_equipo)
                
                for nombre_pokemon, movimientos in equipo.obtener_pokemones().items():
                    informacion_pokemon = gestor_archivos.obtener_pokemon_nombre(nombre_pokemon)
                    
                    pokemon = file_manager.Pokemon(informacion_pokemon['nombre'],
                                                    informacion_pokemon['tipos'],
                                                    informacion_pokemon['imagen'],
                                                    informacion_pokemon['hp'],
                                                    informacion_pokemon['atk'],
                                                    informacion_pokemon['def'],
                                                    informacion_pokemon['spa'],
                                                    informacion_pokemon['spd'],
                                                    informacion_pokemon['spe'],
                                                    )

                    for nombre_movimiento in movimientos.split(','):
                        informacion_movimiento = gestor_archivos.obtener_detalle_movimiento(nombre_movimiento)
                        
                        movimiento = file_manager.Movimiento(nombre_movimiento,
                                                                informacion_movimiento['categoria'],
                                                                informacion_movimiento['objetivo'],
                                                                informacion_movimiento['pp'],
                                                                informacion_movimiento['poder'],
                                                                informacion_movimiento['tipo'],
                                                                informacion_movimiento['stats'],)
                        
                        pokemon.agregar_movimiento(movimiento)
                    
                    entrenador.agregar_pokemon(pokemon) 
                
                if not state['entrenador_1']:
                    state['entrenador_1'] = entrenador
                else:
                    state['entrenador_2'] = entrenador
                    
            state['vista_actual'] = 'arena'
            state['generar_entrenadores'] = False
            
        gamelib.draw_end()
        
        

        input_manager.process_inputs(gamelib.get_events(), state)

gamelib.init(main) 
print("cerro el juego")
