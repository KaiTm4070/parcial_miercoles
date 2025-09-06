def comparar_abs(num1, num2):
    """Compara los valores absolutos de dos números como strings"""
    if len(num1) != len(num2):
        return len(num1) - len(num2)
    return (num1 > num2) - (num1 < num2)


def sumar_positivos(num1, num2):
    num1, num2 = num1.zfill(max(len(num1), len(num2))), num2.zfill(max(len(num1), len(num2)))
    carry, resultado = 0, []

    for i in range(len(num1)-1, -1, -1):
        s = int(num1[i]) + int(num2[i]) + carry
        resultado.append(str(s % 10))
        carry = s // 10

    if carry:
        resultado.append(str(carry))

    return ''.join(reversed(resultado))


def restar_positivos(num1, num2):
    """Asume num1 >= num2"""
    num1, num2 = num1.zfill(max(len(num1), len(num2))), num2.zfill(max(len(num1), len(num2)))
    carry, resultado = 0, []

    for i in range(len(num1)-1, -1, -1):
        r = int(num1[i]) - int(num2[i]) - carry
        if r < 0:
            r += 10
            carry = 1
        else:
            carry = 0
        resultado.append(str(r))

    return ''.join(reversed(resultado)).lstrip("0") or "0"


def sumar(num1, num2):
    neg1, neg2 = num1.startswith("-"), num2.startswith("-")
    num1, num2 = num1.lstrip("-"), num2.lstrip("-")

    if not neg1 and not neg2:  # positivo + positivo
        return sumar_positivos(num1, num2)
    elif neg1 and neg2:  # negativo + negativo
        return "-" + sumar_positivos(num1, num2)
    else:  # uno positivo y otro negativo → resta
        cmp = comparar_abs(num1, num2)
        if cmp == 0:
            return "0"
        elif cmp > 0:  # |num1| > |num2|
            res = restar_positivos(num1, num2)
            return "-" + res if neg1 else res
        else:  # |num2| > |num1|
            res = restar_positivos(num2, num1)
            return "-" + res if neg2 else res


def restar(num1, num2):
    # Restar es sumar el opuesto
    if num2.startswith("-"):
        return sumar(num1, num2.lstrip("-"))
    else:
        return sumar(num1, "-" + num2)


def multiplicar(num1, num2):
    neg = (num1.startswith("-")) ^ (num2.startswith("-"))
    num1, num2 = num1.lstrip("-"), num2.lstrip("-")

    if num1 == "0" or num2 == "0":
        return "0"

    m, n = len(num1), len(num2)
    resultado = [0] * (m + n)

    for i in range(m-1, -1, -1):
        for j in range(n-1, -1, -1):
            mult = int(num1[i]) * int(num2[j])
            suma = mult + resultado[i+j+1]
            resultado[i+j+1] = suma % 10
            resultado[i+j] += suma // 10

    res = ''.join(map(str, resultado)).lstrip("0")
    return "-" + res if neg else res


def dividir(num1, num2):
    """División entera de números grandes (como //)"""
    if num2 == "0":
        raise ZeroDivisionError("No se puede dividir entre cero")

    neg = (num1.startswith("-")) ^ (num2.startswith("-"))
    num1, num2 = num1.lstrip("-"), num2.lstrip("-")

    # Si el divisor es mayor, resultado = 0
    if comparar_abs(num1, num2) < 0:
        return "0"

    cociente, resto = [], ""
    for digito in num1:
        resto += digito
        resto = resto.lstrip("0") or "0"

        # Buscar cuántas veces cabe num2 en resto
        contador = 0
        while comparar_abs(resto, num2) >= 0:
            resto = restar_positivos(resto, num2)
            contador += 1
        cociente.append(str(contador))

    res = ''.join(cociente).lstrip("0") or "0"
    return "-" + res if neg else res


def potencia(num1, num2):
    neg = num1.startswith("-")
    num1, num2 = num1.lstrip("-"), int(num2)

    resultado = "1"
    for _ in range(num2):
        resultado = multiplicar(resultado, num1)

    if neg and num2 % 2 != 0:
        resultado = "-" + resultado

    return resultado


def a_notacion_cientifica(num_str, limite=30):
    neg = num_str.startswith("-")
    num_str = num_str.lstrip("-")

    if len(num_str) > limite:
        return ("-" if neg else "") + f"{num_str[0]}.{num_str[1:6]}e+{len(num_str)-1}"
    return ("-" if neg else "") + num_str


def calculadora():
    print("=== CALCULADORA DE NÚMEROS GIGANTES ===")
    print("Operaciones: +, -, *, /, ^ (potencia)")
    print("Soporta números negativos")
    print("Escribe 'salir' para terminar.\n")

    while True:
        expresion = input("Ingresa operación (ejemplo: 12345 * -6789): ")

        if expresion.lower() == "salir":
            break

        try:
            partes = expresion.split()
            if len(partes) != 3:
                print("Formato inválido. Usa: num1 operador num2")
                continue

            num1, op, num2 = partes

            if op == "+":
                resultado = sumar(num1, num2)
            elif op == "-":
                resultado = restar(num1, num2)
            elif op == "*":
                resultado = multiplicar(num1, num2)
            elif op == "/":
                resultado = dividir(num1, num2)
            elif op == "^":
                resultado = potencia(num1, num2)
            else:
                print("Operador no válido.")
                continue

            print("Resultado:", a_notacion_cientifica(resultado))

        except Exception as e:
            print("Error:", e)

# Ejecutar
calculadora()