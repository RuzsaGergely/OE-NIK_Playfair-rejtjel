# BevInfo féléves projekt # Playfair-kódoló # Óbudai Egyetem - Neumann János Informatikai Kar
# Készítette: Ruzsa Gergely Gábor (BR1GHH) # Üzemmérnök-informatikus Bprof. (Nappali tagozat)
import sys
import re
import unidecode

kodtabla = []

# A kódtábla fájlból való beolvasása valósul itt meg
def kodtablaBeolvasas():
    print("# Kódtábla beolvasása... #")
    kodtabla_beolv = open("kodtabla1.txt", "r").readlines()
    for s in kodtabla_beolv:
        uj_sor = []
        for k in s.strip():
            uj_sor.append(k)
        kodtabla.append(uj_sor)
    print("# Kódtábla beolvasva és feldolgozva! #")

# Ez a fgv. fogja meghatározni x,y kordinátában a karakterünk helyzetét a kódtáblában
def karakterKeres(k):
    for s in range(len(kodtabla)):
        for o in range(len(kodtabla[s])):
            if(kodtabla[s][o] == k):
                return s, o
    return -1, -1

# A Playfair-rejtjel szabályai szerint ha két ugyanolyan karakter követi egymást, akkor (minden/) a másodiknak fel kell vennie a speciális karaktert ami ebben az esetben az X lesz, mert ritkán használt betű.
# Mivel csak angol ábécével dolgozunk, így az ékezetes betűk normalizálva lesznek.
# Speciális karakterekkel és szóközzel nem foglalkozunk, így azok törlésre kerülnek a stringből.
def szovegTisztitas(be):
    ki = ""
    be = re.sub('\W+','', str(be))
    be = unidecode.unidecode(be)
    be = str(be).upper()
    if len(be) % 2 != 2:
        be += "X"
    for i in range(len(be)):
        if be[i] == be[i-1]:
            ki += 'X'
        else:
            ki += be[i]
    return ki

# A Playfair-rejtjel szabályai szerint a bemeneti szöveget két karakteres blokkokra kell bontani
def szovegTordeles(be):
    ki = []
    ideiglenes = []
    for i in range(len(be)):
        if i % 2 != 0:
            ideiglenes.append(be[i]) 
            ki.append(ideiglenes)
            ideiglenes = []
        else:
            ideiglenes.append(be[i])
    return ki

# 1. szabály: Ellenőrízzük, hogy a két betű egy sorban van
def sorEllenorzes(k1,k2):
    if k1[0] == k2[0]:
        return True
    else:
        return False

# 2. szabály: Ellenőrízzük, hogy a két betű egy oszlopban van
def oszlopEllenorzes(k1, k2):
    if k1[1] == k2[1]:
        return True
    else:
        return False

# 3. szabály: Ellenőrízzük, hogy a két betű különböző helyeken van, tehát téglalapot alkot
def teglalapEllenorzes(k1,k2):
    if k1[0] != k2[0]:
        return True
    else:
        return False

# Ez az eljárás felelős a karakterek átkódolásáért
def szovegKodolas(be, t):
    ki = ""
    szoveg = szovegTordeles(szovegTisztitas(be))
    for bp in szoveg:
        # Az első karakter koordinátája a kódtáblában <sor,oszlop>
        h1 = karakterKeres(bp[0])
        # A második karakter koordinátája a kódtáblában <sor,oszlop>
        h2 = karakterKeres(bp[1])
        
        if h1[0] == -1 or h2[0] == -1:
            print("Hiba! Ismeretlen karakter!")
            break

        if sorEllenorzes(h1,h2):
            if h1[1]+1 > len(kodtabla[0])-1:
                ki += kodtabla[h1[0]][0]
            else:
                ki += kodtabla[h1[0]][h1[1]+1]

            if h2[1]+1 > len(kodtabla[0])-1:
                ki += kodtabla[h2[0]][0]
            else:
                ki += kodtabla[h2[0]][h2[1]+1]
        elif oszlopEllenorzes(h1,h2):
            if h1[0]+1 > len(kodtabla)-1:
                ki += kodtabla[0][h1[1]]
            else:
                ki += kodtabla[h1[0]+1][h1[1]]
            
            if h2[0]+1 > len(kodtabla)-1:
                ki += kodtabla[0][h2[1]]
            else:
                ki += kodtabla[h2[0]+1][h2[1]]
        elif teglalapEllenorzes(h1,h2):
            ki += kodtabla[h1[0]][h2[1]]
            ki += kodtabla[h2[0]][h1[1]]
            
        else:
            print("Hiba történt kódolás közben!")
            exit(1)

        if t:
            print(f'Konverzió: {bp[0]}{bp[1]} -> {ki[-2]}{ki[-1]}')
    return ki

def szovegDekodolas(be, t):
    ki = ""
    szoveg = szovegTordeles(be)

    for bp in szoveg:
        # Az első karakter koordinátája a kódtáblában <sor,oszlop>
        h1 = karakterKeres(bp[0])
        # A második karakter koordinátája a kódtáblában <sor,oszlop>
        h2 = karakterKeres(bp[1])
        
        if h1[0] == -1 or h2[0] == -1:
            print("Hiba! Ismeretlen karakter!")
            break

        if sorEllenorzes(h1,h2):
            if h1[1]-1 > len(kodtabla[0])-1:
                ki += kodtabla[h1[0]][0]
            else:
                ki += kodtabla[h1[0]][h1[1]-1]

            if h2[1]-1 > len(kodtabla[0])-1:
                ki += kodtabla[h2[0]][0]
            else:
                ki += kodtabla[h2[0]][h2[1]-1]
        elif oszlopEllenorzes(h1,h2):
            if h1[0]-1 > len(kodtabla)-1:
                ki += kodtabla[0][h1[1]]
            else:
                ki += kodtabla[h1[0]-1][h1[1]]
            
            if h2[0]-1 > len(kodtabla)-1:
                ki += kodtabla[0][h2[1]]
            else:
                ki += kodtabla[h2[0]-1][h2[1]]
        elif teglalapEllenorzes(h1,h2):
            ki += kodtabla[h1[0]][h2[1]]
            ki += kodtabla[h2[0]][h1[1]]
        else:
            print("Hiba történ kódolás közben!")
            exit(1)

        if t:
            print(f'Konverzió: {bp[0]}{bp[1]} -> {ki[-2]}{ki[-1]}')
    return ki

def kodoloTeszt():
    print("~~ Playfair-kódoló ~~ OE-NIK # BevInfo ~~ Készítette: Ruzsa Gergely Gábor ~~ Szoftverdemo")
    kodtablaBeolvasas()
    demo_szoveg = "Neumann János Informatikai Kar"
    demo_szoveg_tiszt = szovegTisztitas(demo_szoveg)
    megoldas = "DNWJYEUOYEHGRDDXNJPVEHPEVEDU"
    print("# Paraméterek #")
    print(f'Eredeti szöveg: {demo_szoveg}')
    print(f'Tisztított szöveg: {szovegTisztitas(demo_szoveg)}')
    print(f'Betűpárokra tördelt szöveg: {szovegTordeles(szovegTisztitas(demo_szoveg))}')
    print("\n# Kódolás tesztelése #")
    print(f'Várt kódolt eredmény: {megoldas}')
    print(f'Kódolt megoldás: {szovegKodolas(demo_szoveg, True)}')
    if szovegKodolas(demo_szoveg, False) == megoldas:
        print("Siker! A megoldás és a kódolt megoldás megegyezik!")
    else:
        print("Hiba! A megoldás és a kódolt megoldás nem megegyezik!")
    print("A megoldás a https://www.dcode.fr/playfair-cipher oldal alapján került ellenőrzésre!")
    print("\n# Dekódolás tesztelése #")
    print(f'Várt dekódolt eredmény: {demo_szoveg_tiszt}')
    print(f'Dekódolt szöveg: {szovegDekodolas(megoldas, False)}')
    if szovegDekodolas(megoldas, False) == demo_szoveg_tiszt:
        print("Siker! A megoldás és a dekódolt megoldás megegyezik!")
    else:
        print("Hiba! A megoldás és a dekódolt megoldás nem megegyezik!")

    exit(0)

def kodoloFelhasznalo():
    print("~~ Playfair-kódoló ~~ OE-NIK # BevInfo ~~ Készítette: Ruzsa Gergely Gábor ~~ Felhasználói üzemmód # Szövegkódolás")
    kodtablaBeolvasas()
    bemenet = input("\nAdjon meg egy kódolandó jeligét: ")
    print(f'\nA kódolt szöveg: {szovegKodolas(bemenet, False)}')

def dekodoloFelhasznalo():
    print("~~ Playfair-kódoló ~~ OE-NIK # BevInfo ~~ Készítette: Ruzsa Gergely Gábor ~~ Felhasználói üzemmód # Szövegdekódolás")
    kodtablaBeolvasas()
    bemenet = input("\nAdjon meg egy dekódolandó jeligét: ")
    print(f'\nA dekódolt szöveg: {szovegDekodolas(bemenet, False)}')

def segitsegKiir():
    print("~~ Playfair-kódoló ~~ OE-NIK # BevInfo ~~ Készítette: Ruzsa Gergely Gábor ~~ Útmutató")
    print("./playfair.py [-h|-t|-k|-d]")
    print("\t-h\tKiírja az útmutatót")
    print("\t-t\tTeszteli a (de)kódoló működését")
    print("\t-k\tKódol egy megadott szöveget a kulcstábla alapján")
    print("\t-d\tDekódol egy kódolt szöveget a kulcstábla alapján")
    exit(0)

if len(sys.argv) < 2:
    segitsegKiir()
elif sys.argv[1] == "-h":
    segitsegKiir()
elif sys.argv[1] == "-t":
    kodoloTeszt()
elif sys.argv[1] == "-d":
    dekodoloFelhasznalo()
elif sys.argv[1] == "-k":
    kodoloFelhasznalo()
else:
    print("Hiba! Ismeretlen paraméter. Add meg a '-h' paramétert a segédlet kiiírásához!")
    exit(1)
