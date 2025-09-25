import re
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

bcrypt = Bcrypt()
MENTION_REGEX = r"@([a-zA-Z0-9_]+)"

class Helper:
    def __init__(self):
       pass
        
    def hashingTextToHash(self, plainText):
        return bcrypt.generate_password_hash(plainText, 10).decode("utf-8")
    
    def compareHashAndPlainText(self, plainText, hashText):
        return bcrypt.check_password_hash(hashText, plainText)
    
    def formatting_time(self, timeToBeFormatted= "", formatTime="", action=""):
        if action == "subs_time":
            current_date = datetime.now()
            dateTime = (current_date - timedelta(days=15)).strftime(formatTime)
        elif action == "add_time":
            dateTime = (current_date + timedelta(days=3)).strftime(formatTime)
        else:
            dateTime = timeToBeFormatted.strftime(formatTime)
        return dateTime
    
    def extract_mentions_from_content(self, text):
        return re.findall(MENTION_REGEX, text)
    
    