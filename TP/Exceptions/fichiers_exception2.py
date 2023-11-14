if __name__ == "__main__":
    fichier = "etudiant.txt"
    try:
        file = open(fichier, 'r')
    except FileNotFoundError:
        print("le fichier spéficié n'a pas été trouvé")
    except FileExistsError:
        print("Le fichier existe deja")
    except PermissionError:
        print("nous n'avons pas les permissions")
    except IOError:
        print("Erreur lors de l'ouverture / écriture du fichier")
    else:
        for l in file:
            l = l.rstrip("\n\r")
            print(l)
    finally:
        print("fin du programme")