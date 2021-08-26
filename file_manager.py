import csv

class FileManager():
    def __init__(self):
        self.ARCHIVO_POKEMONS = 'pokemons.csv'
        self.ARCHIVO_EQUIPOS = 'equipos.csv'
        self.ARCHIVO_DETALLE_MOVIMIENTOS = 'detalle_movimientos.csv'
        self.ARCHIVO_TABLA_TIPOS = 'tabla_tipos.csv'
        self.diccionario_pokemones_nombre = {}
        self.diccionario_pokemones_id = {}
        self.diccionario_detalle_movimientos_nombre = {}
        self.diccionario_tabla_tipos = {}
        self.cant_pokemones = 0

    def cargar_pokemones(self): 
        print(f'DEBUG: Cargando pokemones desde archivo')
        with open(self.ARCHIVO_POKEMONS) as file:
            reader = csv.DictReader(file, delimiter=';')
            for fila in reader:
                self.diccionario_pokemones_nombre[fila['nombre']] = fila
                self.diccionario_pokemones_id[int(fila['numero'])] = fila
                self.cant_pokemones += 1
                
    def cargar_detalle_movimientos(self):
        print(f'DEBUG: Cargando detalle de movimientos desde archivo')
        with open(self.ARCHIVO_DETALLE_MOVIMIENTOS) as file:
            reader = csv.DictReader(file, delimiter=',')
            for movimiento in reader:
                self.diccionario_detalle_movimientos_nombre[movimiento['nombre']] = {'categoria' : movimiento['categoria'],
                                                                                     'objetivo' : movimiento['objetivo'],
                                                                                     'pp' : movimiento['pp'],
                                                                                     'poder' : movimiento['poder'],
                                                                                     'tipo' : movimiento['tipo'],
                                                                                     'stats' : movimiento['stats'],
                                                                                    }
                
    def cargar_tabla_tipos(self):
        print(f'DEBUG: Cargando tabla tipos desde archivo')
        with open(self.ARCHIVO_TABLA_TIPOS) as file:
            reader = csv.DictReader(file, delimiter=';')
            for fila in reader:
                self.diccionario_tabla_tipos[fila['Types']] = {'Bug' : fila['Bug'],
                                                               'Dark' : fila['Dark'],
                                                               'Dragon' : fila['Dragon'],
                                                               'Electric' : fila['Electric'],
                                                               'Fairy' : fila['Fairy'],
                                                               'Fighting' : fila['Fighting'],
                                                               'Fire' : fila['Fire'],
                                                               'Flying' : fila['Flying'],
                                                               'Ghost' : fila['Ghost'],
                                                               'Grass' : fila['Grass'],
                                                               'Ground' : fila['Ground'],
                                                               'Ice' : fila['Ice'],
                                                               'Normal' : fila['Normal'],
                                                               'Poison' : fila['Poison'],
                                                               'Psychic' : fila['Psychic'],
                                                               'Rock' : fila['Rock'],
                                                               'Steel' : fila['Steel'],
                                                               'Water' : fila['Water'],
                                                               }
            
    def obtener_detalle_movimiento(self, nombre_movimiento):
        return self.diccionario_detalle_movimientos_nombre.get(nombre_movimiento, None)
        
    def obtener_pokemon_id(self, id):
        return self.diccionario_pokemones_id.get(id, None)
    
    def obtener_pokemon_nombre(self, nombre):
        return self.diccionario_pokemones_nombre.get(nombre, None)

    def cantidad_pokemones(self):
        print('DEBUG: Obteniendo cantidad de pokemones en el archivo')
        return self.cant_pokemones
    
    def cargar_equipos_desde_archivo(self, lista_equipos):
        print('DEBUG: Cargando equipos desde archivo')
        with open(self.ARCHIVO_EQUIPOS, 'r') as file:
            reader = csv.reader(file, delimiter = ";")
            
            equipo_actual = None
            
            for equipo, pokemon, movimientos in reader:
                print(f'DEBUG: Cargando {equipo}, {pokemon}, {movimientos}')
                if equipo_actual is None:
                    equipo_actual = Equipo(equipo)
                    equipo_actual.agregar_pokemon(pokemon, movimientos)
                    
                elif equipo_actual.nombre_equipo != equipo:
                    lista_equipos.append(equipo_actual)
                    equipo_actual = Equipo(equipo)
                    equipo_actual.agregar_pokemon(pokemon, movimientos)

                elif equipo_actual.nombre_equipo == equipo:
                    equipo_actual.agregar_pokemon(pokemon, movimientos)
            lista_equipos.append(equipo_actual)

class Equipo():
    """
    Esta clase se utiliza para generar objetos en base al archivo equipos.csv y solo contiene los pokemons pertenecientes a dicho equipo
    con los movimientos pertinentes a cada pokemon.
    """
    def __init__(self, nombre_equipo):
        self.nombre_equipo = nombre_equipo
        self.pokemones = {}
        
    def agregar_pokemon(self, nombre_pokemon, movimientos):
        self.pokemones[nombre_pokemon] = movimientos
        
    def cantidad_pokemones(self):
        return len(self.pokemones)
    
    def obtener_pokemones(self):
        return self.pokemones
    
class Entrenador():
    """
    Esta clase es la que contendra a los objetos Pokemons y solo se crearan dos instancias de esta clase, una para cada equipo seleccionado.
    """
    def __init__(self, nombre_entrenador):
        self.nombre_entrenador = nombre_entrenador
        self.pokemones = {}
        self.pokemon_activo = None
        self.cantidad_pokemones = None
    
    def agregar_pokemon(self, pokemon):
        self.pokemones[pokemon.nombre] = pokemon  
        
    def hay_pokemones_vivos(self):
        for pokemon in self.pokemones.values():
            if pokemon.hp > 0:
                return True
        return False
    
    def obtener_nombre_pokemones(self):
        return self.pokemones.keys()
        
    def __str__(self):
        return f"""
        Nombre entrenador: {self.nombre_entrenador}
        Pokemones: {self.pokemones}
        Pokemon_activo: {self.pokemon_activo}
        Cantidad de pokemones: {self.cantidad_pokemones}
        """
    
class Pokemon():
    """
    Esta clase solo se utilizara para los pokemons que formen parte de los equipos seleccionados.
    """
    def __init__(self, nombre, tipo, imagen, hp, atk, defe, spa, spd, spe):
        self.nombre = nombre
        self.tipo = tipo
        self.imagen = imagen
        self.hp = 110 + int(hp)
        self.hp_max = 110 + int(hp)
        self.atk = int(atk)
        self.defe = int(defe)
        self.spa = int(spa)
        self.spd = int(spd)
        self.spe = int(spe)
        self.movimientos = {}
        self.movimiento_a_realizar = None
        
    def esta_vivo(self):
        return True if self.hp > 0 else False
    
    def agregar_movimiento(self, movimiento):
        self.movimientos[movimiento.nombre] = movimiento
        
    def obtener_movimientos(self):
        return self.movimientos.keys()
        
    def __str__(self):
        return f"""
        Nombre: {self.nombre}
        Tipo: {self.tipo}
        Imagen: {self.imagen}
        HP: {self.hp}
        ATK: {self.atk}
        DEF: {self.defe}
        SPA: {self.spa}
        SPD: {self.spd}
        SPE: {self.spe}
        Movimientos: {self.movimientos}
        """
        
class Movimiento():
    """
    Esta clase solo se utilizara para los movimientos de los pokemons que formen parte de los equipos seleccionados.
    """
    def __init__(self, nombre, categoria, objetivo, pp, poder, tipo, stats):
        self.nombre = nombre
        self.categoria = categoria
        self.objetivo = objetivo
        self.pp = pp
        self.poder = int(poder)
        self.tipo = tipo
        self.stats = stats
        
    def __str__(self):
        return f"""
        Nombre: {self.nombre}
        Categoria: {self.categoria}
        Objetivo: {self.objetivo}
        PP: {self.pp}
        Poder: {self.poder}
        Tipo: {self.tipo}
        Stats: {self.stats}
        """

