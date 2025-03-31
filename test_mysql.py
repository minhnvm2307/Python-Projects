import requests
import mysql.connector
import json

API_HEADERS = {
    'x-rapidapi-key': '2c6c07fcdfmshd32c1bcc83123c3p151142jsndf4645c399b1',
    'x-rapidapi-host': 'exercisedb.p.rapidapi.com'
}

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ai_fitnessdb'
}

def api_call(url, params=None):
    try:
        response = requests.get(url, headers=API_HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f'Error: {err}')
        return None

def fetch_exercises_bodypart(body_part):
    url = f'https://exercisedb.p.rapidapi.com/exercises/bodyPart/{body_part}'
    params = {'limit': 6}
    return api_call(url, params)

def insert_data_to_mysql(data):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = """
        INSERT INTO exercises (id, name, bodyPart, equipment, target, gifUrl, secondaryMuscles, instructions) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for item in data:
            secondary_muscles = ", ".join(item.get('secondaryMuscles', [])) if isinstance(item.get('secondaryMuscles'), list) else item.get('secondaryMuscles', '')
            instructions = " | ".join(item.get('instructions', [])) if isinstance(item.get('instructions'), list) else item.get('instructions', '')
            
            cursor.execute(query, (
                item['id'], item['name'], item['bodyPart'], item['equipment'], 
                item['target'], item['gifUrl'], secondary_muscles, instructions
            ))
        
        conn.commit()
        print("Data inserted successfully!")
    except mysql.connector.Error as err:
        print(f'Database error: {err}')
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    body_parts = ['cardio', 'lower arms', 'lower legs', 'shoulders', 'upper arms', 'upper legs', 'waist']

    for body_part in body_parts:
        exercises = fetch_exercises_bodypart(body_part)
        
        if exercises:
            insert_data_to_mysql(exercises)
