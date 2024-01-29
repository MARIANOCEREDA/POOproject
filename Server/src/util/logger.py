import logging

# Configure the logging settings
formatter = logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum level of messages to log
    format="%(asctime)s - %(name)s - [%(levelname)s]: %(message)s",  # Define the log message format
    datefmt="%Y-%m-%d %H:%M:%S"  # Define the date/time format
)


def get_logger(name):
    
    logger = logging.getLogger(name)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    # Set the log level
    logger.setLevel(logging.DEBUG)

    return logger