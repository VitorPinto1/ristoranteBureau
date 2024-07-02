import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


config = {
    'host': os.getenv('MYSQL_DATABASE_HOST'),
    'port': os.getenv('MYSQL_DATABASE_PORT'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

def total_reservations():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "SELECT id, name, totalPerson, day, time, email FROM reservation"
    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def delete_reservation(reservation_id):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "DELETE FROM reservation WHERE id = %s"
    cursor.execute(query, (reservation_id,))
    conn.commit()

    cursor.close()
    conn.close()

def update_reservation_date(reservation_id, new_date):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "UPDATE reservation SET day = %s WHERE id = %s"
    cursor.execute(query, (new_date, reservation_id))
    conn.commit()

    cursor.close()
    conn.close()

def update_reservation_time(reservation_id, new_time):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "UPDATE reservation SET time = %s WHERE id = %s"
    cursor.execute(query, (new_time, reservation_id))
    conn.commit()

    cursor.close()
    conn.close()
