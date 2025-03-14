import logging
import logging.handlers


def setup_logging(log_file="app.log"):
    """
    Set up logging configuration.

    :param log_file: The file to write logs to.
    """
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)

    # Check if handlers are already added to avoid duplicate logs
    if not logger.handlers:
        # Create handlers
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatters and add them to handlers
        formatter = logging.Formatter(
            "[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
