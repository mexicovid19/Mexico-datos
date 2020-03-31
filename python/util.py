
edos = ['Aguascalientes (AGU)', 'Baja California (BCN)',
        'Baja California Sur (BCS)', 'Campeche (CAM)',
        'Chiapas (CHP)', 'Chihuahua (CHH)',
        'Ciudad de México (CMX)', 'Coahuila (COA)',
        'Colima (COL)', 'Durango (DUR)',
        'Estado de México (MEX)', 'Guanajuato (GUA)',
        'Guerrero (GRO)', 'Hidalgo (HID)',
        'Jalisco (JAL)', 'Michoacán (MIC)',
        'Morelos (MOR)', 'Nayarit (NAY)',
        'Nuevo León (NLE)', 'Oaxaca (OAX)',
        'Puebla (PUE)', 'Querétaro (QUE)',
        'Quintana Roo (ROO)', 'San Luis Potosí (SLP)',
        'Sinaloa (SIN)', 'Sonora (SON)',
        'Tabasco (TAB)', 'Tamaulipas (TAM)',
        'Tlaxcala (TLA)', 'Veracruz (VER)',
        'Yucatán (YUC)', 'Zacatecas (ZAC)']


def captura(entradas=edos, datos_previos=None):

    if datos_previos is not None:
        assert len(datos_previos) == len(entradas)

    data = []

    for i, x in enumerate(entradas):
        if datos_previos is not None:
            n = datos_previos[i]
            s = f'{x}, prev. {n} : ' if n > 0 else f'{x} : '
        else:
            s = f'{x} : '
        num = input(s)
        num = int(num) if num else 0
        data.append(num)

    print(f'\nTotal: {sum(data)}')

    corregir = True

    while corregir:
        siglas = input('Corregir (Introduce siglas; x para salir) : ')
        if siglas == 'x':
            corregir = False
        elif siglas == '':
            continue
        else:
            idx_entrada = [(i, x) for i, x in enumerate(entradas)
                           if siglas.upper() in x][0]
            num = input(f'{idx_entrada[1]} : ')
            num = int(num) if num else 0
            data[idx_entrada[0]] = num

    print(f'\nTotal: {sum(data)}')
    return data


if __name__ == '__main__':
    l = captura()
    print(l)
