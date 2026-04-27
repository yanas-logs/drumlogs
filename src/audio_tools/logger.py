import logging
import os

class AudioLogger:
    def __init__(self, log_file="drumlogs.log"):
        self.logger = logging.getLogger("DrumLogs")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)
