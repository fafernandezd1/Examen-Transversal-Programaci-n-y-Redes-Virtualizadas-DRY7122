def verificar_rango_vlan(numero_vlan):
    numero_vlan = int(numero_vlan) 
    
    if 1 <= numero_vlan <= 1005:
        return "VLAN {} pertenece al rango normal (1-1005)".format(numero_vlan)
    elif 1006 <= numero_vlan <= 4094:
        return "VLAN {} pertenece al rango extendido (1006-4094)".format(numero_vlan)
    else:
        return "VLAN {} no pertenece a ningún rango válido".format(numero_vlan)

# Solicitar al usuario ingresar el número de VLAN
numero_vlan = input("Ingrese el número de VLAN: ")

# Llamar a la función para verificar el rango de la VLAN y mostrar el resultado
resultado = verificar_rango_vlan(numero_vlan)
print(resultado)
