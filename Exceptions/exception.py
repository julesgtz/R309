# Le code divise un nombre entier par un autre
# On doit gérer valueerror au cas ou l'user rentre autre chose qu'un nombre entier
# On a une erreur de récursivitée
def divEntier(x: int, y: int):
    try:
        assert x >= 0
    except AssertionError:
        return "X est négatif"
    try:
        assert y >= 0
    except AssertionError:
        return "Y est négatif"
    try:
        assert y != 0
    except AssertionError:
        return "Y est égal a 0"

    if x < y:
        return 0
    else:
        x = x - y
    return divEntier(x, y) + 1



def main():
    while True:
        try:
            x = int(input("entrez une valeur pour x : "))
            y = int(input("entrez une valeur pour y : "))
        except ValueError:
            print("veuillez entrer de bonnes valeurs")
        else:
            try:
                print(divEntier(x,y))
            except RecursionError:
                print("Impossible de diviser par 0")
            return

if __name__=="__main__":
    main()