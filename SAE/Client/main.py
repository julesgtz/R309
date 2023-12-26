from client import MainWindow
import argparse
import ipaddress
import sys
from PyQt5.QtWidgets import QApplication

def args_checker(args):
    """
    Permet de verifier si les arguments entrés sont bon
    :param args: Arguments passés pour lancer le script python
    :return: False si un argument est mauvais, sinon True
    """
    try:
        ipaddress.ip_address(args.get("i", None))
    except ValueError:
        print("L'ip que vous avez selectionné n'est pas bonne")
        return False
    except Exception as e:
        print(e)
        return False

    try:
        port = args.get("p",None)
        assert 0<port<65535
    except AssertionError:
        print("Le port n'est pas compris entre 0 et 65535")
        return False
    except Exception as e:
        print(e)
        return False

    return True



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Commande pour lancer le serveur")
    parser.add_argument('-i', required=True, type=str,
                        help="L'ip du serveur")
    parser.add_argument('-p', required=True, type=int,
                        help='Le port du server')

    args = vars(parser.parse_args())
    is_args_good = args_checker(args)

    if is_args_good:
        app = QApplication(sys.argv)
        MainWindow(ip=args['i'], port=args['p'])
        app.exec()

