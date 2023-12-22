
#STATISTIQUE VARIABLE
#TYPE  DISPLAY :

displayType = [
    "NUM", #En nombre
    "BAR", #Sous forme de barre
    "INV", #Invisible
    "PR%"  #En Pourcent
]

displayType_descript = {
   "NUM" : "Montre la statistique sous la forme d'un simple numéro",
   "BAR" : "Montre la statistique sous la forme d'une barre, statistique double",
   "INV" : "La statistique n'est pas montré",
   "PR%" : "Montre la statistique sous la forme d'un pourcentage"
}

displayType_Desig = {
    "NUM" : "Numéro",
    "BAR" : "Barre",
    "INV" : "invisible",
    "PR%" : "Pourcentage"
}

#TYPE STATISTIQUE

StatType = [
    "SPL", #Simple
    "CAL", #Calculé a partir d'autre statistique
    "XPE", #de type expérience
    "VIT" #barre vitale exemple : pv, mana, endurance, etc, Est calculé
    
]

StatType_descript = {
    "SPL" : "Statistique simple, définie qui peu être augmenter ou diminuer de manière simple",
    "CAL" : "Statistique Caluler grace a d'autre statistique, permettant ainsi de réaliséer des systeme plus complexe",
    "XPE" : "Statistique d'expérience, ne peu pas diminuer, peu avoir plusieurs utilisation",
    "VIT" : "Statistique vitale, c'est une barre de vie, forcément calculé cette stat permet de gérer l'état d'un personage, au moins une stat vitale est requise."
    
}

StatType_Desig = {
   "SPL" : "Simple",
   "CAL" : "Calculer",
   "XPE" : "Expérience",
   "VIT" : "Vitale"
}

#TYPE AFFECTATION STATISTIQUE/EFFECT

CibleList = [
    "PYR", #Player
    "OBJ", #Objet
    "MON", #Hostile
    "DJN", #Donjon
    "ALA", #Player + Hostile
    "ALB", #Player + Hostile + Objet
    "ALC" #Player + Objet
]

CibleList_Desig = {
    "PYR" : "Player",
    "OBJ" : "Objet",
    "MON" : "Hostile",
    "DJN" : "Donjon",
    "ALA" : "Player/Hostile",
    "ALB" : "Player/Hostile/Objet",
    "ALC" : "Player/Objet"
}

CibleList_descript = {
    "PYR" : "Peut être attribuer a un Player",
    "OBJ" : "Peut être attribuer a un Objet",
    "MON" : "Peut être attribuer a un Hostile",
    "DJN" : "Peut être attribuer a un Donjon",
    "ALA" : "Peut être attribuer a un Player ou un Hostile",
    "ALB" : "Peut être attribuer a un Player, un Hostile ou un Objet",
    "ALC" : "Peut être attribuer a un Player ou un Objet"
}

#EFFECT VARIABLE

EffectType = [
    "BUF", #Buff
    "UNI", #Instant Effect
    "BRN"  #Multi Turn Effect
]

EffectType_Desig = {
    "BUF" : "Buff",
    "UNI" : "Instant Effect", 
    "BRN" : "Multi Turn Effect"
}

EffectType_descript = {
    "BUF" : "Effet de Buff, affecte les statistique d'un personnage, durée variable", 
    "UNI" : "Effet instantané, Si les effet sont activé sur le serveur, la moindre action affectant les statistique VIT passera part les effets instantané, ou les effet multi Tours", 
    "BRN" : "Effet Multi Tour, cet effet est appliqué sur de multiple tour a un moment précis, Avant le tour, pendant le tour, Apres le tour"
}

# EFFECT BRN TIMER
Effect_BrnTimer = [
    "BFR", #Avant
    "PDT", #Pendant
    "AFT"  #Apres
]

# EFFECT CIBLE
Effect_Cible = [
    "HOS", # Tout Hostile
    "MON", # Cible Actuelle
    "SEL", # Sois Même
    "ALY"  # Tout Allié
]

