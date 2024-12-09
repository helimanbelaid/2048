import random
import keyboard

def init_plateau(taille):
    plateau = [[0] * taille for _ in range(taille)]
    ajouter_nouvelle_tuile(plateau)
    ajouter_nouvelle_tuile(plateau)
    return plateau

def ajouter_nouvelle_tuile(plateau):
    taille = len(plateau)
    cellules_vides = [(i, j) for i in range(taille) for j in range(taille) if plateau[i][j] == 0]
    if cellules_vides:
        i, j = random.choice(cellules_vides)
        plateau[i][j] = 2 if random.random() < 0.9 else 4

def peut_deplacer_direction(plateau, direction):
    def deplacement_possible(plateau):
        taille = len(plateau)
        for i in range(taille):
            for j in range(taille):
                if plateau[i][j] == 0:
                    return True
                if i < taille - 1 and plateau[i][j] == plateau[i + 1][j]:
                    return True
                if j < taille - 1 and plateau[i][j] == plateau[i][j + 1]:
                    return True
        return False

    nouveau_plateau = deplacer(plateau, direction)
    return nouveau_plateau != plateau

def afficher_plateau(plateau, score):
    taille = len(plateau)
    print("-" * (taille * 5 + 1))
    for ligne in plateau:
        print("|" + "|".join(f"{num:4}" if num != 0 else "    " for num in ligne) + "|")
        print("-" * (taille * 5 + 1))
    print(f"Score: {score}")
    print("Déplacements possibles:", end=" ")
    if peut_deplacer_direction(plateau, 'up'):
        print("haut", end=" ")
    if peut_deplacer_direction(plateau, 'down'):
        print("bas", end=" ")
    if peut_deplacer_direction(plateau, 'left'):
        print("gauche", end=" ")
    if peut_deplacer_direction(plateau, 'right'):
        print("droite", end=" ")
    print()

def deplacer(plateau, direction):
    def glisser(ligne):
        nouvelle_ligne = [num for num in ligne if num != 0]
        nouvelle_ligne += [0] * (len(ligne) - len(nouvelle_ligne))
        return nouvelle_ligne

    def combiner(ligne):
        for i in range(len(ligne) - 1):
            if ligne[i] == ligne[i + 1] and ligne[i] != 0:
                ligne[i] *= 2
                ligne[i + 1] = 0
        return ligne

    tourne = False
    if direction in ('up', 'down'):
        plateau = [list(ligne) for ligne in zip(*plateau)]
        tourne = True

    if direction in ('down', 'right'):
        plateau = [ligne[::-1] for ligne in plateau]

    nouveau_plateau = []
    for ligne in plateau:
        nouvelle_ligne = glisser(combiner(glisser(ligne)))
        nouveau_plateau.append(nouvelle_ligne)

    if direction in ('down', 'right'):
        nouveau_plateau = [ligne[::-1] for ligne in nouveau_plateau]

    if tourne:
        nouveau_plateau = [list(ligne) for ligne in zip(*nouveau_plateau)]

    return nouveau_plateau

def peut_deplacer(plateau):
    taille = len(plateau)
    for i in range(taille):
        for j in range(taille):
            if plateau[i][j] == 0:
                return True
            if i < taille - 1 and plateau[i][j] == plateau[i + 1][j]:
                return True
            if j < taille - 1 and plateau[i][j] == plateau[i][j + 1]:
                return True
    return False

def main():
    taille = int(input("Choisissez la taille de la grille (par exemple, 4 pour une grille 4x4): "))
    plateau = init_plateau(taille)
    score = 0

    afficher_plateau(plateau, score)

    while True:
        if keyboard.is_pressed('up'):
            direction_deplacement = 'up'
        elif keyboard.is_pressed('down'):
            direction_deplacement = 'down'
        elif keyboard.is_pressed('left'):
            direction_deplacement = 'left'
        elif keyboard.is_pressed('right'):
            direction_deplacement = 'right'
        else:
            continue

        nouveau_plateau = deplacer(plateau, direction_deplacement)
        
        if nouveau_plateau != plateau:
            ajouter_nouvelle_tuile(nouveau_plateau)
            score += sum(sum(nouveau_plateau[i][j] - plateau[i][j] for j in range(taille)) for i in range(taille))
            plateau = nouveau_plateau
        
        afficher_plateau(plateau, score)
        
        if not peut_deplacer(plateau):
            print("Game Over! Votre score final est:", score)
            break

if __name__ == "__main__":
    main()