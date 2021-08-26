import output_manager
import random

def seleccionar_pokemon_activo(entrenador):
    """
    Le solicita al usuario que seleccione entre todos los pokemones que posee el entrenador uno, hasta que el usuario ingrese uno correcto, para establecerlo como pokemon_activo

    Args:
        entrenador (Entrenador): Objeto de la clase entrenador al cual se le seleccionara su pokemon_activo en base a los pokemones que tenga.
    """
    while True:
        pokemon_ingresado = output_manager.solicitar(f'Seleccione el pokemon activo para el equipo {entrenador.nombre_entrenador}, los pokemons disponibles son: {entrenador.obtener_nombre_pokemones()}')
        pokemon_seleccionado = entrenador.pokemones.get(pokemon_ingresado, None)
        
        if pokemon_seleccionado is None:
            output_manager.imprimir_mensaje('El pokemon seleccionado no ha sido encontrado, seleccione otro pokemon.')
        elif pokemon_seleccionado.hp <= 0:
            output_manager.imprimir_mensaje(f'{pokemon_seleccionado.nombre} se encuentra inconsciente, seleccione otro pokemon.')
        else:
            entrenador.pokemon_activo = pokemon_seleccionado
            break
        
def seleccionar_movimiento(entrenador):
    """Le solicita al usuario que seleccione entre todos los movimientos que posea el pokemon activo, hasta que el usuario ingrese uno correcto

    Args:
        entrenador (Entrenador): Objeto de la clase entrenador al cual se le indicara el movimiento a realizar para su pokemon activo
    """
    while True:
        movimiento_ingresado = output_manager.solicitar(f'Seleccione el movimiento que va a realizar el equipo {entrenador.nombre_entrenador}, con el pokemon {entrenador.pokemon_activo.nombre}, los movimientos disponibles son: {entrenador.pokemon_activo.obtener_movimientos()}')
        movimiento_seleccionado = entrenador.pokemon_activo.movimientos.get(movimiento_ingresado, None)
        
        if movimiento_seleccionado is None:
            output_manager.imprimir_mensaje('El movimiento seleccionado no ha sido encontrado, seleccione otro movimiento.')
        else:
            entrenador.pokemon_activo.movimiento_a_realizar = movimiento_seleccionado
            break
        
def definir_ejecuciones(entrenador_1, entrenador_2):
    """Define en base a las velocidades de los pokemones activos de cada entrenador, quien ataca primero y devuelve los entrenadores en dicho orden.

    Args:
        entrenador_1 (Entrenador): Objeto de la clase Entrenador con un pokemon en el atributo pokemon_activo
        entrenador_2 (Entrenador): Objeto de la clase Entrenador con un pokemon en el atributo pokemon_activo

    Returns:
        prioridad_1 (Entrenador): Objeto de la clase entrenador cuyo pokemon activo comenzara atacando
        prioridad_2 (Entrenador): Objeto de la clase entrenador cuyo pokemon activo sera el segundo en atacar
    """
    if entrenador_1.pokemon_activo.spd != entrenador_2.pokemon_activo.spd:
        prioridad_1 = entrenador_1 if entrenador_1.pokemon_activo.spd >= entrenador_2.pokemon_activo.spd else entrenador_2
        prioridad_2 = entrenador_2 if prioridad_1 == entrenador_1 else entrenador_1
    else:
        prioridad_1 = random.choice([entrenador_1, entrenador_2])
        prioridad_2 = entrenador_2 if prioridad_1 == entrenador_1 else entrenador_1
    
    return prioridad_1, prioridad_2

def realizar_movimiento(atacante, defensor, gestor_archivos):
    """Realiza el movimiento del pokemon atancante y si el segundo permanece vivo, tambien el del segundo.

    Args:
        atacante (Pokemon): Pokemon que comenzara atacando
        defensor (Pokemon): Pokemon que sera el segundo en atacar
    """
    
    movimiento = atacante.movimiento_a_realizar
    # Movimiento de ataque normal
    if movimiento.categoria == 'Physical':
        d_base = 15 * movimiento.poder * (atacante.atk / defensor.defe) / 50
        
        stab = True if atacante.tipo == movimiento.tipo else False
        rand = random.randrange(8, 11) / 10
        mod_defensor = 1
        
        print(f'DEBUG: atacante tipo = {atacante.tipo}')
        print(f'DEBUG: defensor tipo = {defensor.tipo}')
        
        for tipo_atk in atacante.tipo.split(','):
            for tipo_def in defensor.tipo.split(','):
                mod_defensor *= float(gestor_archivos.diccionario_tabla_tipos[tipo_atk][tipo_def])
        
        d_total = int(d_base * rand * mod_defensor * (1.5 if stab else 1))
        
        defensor.hp -= d_total
        
        print(f'DEBUG: movimiento_poder = {movimiento.poder}')
        print(f'DEBUG: atk = {atacante.atk}')
        print(f'DEBUG: defe = {defensor.defe}')
        print(f'DEBUG: d_base = {d_base}')
        print(f'DEBUG: rand = {rand}')
        print(f'DEBUG: stab = {stab}')
        print(f'DEBUG: d_total = {d_total}')
        
        output_manager.imprimir_mensaje(f'{atacante.nombre} ha atacado a {defensor.nombre}, quitandole {d_total} de HP. {defensor.nombre} ha quedado con {defensor.hp} de HP.')
        
    # Movimiento de ataque especial
    elif movimiento.categoria == 'Special':
        d_base = 15 * movimiento.poder * (atacante.spa / defensor.spd) / 50
        
        stab = True if atacante.tipo == movimiento.tipo else False
        rand = random.randrange(8, 11) / 10
        mod_defensor = 1
        
        print(f'DEBUG: atacante tipo = {atacante.tipo}')
        print(f'DEBUG: defensor tipo = {defensor.tipo}')
        
        for tipo_atk in atacante.tipo.split(','):
            for tipo_def in defensor.tipo.split(','):
                mod_defensor *= float(gestor_archivos.diccionario_tabla_tipos[tipo_atk][tipo_def])
        
        d_total = int(d_base * rand * mod_defensor * (1.5 if stab else 1))
        
        defensor.hp -= d_total
        
        print(f'DEBUG: movimiento_poder = {movimiento.poder}')
        print(f'DEBUG: spa = {atacante.spa}')
        print(f'DEBUG: spd = {defensor.spd}')
        print(f'DEBUG: d_base = {d_base}')
        print(f'DEBUG: rand = {rand}')
        print(f'DEBUG: stab = {stab}')
        print(f'DEBUG: d_total = {d_total}')
        
        output_manager.imprimir_mensaje(f'{atacante.nombre} ha atacado a {defensor.nombre}, quitandole {d_total} de HP. {defensor.nombre} ha quedado con {defensor.hp} de HP.')
    
    # Movimiento de sanacion 
    elif movimiento.categoria == 'Status' and movimiento.objetivo == 'self' and movimiento.stats == '':
        atacante.hp += atacante.hp_max // 2 
        
    # Movimeinto de empoderamiento a si mismo
    elif movimiento.categoria == 'Status' and movimiento.objetivo == 'self' and movimiento.stats != '':
        for stat in movimiento.stats.split(','):
            output_manager.imprimir_mensaje(f'Duplicando el {stat} de {atacante.nombre}')
            
            if stat == 'atk': 
                atacante.atk *= 2
            elif stat == 'def': 
                atacante.defe *= 2
            elif stat == 'spe': 
                atacante.spe *= 2
    
    # Movimeinto de empoderamiento al oponente
    elif movimiento.categoria == 'Status' and movimiento.objetivo == 'normal' and movimiento.stats != '':
        for stat in movimiento.stats.split(','):
            output_manager.imprimir_mensaje(f'Reduciendo a la mitad el {stat} de {defensor.nombre}')
            
            if stat == 'atk':
                defensor.atk *= 0.5
            elif stat == 'def':
                defensor.defe *= 0.5
            elif stat == 'spe':
                defensor.spe *= 0.5
        
def ejecutar_turno(entrenador_1, entrenador_2, gestor_archivos):
    prioridad_1, prioridad_2 = definir_ejecuciones(entrenador_1, entrenador_2)
    
    realizar_movimiento(prioridad_1.pokemon_activo, prioridad_2.pokemon_activo, gestor_archivos)
    if prioridad_2.pokemon_activo.hp > 0: 
        realizar_movimiento(prioridad_2.pokemon_activo, prioridad_1.pokemon_activo, gestor_archivos)
    else:
        output_manager.imprimir_mensaje(f'{prioridad_2.pokemon_activo.nombre} no ha podido atacar por que se encontraba inconsciente.')
    
    
    
    
    