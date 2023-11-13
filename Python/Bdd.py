import mysql.connector
import Config

project_Ares_bdd = mysql.connector.connect(
    host=Config.connection_params["host"],
    user=Config.connection_params["user"],
    password=Config.connection_params["password"],
    database=Config.connection_params["database"]
)
