# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

load_dotenv()

app = Flask(__name__)
CORS(app)

key_vault_name = "mana-kv"
kv_uri = f"https://mana-kv.vault.azure.net/"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=kv_uri, credential=credential)

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/api/projects', methods=['GET'])
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Projects')
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(projects)

if __name__ == '__main__':
    app.run(debug=True)
