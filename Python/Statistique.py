import mysql.connector

displayType = [
    "Num", #En nombre
    "Bar", #Sous forme de barre
    "Inv", #Invisible
    "pr%"  #En Pourcent
]

StatType = [
    "Spl", #Simple
    "Cal" #Calculé a partir d'autre statistique
]

CibleList = [
    "Pyr", #Player
    "Obj", #Objet
    "Mon", #Hostile
    "Djn", #Donjon
    "ALA", #Player + Hostile
    "ALB", #Player + Hostile + Objet
]

class Statistique:

    def __init__(self, name, displayType, cible):
        self.Name           = name
        self.Resume         = ""
        self.displayType    = displayType
        self.cible          = cible

