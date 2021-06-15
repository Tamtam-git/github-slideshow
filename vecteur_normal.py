class point(object) :

    def __init__(self, coord: list, nom: str) -> object :
        self.nom = nom
        self.coord3D = coord

class objet(object) :

    def __init__(self, points: list, nom: str) -> object :
        self.nom = nom
        self.points = points

    def bouger(self, vecteur: list) :
        for pt in self.points :
            for i in range(3) :
                pt.coord3D[i] += vecteur[i]

    def tourner(self, angle: float, centre: list) :
        pass

class écran(object) :

    def __init__(self, origine: list, deux_vecteurs_directeurs: list, point_perspective: list) -> object :
        self.perspective = False
        self.p = point_perspective
        self.o = origine
        self.u = deux_vecteurs_directeurs[0]
        self.v = deux_vecteurs_directeurs[1]
        assert len(self.u) == len(self.v) == 3
        self.n = self.calcul_vecteur_normal()
        self.d = self.calcul_d()
        self.points2D = {}

    def calcul_vecteur_normal(self) -> list :
        try :
            x = 1
            y = self.calcul_valeur_n((0,1,2))
            z = self.calcul_valeur_n((0,2,1))
        except :
            try :
                x = self.calcul_valeur_n((1,0,2))
                y = 1
                z = self.calcul_valeur_n((1,2,0))
            except :
                try :
                    x = self.calcul_valeur_n((2,0,1))
                    y = self.calcul_valeur_n((2,1,0))
                    z = 1
                except :
                    print("échec du calcul du vecteur normal, valeur des vecteurs != noir")
        return [x,y,z]

    def calcul_d(self) -> float :
        d = 0
        for i in range(3) :
            d -= self.n[i] * self.o[i]
        return d

    def calcul_valeur_n(self, ordre) -> float :
            # dans l'ordre : connu, cherché et autre
            a, b, c = ordre
            coef = self.u[a] * self.v[c] - self.u[c] * self.v[a]
            if coef == 0 :
                res = 0
            else :
                res = coef / (self.u[c] * self.v[b] - self.u[b] * self.v[c])
            return res

    def calcul_point_2D(self, point: list) -> list :
        if self.perspective :
            vecteur = []
            for i in range(3) :
                vecteur += [self.p[i] - point.coord3D[i]]
        else :
            vecteur = self.n
        t = - (vecteur[0] * point.coord3D[0] + vecteur[1] * point.coord3D[1] + vecteur[2] * point.coord3D[2])\
            / (vecteur[0] ** 2 + vecteur[1] ** 2 + vecteur[2] ** 2)
        xyz = []
        for i in range(3) :
            xyz.append(point.coord3D[i] + vecteur[i] * t + self.o[i])
        try :
            y_écran = self.calcul_y_écran((0,1), xyz)
        except :
            try :
                y_écran = self.calcul_y_écran((1,2), xyz)
            except :
                try :
                    y_écran = self.calcul_y_écran((0,2), xyz)
                except :
                    print("échec du calcul de y_écran : c'est chelou tout ça")
        try :
            coef = xyz[0] - y_écran * self.v[0]
            if coef == 0 :
                x_écran = 0
            else :
                x_écran = coef / self.u[0]
        except :
            try :
                coef = xyz[1] - y_écran * self.v[1]
                if coef == 0 :
                    x_écran = 0
                else :
                    x_écran = coef / self.u[1]
            except :
                try :
                    coef = xyz[2] - y_écran * self.v[2]
                    if coef == 0 :
                        x_écran = 0
                    else :
                        x_écran = coef / self.u[2]
                except :
                    print("échec du calcul de x_écran -> ???")
        return [x_écran, y_écran, t]

    def calcul_points_2D(self, points) -> dict :
        pt_2D = {}
        for pt in points :
            pt_2D[pt.nom] = self.calcul_point_2D(pt)
        return pt_2D

    def calcul_y_écran(self, ordre, xyz) -> float :
        a, b = ordre
        coef = xyz[a] * self.u[b] - xyz[b] * self.u[a]
        if coef == 0 :
            y_écran = 0
        else :
            y_écran = coef / (self.u[b] * self.v[a] - self.u[a] * self.v[b])
        return y_écran

    def update(self, points) :
        self.n = self.calcul_vecteur_normal()
        self.d = self.calcul_d()
        self.points2D = self.calcul_points_2D(points)

    def axes(self) -> list :
        o_repère = self.calcul_point_2D(point([0,0,0], "O"))
        sortie = {}
        dico = self.calcul_points_2D(\
            [point([1,0,0], "x"), point([0,1,0], "y"), point([0,0,1], "z")])
        for nom, valeur in dico.items() :
            y_y = (valeur[1] - o_repère[1])
            x_x = (valeur[0] - o_repère[0])
            if y_y == 0 :
                if x_x == 0 :
                    sortie[nom] = None
                    continue
                coef = 0
                b = o_repère[1]
                f = "y"
            else :
                try :
                    coef = y_y / x_x
                    if coef > 1 or coef < -1 :
                        coef = 1 / coef
                        b = o_repère[0] - o_repère[1] * coef
                        f = "x"
                    else :
                        b = o_repère[1] - o_repère[0] * coef
                        f = "y"
                except :
                    coef = 0
                    b = o_repère[0] - o_repère[1] * coef
                    f = "x"
            sortie[nom] = [coef, b, f]
        return sortie