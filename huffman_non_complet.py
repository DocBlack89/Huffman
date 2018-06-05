#####################################################
######  Introduction à la cryptographie  	###
#####   Codes de Huffman             		###
####################################################

from heapq import *
import math

###  distribution de proba sur les letrres

caracteres = [
    ' ', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z' ]

proba = [
    0.1835, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
    0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
    0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
    0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008  ]

def frequences() :
    table = {}
    n = len(caracteres)
    for i in range(n) :
        table[caracteres[i]] = proba[i]
    return table

F = frequences()

###  la classe Arbre
class Tree:

    def __init__(self, root=None):
        self.root = root

    def __str__(self):
        if self.root is not None:
            return "Empty tree"
        else:
            return "Tree:\n" + self.root.print("", True)


class Arbre :
    def __init__(self, lettre, gauche=None, droit=None):
        self.gauche=gauche
        self.droit=droit
        self.lettre=lettre
    def estFeuille(self):
        return self.gauche == None and self.droit == None
    def estVide(self):
        return self == None
    def __str__(self):
        return '<'+ str(self.lettre)+'.'+str(self.gauche)+'.'+str(self.droit)+'>'


###  Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"
def arbre_huffman() :
    # à compléter
    liste2 = []
    for i in range(len(caracteres)):
        liste2.append((proba[i], Arbre(caracteres[i])))
    heapify(liste2)
    #print(liste2)
    while  len(liste2) > 1:
        node1 = heappop(liste2)
        node2 = heappop(liste2)
        parent = (node1[0] + node2[0], Arbre(None, gauche=node1[1], droit=node2[1]))

        heappush(liste2, parent)
    if len(liste2) == 1:
        final = Tree(liste2[0][1])
        #print(final)
        return final
    else:
        raise Exception()


###  Ex.2  construction du code d'Huffamn

def parcours(arbre, prefixe, code) :
    if arbre.estFeuille():
        code[arbre.lettre] = prefixe
        return

    parcours(arbre.gauche, prefixe + '0', code)
    parcours(arbre.droit, prefixe + '1', code)


def code_huffman(arbre) :
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    #print(arbre)
    code = {}
    parcours(arbre.root,'',code)
    return code



###  Ex.3  encodage d'un texte contenu dans un fichier

def encodage(dico,fichier) :
    fich = open(fichier, "r")
    compre = ""
    for caracteres in fich.read():
        for lettre, valeur in dico.items():
            if caracteres == lettre:
                compre = compre + valeur
            if caracteres not in dico:
                val = dico[' ']
                compre = compre + val
    fich_comp = open("leHorlaEncoded.txt", "a")
    fich_comp.write(compre)
    return compre

encode = encodage(code_huffman(arbre_huffman()),'leHorla.txt')
print(encode)


##  Ex.4  décodage d'un fichier compresse

def decodage(arbre,fichierCompresse) :
    '''
    Comment faire:
        -On lit bit par bit et on parcours l'arbre en suivant les préfixe
        - lorsque l'on arrive à une feuille dans l'arbre, on repars à 0 après avoir ajouté la letttre au texte décompréssé
    '''
#     #à compléter
    with open(fichierCompresse, "r") as f:
        data = f.read()
    courant = arbre.root
    content = ""
    for bit in data:
        if bit == "1":
            courant = courant.droit
        else:
            courant = courant.gauche
        if courant.estFeuille():
            content = content + courant.lettre
            courant = arbre.root
    fich_comp = open("leHorlaDecoded.txt", "a")
    fich_comp.write(content)
    return content

decode = decodage(arbre_huffman(),'leHorlaEncoded.txt')
print(decode)