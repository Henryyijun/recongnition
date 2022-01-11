import logging
from logging import handlers

class MyLogger(object):
    level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):

        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level.get(level))
        if not self.logger.handlers:
            sh = logging.StreamHandler()
            sh.setFormatter(format_str)
            th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                                   encoding='utf-8')
            th.setFormatter(format_str)  # Set the format written in the file
            self.logger.addHandler(sh)  # Add object to logger
            self.logger.addHandler(th)


if __name__ == '__main__':
    log = MyLogger('log.txt')
    log.logger.debug('This is a bug')
    log.logger.info('This is a info')
    log.logger.debug('This is a bug2')

    log2 = MyLogger('log.txt')
    log2.logger.info('This is a another info')