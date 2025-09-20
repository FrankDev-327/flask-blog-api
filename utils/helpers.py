from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Helper:
    def __init__(self):
       pass
        
    def hashingTextToHash(self, plainText):
        return bcrypt.generate_password_hash(plainText, 10).decode("utf-8")
    
    def compareHashAndPlainText(self, plainText, hashText):
        return bcrypt.check_password_hash(hashText, plainText)
    
    def formatting_time(self, timeToBeFormatted, formatTime):
        return timeToBeFormatted.strftime(formatTime)