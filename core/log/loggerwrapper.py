import logging

class LoggerWrapper:

    def __init__(self, level=logging.INFO):
        
        self.logger = logging.getLogger("iceBreaker")
        self.logger.setLevel(level)
        self.level = level

        formatter = logging.Formatter(f"%(asctime)s %(name)s %(levelname)s %(message)s")

        handlerFile = logging.FileHandler("log-jailbreak", mode='w')
        handlerFile.setFormatter(formatter)

        handlerConsole = logging.StreamHandler()
        handlerConsole.setFormatter(formatter)

        self.logger.addHandler(handlerFile)
        self.logger.addHandler(handlerConsole)

    def __call__(self, message):
        self.logger.log(self.level, message)
