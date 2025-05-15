import logging

class LoggerSingl:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerSingl, cls).__new__(cls)
            # Initialize the logger
            cls._instance.log = cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # Avoid duplicate handlers
        if not logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handlerFile = logging.FileHandler("log-jailbreak", mode='w')
            handlerFile.setFormatter(formatter)
            #
            handlerConsole = logging.StreamHandler()
            handlerConsole.setFormatter(formatter)

            handlerFile.setFormatter(formatter)
            handlerConsole.setFormatter(formatter)

            logger.addHandler(handlerFile)
            logger.addHandler(handlerConsole)

        return logger