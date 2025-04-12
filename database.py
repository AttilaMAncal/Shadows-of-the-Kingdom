import mysql.connector
from mysql.connector import Error


def save_game_data(player_data):
    connection = None
    try:
        #pripojenie k databáze MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="game_data"
        )

        if connection.is_connected():
            cursor = connection.cursor()
            # vytvorenie tabuľku, ak ešte neexistuje
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_save (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    health INT,
                    coins INT,
                    level INT,
                    time FLOAT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            #vloženie herných údajov do tabuľky
            insert_query = """
                INSERT INTO game_save (health, coins, level, time)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                player_data.get("health", 0),
                player_data.get("coins", 0),
                player_data.get("level", 1),
                player_data.get("time", 0)

            ))
            connection.commit()


    except Error as e:
        print(e)

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def get_last_three_saves():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="game_data"
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT level, time, coins, health FROM game_save ORDER BY id DESC LIMIT 3"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Error as e:
        print(e)
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()