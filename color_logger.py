import logging

class CustomFormatter(logging.Formatter):
    pre = "\x1b"
    grey = pre + "[38;20m"
    yellow = pre + "[33;20m"
    red = pre + "[31;20m"
    bold_red = pre + "[31;1m"
    green = pre + "[32;1m"
    reset = pre + "\x1b[0m"



    format = "%(message)s"


    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }


    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)