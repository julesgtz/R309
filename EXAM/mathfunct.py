import math

def log_de_x(val):
    return math.log(val)

def main():
    try:
        val = float(input("Entrez la valeur de X : "))
        assert val > 0
    except ValueError:
        return print("Veuillez entrer une bonne valeur de X")
    except AssertionError:
        return print("Il faut que la valeur soit plus grande que 0")
    else:
        print(log_de_x(val))

if __name__ == "__main__":
    main()