if __name__ == "__main__":
    fichier = "etudiant.txt"
    try:
        with open(fichier, 'r') as f:
            for l in f:
                l = l.rstrip("\n\r")
                print(l)
    except FileNotFoundError:
        print("le fichier spéficié n'a pas été trouvé")
    except FileExistsError:
        print("Le fichier existe deja")
    except PermissionError:
        print("nous n'avons pas les permissions")
    except IOError:
        print("Erreur lors de l'ouverture / écriture du fichier")
    else:
        print("Aucune erreur détectée")
    finally:
        print("fin du programme")