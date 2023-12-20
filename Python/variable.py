displayType = [
    "NUM", #En nombre
    "BAR", #Sous forme de barre
    "INV", #Invisible
    "PR%"  #En Pourcent
]

displayType_descript = [
    "Montre la statistique sous la forme d'un simple numéro",
    "Montre la statistique sous la forme d'une barre, statistique double",
    "La statistique n'est pas montré",
    "Montre la statistique sous la forme d'un pourcentage"
]

displayType_Desig = [
    "Numéro",
    "Barre",
    "invisible",
    "Pourcentage"
]

StatType = [
    "SPL", #Simple
    "CAL", #Calculé a partir d'autre statistique
    "XPE", #de type expérience
    "VIT" #barre vitale exemple : pv, mana, endurance, etc, Est calculé
    
]

StatType_descript = [
    "Statistique simple, définie qui peu être augmenter ou diminuer de manière simple",
    "Statistique Caluler grace a d'autre statistique, permettant ainsi de réaliséer des systeme plus complexe",
    "Statistique d'expérience, ne peu pas diminuer, peu avoir plusieurs utilisation",
    "Statistique vitale, c'est une barre de vie, forcément calculé cette stat permet de gérer l'état d'un personage, au moins une stat vitale est requise."
    
]

StatType_Desig = [
    "Simple",
    "Calculer",
    "Expérience",
    "Vitale"
]

CibleList = [
    "PYR", #Player
    "OBJ", #Objet
    "MON", #Hostile
    "DJN", #Donjon
    "ALA", #Player + Hostile
    "ALB", #Player + Hostile + Objet
    "ALC" #Player + Objet
]

CibleList_Desig = [
    "Player",
    "Objet",
    "Hostile",
    "Donjon",
    "Player/Hostile",
    "Player/Hostile/Objet",
    "Player/Objet"
]

CibleList_descript = [
    "Peut être attribuer a un Player",
    "Peut être attribuer a un Objet",
    "Peut être attribuer a un Hostile",
    "Peut être attribuer a un Donjon",
    "Peut être attribuer a un Player ou un Hostile",
    "Peut être attribuer a un Player, un Hostile ou un Objet",
    "Peut être attribuer a un Player ou un Objet"
]