"""
Intituto Tecnologico de Estudios Superiores de Monterrey
Equipo "Default":
Daniel de Zamacona Madero - A01570576
Elmer Osiel Avila Vargas - A00826359
El programa despliega un juego de snake con variantes de colores y movimientos de la comida
Fecha de Modificacion: 17/9/2020
"""
from random import choice
from turtle import *
from freegames import floor, vector

# Declaracion de valores iniciales
state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
# Matriz del tablero para la interfaz
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

'''
Dibuja un cuadro vacio segun una posicion vectorial
Entrada: Posicion Vectorial
Salida: Ninguna
'''
def square(x, y):
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    # For para dibujar el cuadro a partir de turtle
    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

'''
Regresa el posicionamiento del punto en el recuadro
Entrada: Una posicion vectorial donde se encuentra un punto
Salida: Posicion del punto
'''
def offset(point):
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

'''
Regresa true si el punto (posicion vectorial) mandado se trata de un recuadro valido en el mapa
Entrada: Vector de una posicion a validar
Salida: Booleano, si la posicion es valida o no
'''
def valid(point):
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

'''
Dibuja el tablero segun la ubicacion de los puntos regresados como verdaderos usando la matriz "tiles", que es el mapa
Entrada: Niguna
Salida: Ninguna
'''
def world():
    bgcolor('black')
    path.color('blue')

    # For para dibujar cada cuadro dentro de la interfaz
    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

'''
Genera el movimiento dentro del juego, tando de los fantasmas como de pacman y en caso de este ultimo sea alcanzado, es decir pierdes, se detiene el juego
Entrada: Niguna
Salida: Tiene un return que rompe el movimiento cuando un fantasma te alcanza, no regresa nada
'''
def move():
    writer.undo()
    writer.write(state['score'])

    clear()
    # Revisa si se puede tomar la direccion mandada por el usuario y realiza el movimiento en caso de que sea valido
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)
    # Revisa si pacman pasa encima de un punto, aumenta el marcador y elimina el punto en la interfaz
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    # Realiza la eleccion del movimiento de los fantasmas, y los mueve
    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            
            ''' Modificacion: Se aumenta la inteligencia de los fantasmas, ahora cuando esten en la misma escala ya sea de "x" o de "y" que el usuario,
                los fantasmas siempre se iran directo hacia pacman para intentar atraparlo'''
            if pacman.x == point.x and pacman.y > point.y and valid(point + vector(0,5)):
                plan = vector(0,5)
            elif pacman.x == point.x and pacman.y < point.y and valid(point + vector(0,-5)):
                plan = vector(0,-5)
            elif pacman.y == point.y and pacman.x > point.x and valid(point + vector(5,0)):
                plan = vector(5,0)
            elif pacman.y == point.y and pacman.x < point.x and valid(point + vector(-5,0)):
                plan = vector(-5,0)
            else:
                # En caso de que no este en una misma escala x o y, se realiza una eleccion al azar del siguiente movimiento
                options = [
                    vector(5, 0),
                    vector(-5, 0),
                    vector(0, 5),
                    vector(0, -5),
                ]
                plan = choice(options)

            # Se define el nuevo curso del fantasma segun la desicion anterior a partir de la variable plan
            course.x = plan.x
            course.y = plan.y
        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    # Revisa si un fantasma ha alcanzado a pacman y termina el movimiento en caso de que sea verdad
    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    ontimer(move, 100)

'''
Cambia la direccion del movimiento de pacman si es valida la entrada del usuario
Entrada: Vector de posicion que definira la nueva direccion
Salida: Ninguna
'''
def change(x, y):
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()