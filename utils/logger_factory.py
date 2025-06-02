import logging

logging.basicConfig(
    level=logging.INFO,  # Global logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log message format
    handlers=[
        logging.StreamHandler(),  # Console output
    ]
)

def get_logger(name: str):
    """Returns a module-specific logger."""
    return logging.getLogger(name)