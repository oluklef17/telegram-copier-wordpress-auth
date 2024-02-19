# Required packages: PyQt5, requests, PyJWT, psycopg2-binary, keyring
import sys
import requests
import psycopg2
import uuid
import jwt
from datetime import datetime, timedelta
import keyring
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer

# Configuration placeholders
DATABASE_CONFIG = {"dbname": "yourdbname", "user": "youruser", "password": "yourpassword", "host": "localhost"}
WORDPRESS_AUTH_URL = "https://yourwordpresssite.com/wp-json/jwt-auth/v1/token"
WORDPRESS_REFRESH_URL = "https://yourwordpresssite.com/wp-json/jwt-auth/v1/token/refresh"
SERVICE_NAME = 'MyAppService'
ACCOUNT_NAME = 'UserJWT'

# Helper Functions
def save_jwt_token(token):
    keyring.set_password(SERVICE_NAME, ACCOUNT_NAME, token)

def get_jwt_token():
    return keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)

def clear_jwt_token():
    keyring.delete_password(SERVICE_NAME, ACCOUNT_NAME)

def create_user_session(username, jwt_token):
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    session_id = str(uuid.uuid4())
    cur.execute("DELETE FROM user_sessions WHERE username = %s", (username,))
    cur.execute("INSERT INTO user_sessions (session_id, username, jwt_token, is_active) VALUES (%s, %s, %s, TRUE)",
                (session_id, username, jwt_token))
    conn.commit()
    cur.close()
    conn.close()

def refresh_token(token):
    response = requests.post(WORDPRESS_REFRESH_URL, json={"JWT": token})
    if response.status_code == 200 and 'data' in response.json() and 'jwt' in response.json()['data']:
        return response.json()['data']['jwt']
    return None

# Login GUI
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 280, 120)
        self.setupUI()

    def setupUI(self):
        self.layout = QVBoxLayout()
        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Username")
        self.layout.addWidget(self.usernameInput)

        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Password")
        self.layout.addWidget(self.passwordInput)

        loginButton = QPushButton("Login")
        loginButton.clicked.connect(self.authenticate)
        self.layout.addWidget(loginButton)
        self.setLayout(self.layout)

    def authenticate(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        response = requests.post(WORDPRESS_AUTH_URL, json={"username": username, "password": password})
        if response.status_code == 200 and response.json().get('success'):
            jwt_token = response.json()['data']['token']
            save_jwt_token(jwt_token)
            create_user_session(username, jwt_token)
            self.openBotGUI()
        else:
            QMessageBox.warning(self, "Login Failed", "Authentication failed.")

    def openBotGUI(self):
        self.bot_window = BotWindow()
        self.bot_window.show()
        self.close()

# Bot GUI with Logout and Token Refresh
class BotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Interface")
        self.setGeometry(100, 100, 320, 200)
        self.jwt_token = get_jwt_token()
        self.setupUI()
        self.initTokenRefreshTimer()

    def setupUI(self):
        self.layout = QVBoxLayout()
        infoLabel = QLabel("You're logged into the Bot.")
        self.layout.addWidget(infoLabel)

        logoutButton = QPushButton("Logout")
        logoutButton.clicked.connect(self.logoutUser)
        self.layout.addWidget(logoutButton)
        self.setLayout(self.layout)

    def initTokenRefreshTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refreshTokenIfNeeded)
        self.timer.start(1500000)  # 25 minutes in milliseconds

    def refreshTokenIfNeeded(self):
        token = get_jwt_token()
        if not token:
            self.promptForReAuthentication()
            return

        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            exp = datetime.utcfromtimestamp(payload['exp'])
            if datetime.utcnow() + timedelta(minutes=5) >= exp:
                new_token = refresh_token(token)
                if new_token:
                    save_jwt_token(new_token)
                    print("Token successfully refreshed.")
                else:
                    self.promptForReAuthentication()
        except Exception as e:
            print(f"Error during token refresh: {e}")
            self.promptForReAuthentication()

    def logoutUser(self):
        clear_jwt_token()
        QMessageBox.information(self, "Logout", "You have been logged out.")
        self.close()
        login_window = LoginWindow()
        login_window.show()

    def promptForReAuthentication(self):
        clear_jwt_token()
        QMessageBox.warning(self, "Session Expired", "Please log in again.")
        self.close()
        login_window = LoginWindow()
        login_window.show()

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()





Enhanced Error Handling and Logging

let's introduce logging and improve error handling. Python's built-in logging module can facilitate this:


import logging

# Configure logging at the start of your application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Example usage within your application
try:
    # Potentially risky operation
except Exception as e:
    logging.error("An error occurred: %s", e)
    QMessageBox.critical(None, "Error", "An unexpected error occurred.")
	
	
	
Dynamic Token Refresh Intervals
Adjust the token refresh logic to dynamically set intervals based on the token's expiration time. This involves decoding the JWT to extract the expiration time:

python
Copy code
def initTokenRefreshTimer(self):
    token = get_jwt_token()
    if token:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp = datetime.utcfromtimestamp(payload['exp'])
        now = datetime.utcnow()
        seconds_until_exp = (exp - now).total_seconds()
        
        # Refresh the token 5 minutes (300 seconds) before it expires
        refresh_interval = max(0, seconds_until_exp - 300) * 1000  # QTimer expects milliseconds
        self.timer.start(refresh_interval)
    else:
        logging.warning("No token available for setting refresh timer.")


Refresh Token Handling
Assuming the system uses refresh tokens (which wasn't specified earlier), you'd typically receive a refresh token alongside the access token during authentication. Here's a conceptual approach:

python
Copy code
def save_refresh_token(token):
    keyring.set_password(SERVICE_NAME, "UserRefreshToken", token)

def get_refresh_token():
    return keyring.get_password(SERVICE_NAME, "UserRefreshToken")

def clear_refresh_token():
    keyring.delete_password(SERVICE_NAME, "UserRefreshToken")

# Modify your authentication and token refresh logic to handle and use refresh tokens.



Checking for updates against a PostgreSQL database and launching an external updater

import sys
import requests
import psycopg2
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer
import subprocess
import tempfile
import hashlib

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Application and Database Configuration
CURRENT_APP_VERSION = "1.0"
DATABASE_CONFIG = {
    "dbname": "exampledb", "user": "exampleuser", "password": "examplepass", "host": "examplehost"
}
UPDATE_SERVER_URL = "https://example.com/version.json"

class BotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Interface")
        self.setGeometry(100, 100, 320, 200)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        updateButton = QPushButton("Check for Updates")
        updateButton.clicked.connect(self.check_for_updates)
        layout.addWidget(updateButton)

        self.setLayout(layout)

    def check_for_updates(self):
        logging.info("Checking for updates...")
        # Check for the latest version information from the database
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT version, url, checksum FROM app_versions ORDER BY release_date DESC LIMIT 1")
        latest_version_info = cur.fetchone()
        cur.close()
        conn.close()

        if latest_version_info:
            latest_version, url, expected_checksum = latest_version_info
            if latest_version > CURRENT_APP_VERSION:
                reply = QMessageBox.question(self, 'Update Available',
                                             "An update is available. Would you like to download and install it now?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.download_and_update(url, expected_checksum)

    def download_and_update(self, url, expected_checksum):
        # Placeholder: Download the update and verify its checksum
        # If verified, launch the external updater script
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        response = requests.get(url)
        temp_file.write(response.content)
        temp_file.close()
        
        if self.verify_checksum(temp_file.name, expected_checksum):
            subprocess.Popen(['python', 'updater.py', sys.executable, temp_file.name])
            QApplication.quit()
        else:
            QMessageBox.warning(self, "Update Failed", "The update could not be verified.")

    def verify_checksum(self, file_path, expected_checksum):
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest() == expected_checksum

def main():
    app = QApplication(sys.argv)
    window = BotWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


External Updater Script (updater.py)
This script is called by the main application to replace the current executable with the downloaded update.

# updater.py
import sys
import time
import shutil
import os

def apply_update(current_app_path, update_file_path):
    time.sleep(5)  # Wait for the main application to close
    try:
        os.remove(current_app_path)  # Remove the current executable
        shutil.move(update_file_path, current_app_path)  # Move the new update to the application path
        # Optionally, restart the application here
    except Exception as e:
        print(f"Failed to apply update: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        apply_update(sys.argv[1], sys.argv[2])
    else:
        print("Usage: updater.py <current_app_path> <update_file_path>")


Modified Script with Refresh Token Handling

import sys
import requests
import psycopg2
import logging
import jwt
from datetime import datetime, timedelta
import keyring
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Application and Database Configuration with example values
DATABASE_CONFIG = {
    "dbname": "exampledb", "user": "exampleuser", "password": "examplepass", "host": "localhost"
}
WORDPRESS_AUTH_URL = "https://yourwordpresssite.com/wp-json/jwt-auth/v1/token"
WORDPRESS_REFRESH_URL = "https://yourwordpresssite.com/wp-json/jwt-auth/v1/token/refresh"
SERVICE_NAME = 'MyAppService'
ACCOUNT_NAME = 'UserJWT'
REFRESH_TOKEN_ACCOUNT = 'UserRefreshToken'

def save_jwt_token(token):
    keyring.set_password(SERVICE_NAME, ACCOUNT_NAME, token)

def get_jwt_token():
    return keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)

def clear_jwt_token():
    keyring.delete_password(SERVICE_NAME, ACCOUNT_NAME)

def save_refresh_token(token):
    keyring.set_password(SERVICE_NAME, REFRESH_TOKEN_ACCOUNT, token)

def get_refresh_token():
    return keyring.get_password(SERVICE_NAME, REFRESH_TOKEN_ACCOUNT)

def clear_refresh_token():
    keyring.delete_password(SERVICE_NAME, REFRESH_TOKEN_ACCOUNT)

# Login GUI
class LoginWindow(QWidget):
    # Initialization and UI setup
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 280, 120)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Username")
        layout.addWidget(self.usernameInput)

        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Password")
        layout.addWidget(self.passwordInput)

        loginButton = QPushButton("Login")
        loginButton.clicked.connect(self.authenticate)
        layout.addWidget(loginButton)
        self.setLayout(layout)

    def authenticate(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        response = requests.post(WORDPRESS_AUTH_URL, json={"username": username, "password": password})
        if response.status_code == 200 and 'data' in response.json():
            access_token = response.json()['data'].get('token')
            refresh_token = response.json()['data'].get('refresh_token')  # Assuming this key is correct
            if access_token and refresh_token:
                save_jwt_token(access_token)
                save_refresh_token(refresh_token)
                QMessageBox.information(self, "Success", "Login successful.")
                self.openBotGUI()
            else:
                QMessageBox.warning(self, "Login Failed", "Missing tokens in response.")
        else:
            QMessageBox.warning(self, "Login Failed", "Authentication failed.")

    def openBotGUI(self):
        self.bot_window = BotWindow()
        self.bot_window.show()
        self.close()

# Bot GUI with Logout and Token Refresh
class BotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Interface")
        self.setGeometry(100, 100, 320, 200)
        self.setupUI()
        self.initTokenRefreshTimer()

    def setupUI(self):
        layout = QVBoxLayout()
        infoLabel = QLabel("You're logged into the Bot.")
        layout.addWidget(infoLabel)

        logoutButton = QPushButton("Logout")
        logoutButton.clicked.connect(self.logoutUser)
        layout.addWidget(logoutButton)
        self.setLayout(layout)

    def initTokenRefreshTimer(self):
        # Initialize token refresh checking
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refreshTokenIfNeeded)
        self.timer.start(1800000)  # Check every 30 minutes

    def refreshTokenIfNeeded(self):
        refresh_token = get_refresh_token()
        if refresh_token:
            response = requests.post(WORDPRESS_REFRESH_URL, json={"refresh_token": refresh_token})
            if response.status_code == 200 and 'data' in response.json():
                new_access_token = response.json()['data'].get('token')
                new_refresh_token = response.json()['data'].get('refresh_token')  # If a new one is provided
                if new_access_token:
                    save_jwt_token(new_access_token)
                    if new_refresh_token:
                        save_refresh_token(new_refresh_token)  # Update refresh token if a new one is given
                    logging.info("Access token refreshed successfully.")
                else:
                    self.promptForReAuthentication()
            else:
                logging.warning("Failed to refresh access token.")
                self.promptForReAuthentication()
        else:
            self.promptForReAuthentication()

    def logoutUser(self):
        clear_jwt_token()
        clear_refresh_token()
        QMessageBox.information(self, "Logout", "You have been logged out.")
        QApplication.quit()

    def promptForReAuthentication(self):
        clear_jwt_token()
        clear_refresh_token()
        QMessageBox.warning(self, "Session Expired", "Please log in again.")
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


Code Snippet for your help

import sys
import requests
import psycopg2
import logging
import uuid
from datetime import datetime, timedelta
import keyring
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QTimer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Application and Database Configuration
DATABASE_CONFIG = {
    "dbname": "yourdbname", 
    "user": "youruser", 
    "password": "yourpassword", 
    "host": "localhost"
}
WORDPRESS_AUTH_URL = "https://yourwordpresssite.com/wp-json/jwt-auth/v1/token"
WORDPRESS_REFRESH_URL = "https://yourwordpresssite.com/wp-json/jwt-auth/v1/token/refresh"
SERVICE_NAME = 'MyAppService'
ACCOUNT_NAME = 'UserJWT'
REFRESH_TOKEN_ACCOUNT = 'UserRefreshToken'

# Helper Functions
def save_jwt_token(token):
    keyring.set_password(SERVICE_NAME, ACCOUNT_NAME, token)

def get_jwt_token():
    return keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)

def clear_jwt_token():
    keyring.delete_password(SERVICE_NAME, ACCOUNT_NAME)

def save_refresh_token(token):
    keyring.set_password(SERVICE_NAME, REFRESH_TOKEN_ACCOUNT, token)

def get_refresh_token():
    return keyring.get_password(SERVICE_NAME, REFRESH_TOKEN_ACCOUNT)

def clear_refresh_token():
    keyring.delete_password(SERVICE_NAME, REFRESH_TOKEN_ACCOUNT)

def create_user_session(username, jwt_token):
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        with conn.cursor() as cur:
            session_id = str(uuid.uuid4())
            cur.execute("DELETE FROM user_sessions WHERE username = %s", (username,))
            cur.execute("""
                INSERT INTO user_sessions (session_id, username, jwt_token, is_active)
                VALUES (%s, %s, %s, TRUE)
                """, (session_id, username, jwt_token))

def refresh_token_logic():
    refresh_token = get_refresh_token()
    if not refresh_token:
        logging.warning("No refresh token available.")
        return False

    response = requests.post(WORDPRESS_REFRESH_URL, json={"refresh_token": refresh_token})
    if response.status_code == 200 and 'data' in response.json():
        new_access_token = response.json()['data'].get('jwt')
        new_refresh_token = response.json()['data'].get('refresh_token', refresh_token)  # Use new if provided
        save_jwt_token(new_access_token)
        save_refresh_token(new_refresh_token)
        logging.info("Token successfully refreshed.")
        return True
    else:
        logging.error("Failed to refresh token.")
        return False

# UI Classes
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 280, 120)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Username")
        layout.addWidget(self.usernameInput)
        
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Password")
        layout.addWidget(self.passwordInput)
        
        loginButton = QPushButton("Login")
        loginButton.clicked.connect(self.authenticate)
        layout.addWidget(loginButton)
        
        self.setLayout(layout)

    def authenticate(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        response = requests.post(WORDPRESS_AUTH_URL, json={"username": username, "password": password})
        if response.status_code == 200 and 'data' in response.json():
            jwt_token = response.json()['data'].get('token')
            refresh_token = response.json()['data'].get('refresh_token')
            if jwt_token and refresh_token:
                save_jwt_token(jwt_token)
                save_refresh_token(refresh_token)
                QMessageBox.information(self, "Success", "Login successful.")
                self.openBotGUI()
            else:
                QMessageBox.warning(self, "Login Failed", "Authentication failed.")
        else:
            QMessageBox.warning(self, "Login Failed", "Authentication failed.")

    def openBotGUI(self):
        self.bot_window = BotWindow()
        self.bot_window.show()
        self.close()

class BotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Interface")
        self.setGeometry(100, 100, 320, 200)
        self.setupUI()
        self.initTokenRefreshTimer()

    def setupUI(self):
        layout = QVBoxLayout()
        
        infoLabel = QLabel("You're logged into the Bot.")
        layout.addWidget(infoLabel)
        
        logoutButton = QPushButton("Logout")
        logoutButton.clicked.connect(self.logoutUser)
        layout.addWidget(logoutButton)
        
        self.setLayout(layout)

    def initTokenRefreshTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refreshTokenIfNeeded)
        # Adjust interval as needed
        self.timer.start(1500000)  # 25 minutes

    def refreshTokenIfNeeded(self):
        if not refresh_token_logic():
            self.promptForReAuthentication()

    def logoutUser(self):
        clear_jwt_token()
        clear_refresh_token()
        QMessageBox.information(self, "Logout", "You have been successfully logged out.")
        self.close()
        QApplication.quit()

    def promptForReAuthentication(self):
        QMessageBox.warning(self, "Session Expired", "Please log in again.")
        self.close()
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



################################################

FULL PyQt5 Application with Updoate Mechanism

################################################

import sys
import requests
import psycopg2
import logging
import jwt
from datetime import datetime, timedelta
import keyring
import hashlib
import os
import subprocess
import tempfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Application and Database Configuration
CURRENT_APP_VERSION = "1.0"
DATABASE_CONFIG = {
    "dbname": "exampledb", "user": "exampleuser", "password": "examplepass", "host": "examplehost"
}
WORDPRESS_AUTH_URL = "https://example.com/wp-json/jwt-auth/v1/token"
WORDPRESS_REFRESH_URL = "https://example.com/wp-json/jwt-auth/v1/token/refresh"
SERVICE_NAME = 'MyAppService'
ACCOUNT_NAME = 'UserJWT'
REFRESH_TOKEN_ACCOUNT = 'UserRefreshToken'  # For refresh token handling

# Helper Functions
def save_jwt_token(token):
    keyring.set_password(SERVICE_NAME, ACCOUNT_NAME, token)

def get_jwt_token():
    return keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)

def clear_jwt_token():
    keyring.delete_password(SERVICE_NAME, ACCOUNT_NAME)

def save_refresh_token(token):
    keyring.set_password(SERVICE_NAME, REFRESH_TOKEN_ACCOUNT, token)

def get_refresh_token():
    return keyring.get_password(SERVICE_NAME, REFRESH_TOKEN_ACCOUNT)

def clear_refresh_token():
    keyring.delete_password(SERVICE_NAME, REFRESH_TOKEN_ACCOUNT)

def create_user_session(username, jwt_token):
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        with conn.cursor() as cur:
            session_id = str(uuid.uuid4())
            cur.execute("DELETE FROM user_sessions WHERE username = %s", (username,))
            cur.execute("""
                INSERT INTO user_sessions (session_id, username, jwt_token, is_active)
                VALUES (%s, %s, %s, TRUE)
                """, (session_id, username, jwt_token))

def refresh_token_logic():
    refresh_token = get_refresh_token()
    if not refresh_token:
        logging.warning("No refresh token available.")
        return False

    response = requests.post(WORDPRESS_REFRESH_URL, json={"refresh_token": refresh_token})
    if response.status_code == 200 and 'data' in response.json():
        new_access_token = response.json()['data'].get('jwt')
        new_refresh_token = response.json()['data'].get('refresh_token', refresh_token)  # Use new if provided
        save_jwt_token(new_access_token)
        save_refresh_token(new_refresh_token)
        logging.info("Token successfully refreshed.")
        return True
    else:
        logging.error("Failed to refresh token.")
        return False

# UI Classes
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 280, 120)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        
        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Username")
        layout.addWidget(self.usernameInput)
        
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setPlaceholderText("Password")
        layout.addWidget(self.passwordInput)
        
        loginButton = QPushButton("Login")
        loginButton.clicked.connect(self.authenticate)
        layout.addWidget(loginButton)
        
        self.setLayout(layout)

    def authenticate(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        response = requests.post(WORDPRESS_AUTH_URL, json={"username": username, "password": password})
        if response.status_code == 200 and 'data' in response.json():
            jwt_token = response.json()['data'].get('token')
            refresh_token = response.json()['data'].get('refresh_token')
            if jwt_token and refresh_token:
                save_jwt_token(jwt_token)
                save_refresh_token(refresh_token)
                QMessageBox.information(self, "Success", "Login successful.")
                self.openBotGUI()
            else:
                QMessageBox.warning(self, "Login Failed", "Authentication failed.")
        else:
            QMessageBox.warning(self, "Login Failed", "Authentication failed.")

    def openBotGUI(self):
        self.bot_window = BotWindow()
        self.bot_window.show()
        self.close()

class BotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Interface")
        self.setGeometry(100, 100, 320, 200)
        self.setupUI()
        self.initTokenRefreshTimer()


class LoginWindow(QWidget):
    # Initialization and UI setup as before
    def authenticate(self):
        # Authentication logic as before

class BotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Interface")
        self.setGeometry(100, 100, 320, 200)
        self.jwt_token = get_jwt_token()
        self.setupUI()
        self.initTokenRefreshTimer()

    def setupUI(self):
        # UI setup, including the update button as before

    def initTokenRefreshTimer(self):
        # Dynamic token refresh intervals as before

    def refreshTokenIfNeeded(self):
        # Refresh token logic as before, including handling for refresh tokens

    def check_for_updates(self):
        # Checking for updates against PostgreSQL and launching external updater as before

    def download_and_update(self, url, expected_checksum):
        # Download and update logic as before

    def verify_checksum(self, file_path, expected_checksum):
        # Checksum verification as before

    def logoutUser(self):
        # Logout logic as before

    def promptForReAuthentication(self):
        # Re-authentication prompting as before

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()  # Start with the LoginWindow
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
