
from tkinter.filedialog import askopenfilename
class simbolo:
    def __init__(self, token, lexema, linea, columna):
        self.token = token
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
#--------------------- Variables ---------------------------------------
tablaErrores =[]
tablaSimbolos=[]
fila = 0
columna = 0
banderaAutomataId = False
banderaAutomataNumero = False
banderaAutomataCadena = False
idConcaten = ""
numConcaten = ""
cadConcaten = ""
valor = ""
#-------------------------------------------------------------------------
def letras(c):
    return (ord(c) >= 65 and ord(c) <= 90) or (ord(c) >= 97 and ord(c) <= 122)

def numeros(c):
    return (ord(c) >= 48 and ord(c) <= 57)

def indicarEerror(simbolo, expectativa, linea, columna):
    cadenaError = "Error no se reconoce el simbolo: "+simbolo+ " se esperaba: "+expectativa+" en linea: "+str(linea)+" y columna: "+str(columna)
    print("Error no se reconoce el simbolo: "+simbolo+ " se esperaba: "+expectativa+" en linea: "+str(linea)+" y columna: "+str(columna))
    tablaErrores.append(cadenaError)

def automataID(c):
    global idConcaten, columna, fila, banderaAutomataId
    if letras(c) or numeros(c):
        idConcaten += c
        columna += 1
        return ;
    elif ord(c) == 32: #Espacio en Blanco
        idConcaten += c
        columna += 1
        tablaSimbolos.append(simbolo("ID",idConcaten,fila,(columna - 1 - len(idConcaten))))
        idConcaten=""
        banderaAutomataId=False
    elif ord (c) == 61: #signo igual
        tablaSimbolos.append(simbolo("ID",idConcaten,fila,(columna - len(idConcaten))))
        columna += 1
        tablaSimbolos.append(simbolo("simbolo_igual","=",fila,(columna - 2)))
        idConcaten=""
        banderaAutomataId=False
    else:
        indicarEerror(c,"",fila,columna)

def expresionRegularNumero(c):
    global columna,fila,banderaAutomataNumero,numConcaten
    if numeros(c):
        columna += 1
        numConcaten += c
        return 

    columna += 1
    tablaSimbolos.append(simbolo("NUMERO",numConcaten,fila,(columna - 1 - len(numConcaten))))
    numConcaten = ""
    banderaAutomataNumero = False

def automataParaCadenas(c):
    global cadConcaten,columna,fila,banderaAutomataCadena 

    if ord(c) == 34:
        columna += 1
        cadConcaten += c 
        tablaSimbolos.append(simbolo("CADENA",cadConcaten,fila,(columna - 1 - len(cadConcaten))))
        cadConcaten = ""
        banderaAutomataCadena = False
        return; 
    columna += 1
    cadConcaten += c

def analizadorLexico(c):
    global fila, columna, banderaAutomataId, idConcaten, banderaAutomataNumero, numConcaten, cadConcaten, valor, banderaAutomataCadena
    if banderaAutomataId:
        automataID(c)
    elif banderaAutomataNumero:
        expresionRegularNumero(c)
    elif banderaAutomataCadena:
        automataParaCadenas(c)
    elif letras(c):
        columna +=1
        banderaAutomataId = True
        idConcaten = c
    elif numeros(c):
        columna +=1
        banderaAutomataNumero =  True
        numConcaten = c
    elif ord(c) == 61: #=
        columna += 1
        valor = c
        tablaSimbolos.append(simbolo("simbolo_igual","=",fila,(columna - 2)))
        valor = ""
    elif ord(c) == 34: #""
        banderaAutomataCadena = True 
        cadConcaten = c
        columna += 1
    elif ord(c) == 10: #salto de linea
        fila += 1
        columna = 0
        valor = ""
    elif ord(c) == 32: #espacio
        columna += 1
        valor = ""
    else:
        indicarEerror(c,"",fila,columna) 

def leerArchivo():
    archivo = askopenfilename()#Abre la interfaz para escoger el archivo a cargar
    print(archivo)
    archivoLectura = open('' + archivo + '', 'r')
    for linea in archivoLectura:
        print(linea)
        print("\n")
        lineaCaracteres = list(linea)
        for obj in lineaCaracteres:
            analizadorLexico(obj)
        lineaCaracteres.clear
#cadena="Hola=\"como estas\" \n hola2 = 32 "
#caracteres = list(cadena)

#for obj in caracteres:
    #analizadorLexico(obj)



#print(caracteres)

#print("\n")

leerArchivo()
for a in tablaSimbolos:
        print(a.token+" _ "+a.lexema)