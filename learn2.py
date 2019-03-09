import matplotlib.pyplot
import numpy as np
from matplotlib import animation


def hasard(p):
    """renvoie True avec une probabilite p et False avec une probabilité 1-p"""
    r = np.random.random()  # on prend au hasard un nombre entre 0 et 1
    assert 0 <= p <= 1  # verifions que p est dans [0,1]
    return r <= p  # si n<=p (une proba p) on retourne True sinon on retourne False (une proba 1-p)


def creerForet(n, m, pcoccup):
    """cree une foret avec des arbres places aleatoirements"""
    foret = np.zeros((n, m))  # on cree un matrice n*m de zeros
    for i in range(n):
        for j in range(m):
            if hasard(pcoccup):
                foret[i, j] = 1.  # si on une proba p alors il y a un arbre
            else:
                foret[i, j] = 0.  # sinon il n'y a pas d'arbre
    return foret
    # <<<<<<<<<<<< 2) SIMULATION >>>>>>>>>>>>


def mettreLeFeu(foret):
    """met le feu a un arbre"""
    n, m = foret.shape
    i = int((n-1)*np.random.random())
    j = int((m-1)*np.random.random())
    while foret[i, j] != 2.:
        if foret[i, j] == 1.:
            foret[i, j] = 2.  # on met le feu la case d'indice (i,j)
        else:
            i = int((n-1)*np.random.random())
            j = int((m-1)*np.random.random())
    return foret


def peutBrulerSansVent(foret, i, j):
    """verifie si l'arbre d'indice (i,j) est a proximite d'un arbre en feu"""
    n, m = foret.shape  # n et m respectivement le nombre de lignes et de colonnes
    if foret[i, j] == 1.:
        for y in range(max(0, i - 1), min(n, i + 2)):  # bord haut et bas
            if foret[y, j] == 2.:
                return True
        for x in range(max(0, j - 1), min(m, j + 2)):  # bord gauche et droit
            if foret[i, x] == 2.:
                return True
    return False


def propageFeu(foret):
    """les arbres qui peuvent bruler autour d'un arbre en feu prennent feu
    """
    n, m = foret.shape  # n et m respectivement le nombre de lignes et de colonnes
    c = np.copy(foret)
    for i in range(n):
        for j in range(m):
            if peutBrulerSansVent(c, i, j):
                foret[i, j] = 2.
    for i in range(n):
        for j in range(m):
            r = np.random.random()
            if c[i, j] == 2. and r < 0.5:
                foret[i, j] = 3.
    return foret


def auFeu(foret):
    """verifie si au moins un arbre non en feu peut bruler"""
    n, m = foret.shape
    for i in range(n):
        for j in range(m):
            if peutBrulerSansVent(foret, i, j) or foret[i, j] == 2.:
                return True
    return False


def metFeuForet(foret):
    """met le feu et propage l'incendie jusqu'a ce que tous les arbres qui peuvent bruler soient en feu"""
    foret = mettreLeFeu(foret)
    while auFeu(foret):
        foret = propageFeu(foret)
    return foret


# <<<<<<<<<<<< 3) ANIMATION >>>>>>>>>>>>
def animationFeu(foret):
    fig = matplotlib.pyplot.figure()  # nouvelle figure
    film = []
    # Initialisation
    foretFeu = mettreLeFeu(foret)
    film.append([matplotlib.pyplot.matshow(foret, fignum=False, animated=True)])
    matplotlib.pyplot.draw()  # mise a jour en temps reel du contenu des figures

    while auFeu(foret):
        foretFeu = propageFeu(foretFeu)
        film.append([matplotlib.pyplot.matshow(foretFeu, fignum=False, animated=True)])
        matplotlib.pyplot.draw()  # mise a jour en temps reel du contenu des figures

    ani = animation.ArtistAnimation(fig, film, interval=1000, blit=True, repeat_delay=100)
    matplotlib.pyplot.draw()  # mise a jour en temps reel du contenu des figures
    matplotlib.pyplot.show()


animationFeu(creerForet(50, 50, 0.5))
