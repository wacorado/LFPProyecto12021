
from tkinter.filedialog import askopenfilename
class simbolo:
    def __init__(self, token, lexema, linea, columna):
        self.token = token
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
class cliente:
    def __init__(self, token, lexema, linea, columna):
        self.token = token
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
class Data:
    def __init__(self,id,valor):
        self.id = id
        self.valor = valor
class Productos:
    def __init__(self,id,nombre,precio,descripcion):
        self.id = id
        self.nombre = nombre
        self.precio = precio 
        self.descripcion = descripcion

#--------------------- Variables ---------------------------------------
tablaErrores =[]
tablaSimbolos=[]
tablaSFactura=[]
tablaRestaurante =[]
tablaCliente = []
fila = 1
columna = 1
banderaAutomataId = False
banderaAutomataNumero = False
banderaAutomataCadena = False
banderaAutomataRestaurante = False
banderaErCadenaFactura = False
banderaErNumeroFactura = False
banderaErSeccion = False
banderaAutomataSeccion = False
banderaAutomataProducto = False
banderaAutomataNombreCliente= False
banderaDetalleFactura = False
estado = 0
temporal = None
banderaErSeccion = False
idConcaten = ""
numConcaten = ""
cadConcaten = ""
valor = ""
cadenaProductosTemp=""

#-------------------------------------------------------------------------
def letras(c):
    return (ord(c) >= 65 and ord(c) <= 90) or (ord(c) >= 97 and ord(c) <= 122)

def numeros(c):
    return (ord(c) >= 48 and ord(c) <= 57)

def indicarEerror(simbolo, expectativa, linea, columna):
    cadenaError = "Error no se reconoce el simbolo: "+simbolo+ " se esperaba: "+expectativa+" en linea: "+str(linea)+" y columna: "+str(columna)
    print("Error no se reconoce el simbolo: "+simbolo+ " se esperaba: "+expectativa+" en linea: "+str(linea)+" y columna: "+str(columna))
    tablaErrores.append(cadenaError)

def erID(c):
    global idConcaten, columna, fila, banderaAutomataId
    if letras(c) or numeros(c) or ord(c)==95 or ord(c)==45:
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
    elif ord (c) == 59: #signo ;
        tablaSimbolos.append(simbolo("ID",idConcaten,fila,(columna - len(idConcaten))))
        columna += 1
        tablaSimbolos.append(simbolo("simbolo_PuntoComa",";",fila,(columna - 2)))
        idConcaten=""
        banderaAutomataId=False
    else:
        indicarEerror(c,"ID",fila,columna)

def erNumero(c):
    global columna,fila,banderaAutomataNumero,numConcaten
    if numeros(c) or ord(c) == 46:
        columna += 1
        numConcaten += c
        return 
    elif ord(c) == 32: #espacio
        columna += 1
        numConcaten += ""

    columna += 1
    tablaSimbolos.append(simbolo("NUMERO",numConcaten,fila,(columna - 1 - len(numConcaten))))
    numConcaten = ""
    banderaAutomataNumero = False

def erCadenas(c):
    global cadConcaten,columna,fila,banderaAutomataCadena 
    if letras(c) or numeros(c) or ord(c)==95 or ord(c)==45 or ord(c)==35 or ord(c)==44:
        cadConcaten += c
        columna += 1
    elif ord(c) == 39:
        columna += 1
        cadConcaten += c 
        tablaSimbolos.append(simbolo("CADENA",cadConcaten,fila,(columna - 1 - len(cadConcaten))))
        cadConcaten = ""
        banderaAutomataCadena = False
        return;
    else:
        indicarEerror(c,"CADENA",fila,columna)
    
def analizadorLexico(c):
    global fila, columna, banderaAutomataId, idConcaten, banderaAutomataNumero, numConcaten, cadConcaten, valor, banderaAutomataCadena, banderaErSeccion
    if banderaAutomataId:
        erID(c)
    elif banderaAutomataNumero:
        erNumero(c)
    elif banderaAutomataCadena:
        erCadenas(c)
    #elif banderaErSeccion:
    #    erSeccion(c)
    elif letras(c):
        columna +=1
        banderaAutomataId = True
        #banderaErSeccion = True
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
    elif ord(c) == 39: #""
        banderaAutomataCadena = True 
        cadConcaten = c
        columna += 1
    elif ord(c) == 10: #salto de linea
        fila += 1
        columna = 0
        valor = ""
    elif ord(c) == 32: #espacio
        columna += 1
        idConcaten = ""
        numConcaten = ""
        valor = ""
    elif ord(c) == 59: #;
        columna += 1
        valor = c
        tablaSimbolos.append(simbolo("simbolo_PuntoComa",c,fila,(columna - 2)))
        valor = ""
    elif ord(c) == 91: #[
        columna += 1
        valor = c
        tablaSimbolos.append(simbolo("simbolo_llave_abre",c,fila,(columna - 2)))
        valor = ""
    elif ord(c) == 93: #]
        columna += 1
        valor = c
        tablaSimbolos.append(simbolo("simbolo_llave_cierra",c,fila,(columna - 2)))
        valor = ""
    elif ord(c) == 93: #'
        columna += 1
        valor = c
        tablaSimbolos.append(simbolo("simbolo_comilla_simple",c,fila,(columna - 2)))
        valor = ""
    elif ord(c) == 58: #:
        columna += 1
        valor = c
        tablaSimbolos.append(simbolo("simbolo_2Puntos",c,fila,(columna - 2)))
        valor = ""
    elif ord(c) == 44: #,
        columna += 1
        valor = c
        tablaSimbolos.append(simbolo("simbolo_coma",c,fila,(columna - 2)))
        valor = ""
    elif ord(c) == 46: #.
        columna += 1
        valor = c
        tablaSimbolos.append(simbolo("simbolo_Punto",c,fila,(columna - 2)))
        valor = ""
    else:
        indicarEerror(c,"",fila,columna) 

def erCadenasFacturas(c):
    global valor,columna,fila,banderaErCadenaFactura 
    if letras(c) or numeros(c) or ord(c)==95 or ord(c)==45 or ord(c)==35 or ord(c)==44:
        valor += c
        columna += 1
    elif ord(c) == 39 or ord(c)==10:
        columna += 1
        valor += c 
        tablaSFactura.append(simbolo("CADENAF",valor,fila,(columna - 1 - len(valor))))
        valor = ""
        banderaErCadenaFactura = False
        return;
    else:
        indicarEerror(c,"CADENAFactura",fila,columna)

def erNumeroFacturas(c):
    global columna,fila,banderaErNumeroFactura,numConcaten
    if numeros(c) or ord(c)==46:
        columna += 1
        numConcaten += c
        return 
    elif ord(c) == 32 or ord(c)==44 or ord(c)==10: #espacio
        columna += 1
        tablaSFactura.append(simbolo("NUMERO",numConcaten,fila,(columna - 1 - len(numConcaten))))
        numConcaten = ""
        banderaErNumeroFactura = False

def analizadorLexicoFactura(c):
    global fila, columna, valor,numConcaten,banderaErCadenaFactura, banderaErNumeroFactura
    if banderaErCadenaFactura:
        erCadenasFacturas(c)
    elif banderaErNumeroFactura:
        erNumeroFacturas(c)
    elif letras(c):
        columna +=1
        valor = c
        banderaErCadenaFactura = True
    elif numeros(c):
        columna +=1
        banderaErNumeroFactura =  True
        numConcaten = c
    elif ord(c) == 39: # '
        banderaErCadenaFactura = True 
        valor = c
        columna += 1
    elif ord(c) == 44: #,
        columna += 1
        valor = c
        tablaSFactura.append(simbolo("simbolo_coma",c,fila,(columna - 2)))
        valor = ""
    elif ord(c) == 10: #salto de linea
        fila += 1
        columna = 0
        valor = ""
    else:
        indicarEerror(c,"",fila,columna) 

def automataNombreRestaurante(s):
    global temporal,tablaRestaurante,estado,banderaAutomataRestaurante
    if estado ==0:
        if(s.token=="simbolo_igual"):
            estado = 2
        else:
            estado = -1
            banderaAutomataRestaurante = False
            indicarEerror(s.lexema,"=",s.linea,s.columna)
    elif estado == 2:
        if(s.token=="CADENA"):
            temporal = (Data("Nombre Restaurante",s.lexema))
            estado=3
            tablaRestaurante.append(temporal) #Estado de Aceptacion
            estado = 0
            temporal= None
            banderaAutomataRestaurante = False
        else:
            estado = -1
            banderaAutomataRestaurante = False
            indicarEerror(a.lexema,"Nombre Restaurante",a.linea,a.columna)

def automataSeccion(s):
    global temporal,tablaRestaurante,estado,banderaAutomataSeccion
    if estado == 0:
        if(s.token=="simbolo_2Puntos"):
            tablaRestaurante.append(temporal) #Estado de Aceptacion para Seccion de Comida
            estado=0
            temporal = None
            banderaAutomataSeccion= False
        else:
            estado = -1
            banderaAutomataSeccion = False
            indicarEerror(a.lexema,"Seccion de Comida",a.linea,a.columna)

def automataProducto(s):
    global temporal,tablaRestaurante,estado,banderaAutomataProducto,cadenaProductosTemp
    if estado==0:
        if(s.token=="ID"):
            estado=1
            temporal = Data("Producto","")
            #listaProducTemp.append(s.lexema)
            cadenaProductosTemp = cadenaProductosTemp+";"+s.lexema
        else:
            estado = -1
            banderaAutomataProducto = False
            indicarEerror(s.lexema,"ID de Producto",s.linea,s.columna)
    elif estado==1:
        if(s.token=="simbolo_PuntoComa"):
            estado=2
        else:
            estado = -1
            banderaAutomataProducto = False
            indicarEerror(s.lexema,";",s.linea,s.columna)
    elif estado==2:
        if (s.token=="CADENA"):
            estado=3
            #listaProducTemp.append(s.lexema)
            cadenaProductosTemp = cadenaProductosTemp+";"+s.lexema
        else:
            estado = -1
            banderaAutomataProducto = False
            indicarEerror(s.lexema,"Nombre Producto",s.linea,s.columna)
    elif estado ==3:
        if s.token=="simbolo_PuntoComa":
            estado=4
        else:
            estado = -1
            banderaAutomataProducto = False
            indicarEerror(s.lexema,";",s.linea,s.columna)
    elif estado ==4:
        if (s.token=="NUMERO"):
            estado = 5
            #listaProducTemp.append(s.lexema)
            cadenaProductosTemp = cadenaProductosTemp+";"+s.lexema
        else:
            estado = -1
            banderaAutomataProducto = False
            indicarEerror(s.lexema,"Precio de Producto",s.linea,s.columna)
    elif estado ==5:
        if s.token =="CADENA":
            estado = 6
            #listaProducTemp.append(s.lexema)
            cadenaProductosTemp = cadenaProductosTemp+";"+s.lexema
        else:
            estado = -1
            banderaAutomataProducto = False
            indicarEerror(s.lexema,"Descripcion de Producto",s.linea,s.columna)
    elif estado==6:
        if s.token=="simbolo_PuntoComa":
            estado=0
            banderaAutomataProducto = False
        elif s.token == "simbolo_llave_cierra": #estado de aceptacion
            temporal.valor=cadenaProductosTemp
            tablaRestaurante.append(temporal)
            temporal=None
            #listaProducTemp.clear
            estado = 0
            cadenaProductosTemp=""
            banderaAutomataProducto = False
        else:
            estado = -1
            banderaAutomataProducto = False
            indicarEerror(s.lexema,"]",s.linea,s.columna)

def automataNombreCliente(s):
    global temporal,tablaCliente,estado,banderaAutomataNombreCliente
    if estado == 0:
        if(s.token=="simbolo_coma"):
            tablaCliente.append(temporal)# Estado de Aceptacion para Nombre de Cliente
            estado = 1
            temporal = None
            banderaAutomataNombreCliente = True
        else:
            estado = -1
            banderaAutomataNombreCliente = False
            indicarEerror(s.lexema,"NOMBRE",s.linea,s.columna)
    elif estado == 1:
        if(s.token=="CADENAF"):
            temporal = Data ("NIT",s.lexema)
            tablaCliente.append(temporal)
            estado = 2
            temporal = None
        else:
            estado = -1
            banderaAutomataNombreCliente = False
            indicarEerror(s.lexema,"NIT",s.linea,s.columna)
    elif estado == 2:
        if(s.token=="simbolo_coma"):
            estado = 3
        else:
            estado = -1
            banderaAutomataNombreCliente = False
            indicarEerror(s.lexema,",",s.linea,s.columna)
    elif estado == 3:
        if(s.token=="CADENAF"):
            temporal = Data ("Direccion",s.lexema)
            tablaCliente.append(temporal)
            estado = 4
            temporal = None
        else:
            estado = -1
            banderaAutomataNombreCliente = False
            indicarEerror(s.lexema,"Direccion",s.linea,s.columna)
    elif estado == 4:
        if(s.token=="simbolo_coma"):
            estado = 5
        else:
            estado = -1
            banderaAutomataNombreCliente = False
            indicarEerror(s.lexema,",",s.linea,s.columna)
    elif estado == 5:
        if(s.token=="NUMERO"):
            temporal = Data ("%",s.lexema)
            tablaCliente.append(temporal)
            estado = 0
            temporal = None
            banderaAutomataNombreCliente = False
        else:
            estado = -1
            banderaAutomataNombreCliente = False
            indicarEerror(s.lexema,"%",s.linea,s.columna)


def automataDetalleFactura(s):
    global temporal,tablaCliente,estado,banderaDetalleFactura
    if estado == 0:
        if(s.token=="simbolo_coma" or s.token=="CADENAF"):
            if(s.token=="CADENAF"):
                temporal.valor=temporal.valor+";"+str(s.lexema)
                tablaCliente.append(temporal)# Estado de Aceptacion para Nombre de Cliente
                estado = 0
                temporal = None
                banderaDetalleFactura = False
            elif(s.token=="simbolo_coma"):
                tablaCliente.append(temporal)# Estado de Aceptacion para Nombre de Cliente
                estado = 1
                banderaDetalleFactura = True
            else:
                estado = -1
                banderaDetalleFactura = False
                indicarEerror(s.lexema,"Cantidad",s.linea,s.columna)
    elif(estado==1):
        if(s.token=="CADENAF"):
            temporal.valor=temporal.valor+";"+str(s.lexema)
            tablaCliente.append(temporal)# Estado de Aceptacion para Nombre de Cliente
            estado = 0
            temporal = None
            banderaDetalleFactura = False
        else:
            estado = -1
            banderaDetalleFactura = False
            indicarEerror(s.lexema,"Cantidad",s.linea,s.columna)

def automataDirCliente(s):
    global temporal,tablaCliente,estado,banderaAutomataDirCliente
    if estado == 0:
        if(s.token=="simbolo_coma"):
            estado = 1
        else:
            estado = -1
            banderaAutomataDirCliente = False
            indicarEerror(s.lexema,"Direccion",s.linea,s.columna)
    elif estado == 1:
        if(s.token=="CADENAF"):
            temporal = Data("Direccion",s.lexema)
            tablaCliente.append(temporal)# Estado de Aceptacion para Nombre de Cliente
            estado = 0
            temporal = None
            banderaAutomataDirCliente = False
        else:
            estado = -1
            banderaAutomataDirCliente = False
            indicarEerror(s.lexema,"Direccion",s.linea,s.columna)
    


def leerArchivoMenu():
    archivo = askopenfilename()#Abre la interfaz para escoger el archivo a cargar
    print(archivo)
    archivoLectura = open('' + archivo + '', 'r')
    for linea in archivoLectura:
        print(linea)
        lineaCaracteres = list(linea)
        for obj in lineaCaracteres:
            analizadorLexico(obj)
        lineaCaracteres.clear
    print("---------------- Carga de Archivo Exitosa --------------")
    print("\n")

def leerArchivoFactura():
    archivo = askopenfilename()#Abre la interfaz para escoger el archivo a cargar
    print(archivo)
    archivoLectura = open('' + archivo + '', 'r')
    for linea in archivoLectura:
        print(linea)
        lineaCaracteres = list(linea)
        for obj in lineaCaracteres:
            analizadorLexicoFactura(obj)
        lineaCaracteres.clear
    print("---------------- Carga de Archivo Exitosa --------------")
    print("\n")


#leerArchivoMenu()
leerArchivoFactura()
#------------------------- Impresion de resultado Sintactico -----------------------
print("--------------- Resultado Sintactico -----------------")
for a in tablaSimbolos:
    print(a.token+" _ "+a.lexema)
for obj in tablaSFactura:
    print(obj.token+" _ "+obj.lexema)

#---------------------------Impresione de Errores -------------------------------
print("\n")
print("--------------- ERRORES CAPTURADOS -----------------")
for obj in tablaErrores:
    print(obj)

#--------------------------- Aalisis Sintactico ----------------------------------
for s in tablaSimbolos:
    if banderaAutomataRestaurante:
        automataNombreRestaurante(s)
    elif banderaAutomataSeccion:
        automataSeccion(s)
    elif banderaAutomataProducto:
        automataProducto(s)
    elif s.token == "ID":
        estado = 0
        banderaAutomataRestaurante = True
    elif s.token == "CADENA":
        estado = 0
        temporal = (Data("Sección ",s.lexema))
        banderaAutomataSeccion = True
    elif s.token == "simbolo_llave_abre":
        estado = 0
        banderaAutomataProducto = True
    else:
        indicarEerror(s.lexema,"",s.linea,s.columna)


for s in tablaSFactura:
    if banderaAutomataNombreCliente:
        automataNombreCliente(s)
    elif banderaDetalleFactura:
        automataDetalleFactura(s)
    elif s.token == "CADENAF":
        estado = 0 
        temporal = Data("Nombre Cliente",s.lexema)
        banderaAutomataNombreCliente = True
    elif s.token == "NUMERO":
        estado = 0
        temporal = Data("Cantidad Prod",s.lexema)
        banderaDetalleFactura = True

        
    else:
        indicarEerror(s.lexema,"",s.linea,s.columna)


print("----------Data Restaurante ------------------------")
for obj in tablaRestaurante:
    print(obj.id+" : "+str(obj.valor))

for obj in tablaCliente:
    print(obj.id+" : "+ str(obj.valor))
        #print("-------- Fin Automatas del sintactico----------------")
    