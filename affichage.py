from vecteur_normal import point, écran, objet
import pygame as pg
from math import cos, sin, pi

# Création d'objets 3D
points = [point([0,0,0], "A"), point([2,0,0], "B"), point([2,2,0], "C"), point([0,2,0], "D"),\
    point([0,0,2], "E"), point([2,0,2], "F"), point([2,2,2], "G"), point([0,2,2], "H")]

lignes = [
    ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
    ("A", "E"), ("B", "F"), ("C", "G"), ("D", "H"),
    ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E")
]

vue_1 = écran([-1,-1,-5], [[5,0,0],[0,5,0]], [-1,-1,-10])
vue_1.points2D = vue_1.calcul_points_2D(points)

cube = objet(points, "cube1")

# Importation pygame et création d'une fenêtre
pg.init()

win = pg.display.set_mode((1000,600), pg.RESIZABLE)
pg.display.set_caption("test final 3D")

horloge = pg.time.Clock()

# Caractéristiques texte
pala = 'Palatino Linotype'
style = pg.font.SysFont(pala, 10, True)
info = pg.font.SysFont(pala, 14, True)

couleur_axe = {
    "x" : (255,0,0),
    "y" : (0,255,0),
    "z" : (0,0,255)
}

noir = (0,0,0)
obj = "Objet"
cam = "Caméra"
control = cam
trace_lignes = True
axes = True
# 128 -> 30 fps
angle_rotation = pi/256
text_nom = True
vitesse_grossissement = 3
grossissement = 100
tempo = 0
en_marche = True
while en_marche :
    if tempo < 10 :
        tempo += 1
    for événement in pg.event.get() :
        if événement.type == pg.QUIT :
            en_marche = False
        if événement.type == pg.KEYDOWN and control == cam :
            if événement.unicode == "+":
                grossissement += vitesse_grossissement
            elif événement.unicode == "-":
                grossissement -= vitesse_grossissement

    win.fill((150,200,255))

    touche = pg.key.get_pressed()

    if touche[pg.K_n] and tempo >= 10 :
        if text_nom :
            text_nom = False
        else :
            text_nom = True
        tempo = 0

    if touche[pg.K_x] and tempo >= 10 :
        if axes :
            axes = False
        else :
            axes = True
        tempo = 0

    if touche[pg.K_l] and tempo >= 10 :
        if trace_lignes :
            trace_lignes = False
        else :
            trace_lignes = True
        tempo = 0

    if touche[pg.K_o] :
        control = obj

    if touche[pg.K_c] and tempo >= 10 :
        if control == cam :
            control = obj
        else :
            control = cam
        tempo = 0

    if touche[pg.K_p] and tempo >= 10 :
        if vue_1.perspective :
            vue_1.perspective = False
        else :
            vue_1.perspective = True
        tempo = 0
        vue_1.update(points)

    w, h = pg.display.get_surface().get_size()

    if axes :
        for nom_axe, valeurs in vue_1.axes().items() :
            if valeurs != None :
                if valeurs[-1] == 'y' :
                    for i in range(w) :
                        pg.draw.circle(win, couleur_axe[nom_axe], (i, h/2 - valeurs[0] * (i - w/2) - valeurs[1] * grossissement), 1)
                else :
                    for i in range(h) :
                        pg.draw.circle(win, couleur_axe[nom_axe], (w/2 + valeurs[0] * (i - h/2) + valeurs[1] * grossissement, h - i), 1)

    if trace_lignes :
        for element in lignes :
            pg.draw.line(win, (230,230,230),\
                (w/2 + vue_1.points2D[element[0]][0] * grossissement, h/2 - vue_1.points2D[element[0]][1] * grossissement),\
                    (w/2 + vue_1.points2D[element[1]][0] * grossissement, h/2 - vue_1.points2D[element[1]][1] * grossissement))

    for nom, coord in vue_1.points2D.items() :
        pg.draw.circle(win, noir, (w/2 + coord[0] * grossissement, h/2 - coord[1] * grossissement), 3)
        if text_nom :
            text = style.render(nom, 1, noir)
            win.blit(text, (w/2 + coord[0] * grossissement - text.get_width()/2, h/2 - coord[1] * grossissement - 10))

    if control == cam :

        if touche[pg.K_UP] :
            vue_1.o[2], vue_1.o[1] = vue_1.o[2] * cos(-angle_rotation) - vue_1.o[1] * sin(-angle_rotation), vue_1.o[2] * sin(-angle_rotation) + vue_1.o[1] * cos(-angle_rotation)
            vue_1.u[2], vue_1.u[1] = vue_1.u[2] * cos(-angle_rotation) - vue_1.u[1] * sin(-angle_rotation), vue_1.u[2] * sin(-angle_rotation) + vue_1.u[1] * cos(-angle_rotation)
            vue_1.v[2], vue_1.v[1] = vue_1.v[2] * cos(-angle_rotation) - vue_1.v[1] * sin(-angle_rotation), vue_1.v[2] * sin(-angle_rotation) + vue_1.v[1] * cos(-angle_rotation)
            vue_1.p[2], vue_1.p[1] = vue_1.p[2] * cos(-angle_rotation) - vue_1.p[1] * sin(-angle_rotation), vue_1.p[2] * sin(-angle_rotation) + vue_1.p[1] * cos(-angle_rotation)
            vue_1.update(points)
        elif touche[pg.K_DOWN] :
            vue_1.o[2], vue_1.o[1] = vue_1.o[2] * cos(angle_rotation) - vue_1.o[1] * sin(angle_rotation), vue_1.o[2] * sin(angle_rotation) + vue_1.o[1] * cos(angle_rotation)
            vue_1.u[2], vue_1.u[1] = vue_1.u[2] * cos(angle_rotation) - vue_1.u[1] * sin(angle_rotation), vue_1.u[2] * sin(angle_rotation) + vue_1.u[1] * cos(angle_rotation)
            vue_1.v[2], vue_1.v[1] = vue_1.v[2] * cos(angle_rotation) - vue_1.v[1] * sin(angle_rotation), vue_1.v[2] * sin(angle_rotation) + vue_1.v[1] * cos(angle_rotation)
            vue_1.p[2], vue_1.p[1] = vue_1.p[2] * cos(angle_rotation) - vue_1.p[1] * sin(angle_rotation), vue_1.p[2] * sin(angle_rotation) + vue_1.p[1] * cos(angle_rotation)
            vue_1.update(points)

        if touche[pg.K_LEFT] :
            vue_1.o[0], vue_1.o[2] = vue_1.o[0] * cos(-angle_rotation) - vue_1.o[2] * sin(-angle_rotation), vue_1.o[0] * sin(-angle_rotation) + vue_1.o[2] * cos(-angle_rotation)
            vue_1.u[0], vue_1.u[2] = vue_1.u[0] * cos(-angle_rotation) - vue_1.u[2] * sin(-angle_rotation), vue_1.u[0] * sin(-angle_rotation) + vue_1.u[2] * cos(-angle_rotation)
            vue_1.v[0], vue_1.v[2] = vue_1.v[0] * cos(-angle_rotation) - vue_1.v[2] * sin(-angle_rotation), vue_1.v[0] * sin(-angle_rotation) + vue_1.v[2] * cos(-angle_rotation)
            vue_1.p[0], vue_1.p[2] = vue_1.p[0] * cos(-angle_rotation) - vue_1.p[2] * sin(-angle_rotation), vue_1.p[0] * sin(-angle_rotation) + vue_1.p[2] * cos(-angle_rotation)
            vue_1.update(points)
        elif touche[pg.K_RIGHT] :
            vue_1.o[0], vue_1.o[2] = vue_1.o[0] * cos(angle_rotation) - vue_1.o[2] * sin(angle_rotation), vue_1.o[0] * sin(angle_rotation) + vue_1.o[2] * cos(angle_rotation)
            vue_1.u[0], vue_1.u[2] = vue_1.u[0] * cos(angle_rotation) - vue_1.u[2] * sin(angle_rotation), vue_1.u[0] * sin(angle_rotation) + vue_1.u[2] * cos(angle_rotation)
            vue_1.v[0], vue_1.v[2] = vue_1.v[0] * cos(angle_rotation) - vue_1.v[2] * sin(angle_rotation), vue_1.v[0] * sin(angle_rotation) + vue_1.v[2] * cos(angle_rotation)
            vue_1.p[0], vue_1.p[2] = vue_1.p[0] * cos(angle_rotation) - vue_1.p[2] * sin(angle_rotation), vue_1.p[0] * sin(angle_rotation) + vue_1.p[2] * cos(angle_rotation)
            vue_1.update(points)

    if h > 50 and w > 134:
        if vue_1.perspective :
            text2 = "Perspective"
        else :
            text2 = "Parallèle"
        if w > 394 :
            text = info.render(control, 1, noir)
            text2 = info.render(text2, 1, noir)
        else :
            text = info.render(control[0], 1, noir)
            text2 = info.render(text2[0], 1, noir)
        win.blit(text, (10, 10))
        win.blit(text2, (10, 15 + text.get_height()))

    pg.display.flip()

    horloge.tick(60)

pg.quit()