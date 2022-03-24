# AUTOR: Daniel Muñoz i Xamena

# Ejemplo de ejecución: python test.py '4,3' '2/2, 3/2, 3/1, 3/0, 2/0, 1/0, 0/0' 3

# Importamos para poder hacer copias no enlazadas de objetos
import copy

# Import para poder obtener los parámetros de ejecución des de la línea de comandos
import sys

# Representa una coordenada donde puede estar colocada una parte de la serpiente
class cell:
    # ATRIBUTOS:
    #   - fila: int
    #   - col: int
    def __init__(self, coord):
        # Restricciones
        if((coord[0] < 0) | (coord[1] < 0)):
            raise Exception("Las coordenadas tienen que ser positivas")

        self.fila = coord[0]
        self.col = coord[1]

    # Comprueba si la celda es adyacente a c
    def sonAdyacentes(self,c):
        if((self.fila != c.fila) & (self.col != c.col)):
            # Si ni la fila ni la columna son iguales no son adyacentes
            return False
        elif ((abs(self.fila - c.fila) > 1) | (abs(self.col - c.col) > 1)):
            # Si ni las filas ni las columnas son contiguas no son adyacentes
            return False
        
        return True

    # Comprueba si la celda es igual a c
    def iguales(self,c):
        # Dos celdas seran iguales si tienen la misma fila y columna
        return (self.fila == c.fila) & (self.col == c.col)

# Es una lista de celdas. Estas determinan la longitud y posición de la serpiente 
# en el tablero
class snake:
    # ATRIBUTOS:
    #   - sn: list(cell)
    def __init__(self, matrix):
        # La medida de la serpiente tiene que estar entre 
        # 3 y 7 celdas
        if(len(matrix) < 3):
            raise Exception("Serpiente demasiado pequeña")
        elif(len(matrix) > 7):
            raise Exception("Serpiente demasiado grande")

        # Cada elemento pasado en la matriz del constructor
        # será considerado como un objeto cell
        self.sn = list(map(cell,matrix))
    
    # Comprueba si la serpiente se cruza en algun punto del tablero
    def hayInterseccion(self):
        aux = [self.sn[0]]
        for i in range(1,len(self.sn),1):
            # Comprobamos si la celda i-esima ya la hemos ha aparecido.
            # De ser así querrá decir que el camino que sigue la serpiente se cruza
            comparaciones = list(map(lambda x: x.iguales(self.sn[i]),aux))
            if True in comparaciones:
                # Ya ha aparecido esta celda. Por lo tanto, hay una interseccion
                return True
            aux.append(self.sn[i])
        
        return False

    # Comprueba que todas las celdas sean adyacentes formando un camino continuo
    def esContinua(self):
        for i in range(len(self.sn) - 1):
            if(not self.sn[i].sonAdyacentes(self.sn[i + 1])):
                # Si la celda i-esima no es adyacente a la siguiente significa
                # que la serpiente no es continua
                return False
        return True
    
    # Mueve la cabeza de la serpiente a en la dirección indicada por el parámetro mov
    # A continuación el resto del cuerpo sigue a la cabeza.
    def mover(self,mov):
        # Guardamos la posición de la cabeza
        pos = self.sn[0]
        
        # Movemos la cabeza
        if(mov == 'L'):
            self.sn[0] = cell([self.sn[0].fila,self.sn[0].col - 1])
        if(mov == 'R'):
            self.sn[0] = cell([self.sn[0].fila,self.sn[0].col + 1])
        if(mov == 'D'):
            self.sn[0] = cell([self.sn[0].fila + 1,self.sn[0].col])
        if(mov == 'U'):
            self.sn[0] = cell([self.sn[0].fila - 1,self.sn[0].col])

        # Movemos el resto del cuerpo para que sea adyacente a la cabeza
        for i in range(1,len(self.sn),1):
            # Guardamos la posición actual de la celda
            aux = self.sn[i]

            # Modificamos la posición de la celda
            self.sn[i] = pos

            # Guardamos la posición donde se colocará la siguiente celda
            # La siguiente se colocará donde estaba la celda i-esima
            pos = aux

    def estaPrimeraFila(self):
        # Retornamos True si la cabeza esta en la primera fila
        return self.sn[0].fila == 0

    def estaPrimeraCol(self):
        # Retornamos True si la cabeza esta en la primera columna
        return self.sn[0].col == 0

# Contiene las dimensiones del tablero. Se utiliza para comprobar
# que la serpiente esté en una posición admitada dado el tablero
class board:
    # ATRIBUTOS:
    #   - snake: snake
    #   - nfilas: int
    #   - ncols: int
    def __init__(self,matrix,snake):
        # Restricciones
        if(len(matrix) != 2):
            raise Exception("El tablero tiene que ser de dos dimensiones")
        elif(matrix[0] > 10):
            raise Exception("El tablero puede tener 10 filas como máximo")
        elif(matrix[1] > 10):
            raise Exception("El tablero puede tener 10 columnas como máximo")
        
        # Guardamos las medidas de la matriz y la serpiente
        self.nfilas = matrix[0]
        self.ncols = matrix[1]
        self.snake = snake
        # Si la serpiente no es valida para este tablero ya no lo creamos
        if not self.snakeValida():
            raise Exception("La serpiente no es válida")

    # Comprobamos si la serpiente está en una posición valida para un tablero determinado
    def snakeValida(self):
        # Comprobamos que todas las celdas de la serpiente estan dentro del tablero
        dentroTablero = all(list(map(lambda cell: (cell.fila < self.nfilas) & (cell.col < self.ncols),self.snake.sn)))

        # Si existe alguna celda fuera del tablero la serpiente no es válida
        if not dentroTablero:
            return False

        # Comprobamos que cada celda de la serpiente esta unida a la siguiente
        if not self.snake.esContinua():
            return False

        # Comprobamos que no hay ninguna intersección
        if self.snake.hayInterseccion():
            return False

        return True

    # Movemos la serpiente en la dirección indicada por el parámetro mov
    def moverSnake(self,mov):
        self.snake.mover(mov)

        # Retornamos la serpiente movida
        return self.snake

    # Retorna una lista con los movimientos que dejarian a la serpiente en un
    # estado permitido
    def getMovValidos(self):
        mov = ['R','D']
        movVal = []

        # Si está en la primera fila no podemos ir hacia la arriba
        # ya que obtendriamos un punto negativo
        if(not self.snake.estaPrimeraFila()):
            mov.append('U')

        # Si está en la primera columna no podemos ir hacia la izquierda
        # ya que obtendriamos un punto negativo
        if(not self.snake.estaPrimeraCol()):
            mov.append('L')

        # Movemos la serpiente en todas las direcciones posibles.
        # Solo guardamos los movimientos que nos dejan la serpiente en un 
        # estado válido
        for m in mov:
            bd_aux = copy.deepcopy(self)
            bd_aux.snake = bd_aux.moverSnake(m)
            if bd_aux.snakeValida():
                # El movimiento es valido
                # Guardamos el movimiento
                movVal.append(m)
        
        return movVal

    # Cuenta cuantas posibles combinaciones de depth movimientos se pueden realizar 
    # en el tablero dado. Se ha utilizado un algoritmo recursivo que recorre el arbol
    # de posibles combinaciones en profundidad.
    def getCombinaciones(self,depth):
        # Ya no tenemos que bajar más en el arbol, por lo tanto se trata como un nodo hoja.
        # Retornamos el número de posibles movimientos que podriamos hacer en este nodo hoja.
        if(depth == 1):
            return len(self.getMovValidos())
        # Puede haber ramas que no tengan longitud depth. Estos casos no nos sirven.
        elif(len(self.getMovValidos()) == 0):
            return 0
        # Trata un nodo no hoja.
        else:
            sum = 0
            # Guardamos el estado del tablero en el nodo para cuando volvamos a él 
            # después de acceder a un nodo hoja.
            bd_nodo = copy.deepcopy(self)
            for m in (self.getMovValidos()):
                # Movemos la serpiente en una de las direcciones posibles y volvemos a llamar
                # a la función con un nivel de profundidad menor. Cuando esta rama llegue a un 
                # nodo hoja nos devolverá el número de combinaciones obtenidas para esta rama
                bd_aux = copy.deepcopy(bd_nodo)
                bd_aux.snake = bd_aux.moverSnake(m)
                a = bd_aux.getCombinaciones(depth - 1)
                sum += a
            # Al terminar el for y ahabremos explorado todas las ramas del nodo. Por lo tanto, en
            # la variable sum tendremos el número de combinaciones que se pueden realizar des de este
            # nodo hasta los nodos hoja.
            return sum



def main():
    # Comprobamos que se ha utilizado el comando correcto
    if len(sys.argv) != 4:
        raise Exception("Usar: board snake depth")

    # Construimos una lista de ints con el primer parámetro.
    # Esto nos indicará las medidas del tablero
    arg_board = [int(i) for i in sys.argv[1].split(',')]

    # Construimos la matriz que nos servirá para definir la serpiente inicial
    aux = list(map(lambda x: x.split('/'),sys.argv[2].split(',')))
    arg_snake = [[int(i[0]),int(i[1])] for i in aux]

    # Obtenemos el número de movimientos deseados
    arg_depth = int(sys.argv[3])

    # Construimos el tablero
    bd = board(arg_board,snake(arg_snake))
    
    # Obtenemos el número de combinaciones
    comb = bd.getCombinaciones(arg_depth)
    print("Combinaciones: " + str(comb))

if __name__ == "__main__":
    main()