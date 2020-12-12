'''
this file is part of "Thampu"
copyright 2020 Rodrigo Garcia <rgarcia@laotra.red>
'''
def ordenar_tamaños(lista):
    tamaños = sorted([tupla[0] for tupla in lista], reverse=True)
    limitesOrdenados = []
    for tam in tamaños:
        found = False
        j = 0
        while not found and j < len(tamaños):
            if lista[j][0] == tam:
                found = True
                limitesOrdenados.append((tam, lista[j][1]))
            j = j + 1
    return limitesOrdenados

def unidad_almacenamiento(tam):
    cad = ''
    tam = int(tam)
    if tam < 1000:
        cad = '{0} B'.format(tam)
    elif tam >= 1000 and tam < 1000000:
        cad = '{0:0.2f} KB'.format(tam/1000)
    elif tam >= 1000000 and tam < 1000000000:
        cad = '{0:0.2f} MB'.format(tam/1000000)
    elif tam >= 1000000000:
        cad = '{0:0.2f} GB'.format(tam/1000000000)
    return cad
