from loguru import logger


class Logger:
    """
    A class that provides the ability to log errors that occur in the program.
    Used by: Loguru.
    """

    logger = logger

    def __init__(
        self,
        level: str = 'DEBUG',
        format: str = '{time} {level} {message}',
        rotation: str = '100 MB',
    ):
        self.logger.add(
            'logs/debug.log',
            format=format,
            level=level,
            rotation=rotation,
            compression='zip',
        )

    def get_logger(self):
        return self.logger


logger = Logger().get_logger()
