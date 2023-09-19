import requests
import datetime

from .db import MySQLDatabase

class SofaScoreController:
    def __init__(self) -> None:
        self.mysql = MySQLDatabase(
            host='db-fcjuarez-prod.c3qcmhxp5nh5.us-east-1.rds.amazonaws.com', 
            user='kevinro', 
            password='3qynqhj4hST6Ei', 
            port='3306',
            database='db_deportivo'
        )
        
        self.mysql.connect()


    def get_partidos(self):
        url = "https://api.sofascore.com/api/v1/sport/football/events/live"  # Reemplaza esto con la URL real de tu API

    # Definir el agente de usuario de Firefox
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            eventos = data["events"]
            return eventos
        else:
            print("Error al realizar la solicitud a la API. Código de estado:", response.status_code)

    def insert_partidos(self):
        data = self.get_partidos()
        for record in data:
            if record['tournament']['name'] == 'Liga MX, Apertura' and (record['homeTeam']['name'] == 'Juárez FC' or record['awayTeam']['name'] == 'Juárez FC'):
                query = "INSERT INTO PARTIDOS (homeTeam, awayTeam, homeScore, awayScore, startTimeStamp) VALUES (%s, %s, %s, %s, %s)"
                print(record['startTimestamp'])
                data_to_insert = (
                    record['homeTeam']['name'], 
                    record['awayTeam']['name'], 
                    record['homeScore']['current'], 
                    record['awayScore']['current'], 
                    datetime.datetime.utcfromtimestamp(record['startTimestamp']).strftime('%Y-%m-%d %H:%M:%S')
                )
                self.mysql.execute_query(query, data_to_insert)

                return data_to_insert


        return 'No Query executed'

