import gamelib

CONTROLES = {
    'equipos' : {'proximo_equipo' : 'Up',
                 'anterior_equipo' : 'Down', 
                 'elegir_equipos' : 'Return',
                },
    
    'arena' :   {},
}

def process_inputs(events, state):
    for event in events:
        if event.type == gamelib.EventType.KeyPress:

            # Pasa al equipo siguiente si hay mas equipos y la vista actual es equipos
            if event.key == CONTROLES['equipos']['proximo_equipo'] and state['vista_actual'] == 'equipos':  
                state['equipo_actual'] += 1 if state['cantidad_equipos'] - 1 > state['equipo_actual'] else 0
                print(f"DEBUG: Equipo actual: {state['equipo_actual']}")
            
            # Vuelve al equipo anterior dependiento de la vista actual y si hay otro equipo
            if event.key == CONTROLES['equipos']['anterior_equipo'] and state['vista_actual'] == 'equipos':  
                state['equipo_actual'] -= 1 if state['equipo_actual'] > 0 else 0
                print(f"DEBUG: Equipo actual: {state['equipo_actual']}")
            
            # Cambia el estado elegir_equipos a True si se presiona la tecla <elegir_equipos>
            if event.key == CONTROLES['equipos']['elegir_equipos'] and state['vista_actual'] == 'equipos':
                state['elegir_equipos'] = True

            