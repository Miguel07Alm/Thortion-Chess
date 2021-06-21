class Error(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return "Error: "+ self.message
def binary(value):
    '''Aclaración: la función 'append' en una lista sirve para añadir un objeto seguidamente de otro,
    como por ejemplo, si en una lista "[]" se encuentra el número 5, tal que así, [5], usando la función dicha
    anteriormente se podría añadir cualquier objeto un indice superior al anterior si es que existe un objeto en una lista,
    por lo que poniendo 'lista.append(4)' daría de resultado [5,4] y así sucesivamente.
    '''
    #Será la lista donde añadiremos los restos junto con el cociente 1
    
    result = []
    positive= False
    #Analiza si el valor es positivo o negativo
    if value < 0:
        #Asigna el valor negativo a positivo
        value = -(value)
    else:
        positive = True
    #Al ser 0 o 1 el valor, devuelve el mismo número
    if value == 0 or value == 1:
        return "".join(str(0) * 7) + str(value)
    #Si el valor es 3 ,ya que da de cociente uno al dividir entre 2, devuelve dos 1
    elif value//2 == 1:
        result.append(value%2)
        result.append(value//2)
    #Si el valor es mayor que 3, el valor entra en un bucle por el cual divide entre 2, haciendo que el valor sea cada vez que entra en el bucle la division entre 2 y que no sea de cociente 1
    else:
        while value//2 != 1:
            result.append(value%2)
            value = value //2
            #Si el cociente del valor entre 2 da 1 devuelven dos 1
            if value//2 == 1:
                result.append(value%2)
                result.append(1)
                break
        #Al terminar el bucle se obtiene el resto y el cociente
        else:
            result.append(0)
            result.append(1)
    #Teniendo los resultados de los restos, ahora se invierte el orden de la lista
    if positive:
        binary_result = result[::-1]
    #Si es negativo el valor inicial, se sustituyen los 1 por los 0 y viceversa, haciendo que 
    #al final se invierta el orden de la lista como con los números positivos
    else:
        binary_result = result
        #Variable booleana(False o True) por la cual averiguo si se encuentra el 1
        find_1 = False
        #Bucle por el cual se sustituyen los 0 por los 1 y viceversa cuando encuentra el primer 1
        for i in range(len(binary_result)):
            if find_1:
                if binary_result[i] == 1:
                    binary_result[i] = 0
                else:
                    binary_result[i] = 1
            if binary_result[i] == 1:
                find_1 = True
        binary_result = binary_result[::-1]
        
    #Devuelve el resultado en tipo integer ya que con esta funcion ' "".join(iterable) ' se puede
    #poner una lista como por ejemplo [1,0,1,1] en un string tipo '1011' 
    n_Zeros = (8 - len(binary_result)) % 8 
    return "".join([str(0)] * n_Zeros) + "".join(str(number) for number in binary_result)

def binary_to_decimal(biny):
    #Se hace una variable que ponga cada numero por separado para ver si hay
    #alguno que no es 0 o 1
    comprobation_num = list(x for x in biny)
    for i in range(len(biny)):
        if comprobation_num[i] in [str(x) for x in range(2,10)]:
            raise ValueError("Sólo se admiten números binarios")
    #Se pone en una lista el numero binario separando los 0 y los 1 por comas
    bin_nums = list("".join([num for num in biny]))
    bin_nums = [int(num) for num in bin_nums]
    #Exponentes del 2
    exp_2 = list(range(len(bin_nums)))
    #Se invierten los numeros binarios de la lista
    bin_nums_rev = list(reversed(bin_nums))
    #Se hace la sumatoria para conseguir el número decimal tal como explique en el procedimiento hace páginas anteriores
    return sum([bin_nums_rev[indx] * 2**exp_2[indx] for indx in range(len(bin_nums_rev))])
    

def BCD(num):
    '''
    SOLO SIRVE PARA NÚMEROS POSITIVOS
    '''
    if num < 0:
        raise ValueError("Debes usar un número positivo, no uno negativo")
    #Con esto, puedo ya codificar los números decimales a binario, ya que en el Binary-Coded-Decimal, se usan sólo
    #los números binarios del 0 al 9
    bin_nums = [str(binary(x)) for x in range(10)]
        
                
    for i in range(len(bin_nums)):
        if len(bin_nums[i]) == 1:
            bin_nums[i] = "000" + bin_nums[i]
        elif len(bin_nums[i]) == 2:
            bin_nums[i] = "00" + bin_nums[i]
        elif len(bin_nums[i]) == 3:
            bin_nums[i] = "0" + bin_nums[i]
        else:
            pass
    
    dict_nums = {indx: bin_nums[indx] for indx,value in enumerate(bin_nums)}
    str_num = str(num)

    result_num_isolated = list(l for l in str_num)
    
    for i in range(len(result_num_isolated)):
        result_num_isolated[i] = dict_nums[int(result_num_isolated[i])]
    
    encrypted = " ".join(result_num_isolated)
    return encrypted
import string

def mergedicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(mergedicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])
            
            
def text_to_binary(text):
    '''ACLARACION: 
        para pasar a número binario texto hay que separar cada letra de la oración,
        en una lista por ejemplo, si quisiera traducir 'hola' debería de separar 
        todas las letras en una lista tal que quede así ['h','o','l','a']. Después, habrá que pasar esas letras
        a decimal por el código ASCII y por último, traducir esos números decimales a binario con
        8 bits por letra.       
    '''
    result_list = [letter for letter in text if letter != " "]
    
    all_letters_list_lowercase = [i for i in string.ascii_lowercase]
    all_letters_list_uppercase = [j for j in string.ascii_uppercase]
    
    ascii_code_decimal_lowercase = {all_letters_list_lowercase[indx]: indx+97 for indx, value in enumerate(all_letters_list_lowercase)}
    ascii_code_decimal_uppercase = {all_letters_list_uppercase[indx]: indx+65 for indx, value in enumerate(all_letters_list_uppercase)}
    ascii_code_decimal = dict(mergedicts(ascii_code_decimal_uppercase, ascii_code_decimal_lowercase))

    bin_nums = {indx+65:str(binary(x)) for indx,x in enumerate(range(65,123))}
    for indx in range(65,123):
        bin_nums[indx] = "0"+bin_nums[indx]
    
    #bin_text = [binary_to_decimal(bin_nums[indx]) for indx in range(65,123)]
    
    #Pasar la letra al numero asignado del código Ascii
    for indx in range(len(result_list)):
        result_list[indx] = ascii_code_decimal[result_list[indx]]
    
    for indx in range(len(result_list)):
        result_list[indx] = bin_nums[result_list[indx]]
        
            
    return " ".join(result_list)
            
def binary_to_hex(bin):
    '''
    EXPLICACIÓN: 
        El algoritmo coge la cadena de números binarios
        y de esta cadena, guarda en una lista cada cuarteto
        para así transformar el cuarteto a código hexadecimal.
    '''
    
    if len(bin) not in [x*4 for x in range(1,len(bin))]:
        raise ValueError("Debes poner números binarios en cuartetos y todos los numeros contados deben ser múltiplos de 4")
    start = True
    result = []
    indx = 4
    #PARA AGRUPAR EN GRUPOS DE MEDIO BYTE(4 BITS) LAS LISTAS
    while indx <= len(bin):
        if start:
            result.append(bin[:indx])
            start = False
        else:
            result.append(bin[indx:indx+4])
            indx += 4  
    #Si hay un cuarteto borraria en la lista el espacio vacío que se haya creado
    result.remove('')
    
    letters_bin_dict ={indx+10:letter for indx,letter in enumerate(string.ascii_uppercase) if indx <=5}
    
    return "".join(list(str(binary_to_decimal(result[indx])) if binary_to_decimal(result[indx]) < 10 else letters_bin_dict[binary_to_decimal(result[indx])] for indx,value in enumerate(result)))

def hex_to_bin(hex):
    '''
    ACLARACION: 
        El algoritmo hace que se guarde en una lista el binario 
        de cada hexadecimal aunque antes de eso, hay que asegurarse
        de que cada letra sea transformada en el decimal que indica el
        propio código, por lo tanto, teniendo en la lista cada binario de cada
        caracter del código hexadecimal dado, podemos convertirlo a binario fácilmente
        añadiendolo por grupos de 4 bits o medio byte.
    
    '''
    
    letters_bin_dict ={letter:indx+10 for indx,letter in enumerate(string.ascii_uppercase) if indx < 6}
    
    
    hex_list = [str(binary(int(h))) if h not in string.ascii_letters else str(binary(letters_bin_dict[h])) for h in hex]
    
    for indx,bin_num in enumerate(hex_list):
        hex_list[indx] = "0" * abs(len(bin_num) - 4) + hex_list[indx] if len(bin_num) < 4 else hex_list[indx]
        
    return " ".join(hex_list)

def hex_to_dec(hex):
    '''
    ACLARACIÓN:
        Reciclando el diccionario con las equivalencias de
        las letras en el código hexadecimal, podemos pasar
        a decimales cualquier código, el algoritmo lo que haría es
        transformar las letras en números, para después invertir ese código
        haciendo que cada dígito se multiplique por 16 elevado al índice de
        su posición, como por ejemplo:
            codigo_hex = 2FA, se pasa a decimal todo, haciendo la equivalencia 
            de la letra F a 15, y A a 10 dejando el codigo en 2 15 10. 
            Teniendo eso separado, lo invertimos dejándolo en 10 15 2 y 
            podemos ahora pasarlo a decimal tal que así: 10 x 16^0 + 15 x 16^1 + 2x16^2
            dando como resultado 762.
    '''
    hex = [x.lower() if x in string.ascii_uppercase else x for x in hex]
    letters_bin_dict ={letter:indx+10 for indx,letter in enumerate(string.ascii_lowercase) if indx <=5}
    hex_list = [h for h in hex]
    
    for indx,value in enumerate(hex_list):
        if value in string.ascii_lowercase:
            hex_list[indx] = letters_bin_dict[value]
    hex_list = list(reversed(hex_list))
    return sum([int(x) * 16**indx for indx, x in enumerate(hex_list)])
    
def dec_to_hex(dec):
    '''
    ACLARACIÓN:
        El algoritmo hace que guarde en una lista result cada resto 
        obtenido dividiendo el número decimal dado y 16, haciendo que
        cuando el dividendo sea más pequeño que 16 termine de guardarse
        la variable resto dentro de la lista. Para que así sea guardado
        el último divisor, ya teniendo la lista con todos los restos y el 
        último divisor, se invierte el orden para que así podamos convertir
        el número decimal en hexadecimal, cada variable de la lista será
        transformada mediante el código hexadecimal en un número o letra,
        terminando la conversión y dando el resultado en hexadecimal.
    '''
    
    letters_bin_dict ={str(indx+10):letter for indx,letter in enumerate(string.ascii_lowercase) if indx <=5}
    result = []
    if dec == 0 or dec == 1:
        return dec
    elif dec//16 == 2 and dec / 16 < 2.5:
        result.append(str(dec%16))
        result.append(str(dec//16))
        return "".join(result[::-1])
    while dec // 16 != 2:
        result.append(str(dec%16))
        if dec < 16:
            break
        
        dec = dec//16
    else:
        result.append(str(dec%16))
        result.append(str(dec//16))

    result = reversed(result)
    return "".join([str(x) if x not in letters_bin_dict else letters_bin_dict[x] for x in result])
        
        
    
#print(len(binary(12321)))
#print(binary_to_decimal('1000010011001000100111010100100100001101101010101110011011011000010100110011011100111111000101000'))

#print(binary_to_hex('0001000010011001000100111010100100100001101101010101110011011011000010100110011011100111111000101000'))
#print(hex_to_bin('2FA'))