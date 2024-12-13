import base64
import random
import logging

COLORS = {
    "HEADER": "\033[95m",
    "INFO": "\033[94m",
    "SUCCESS": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "RESET": "\033[0m",
}

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def color_text(text, color):
    """
    Apply ANSI color codes to text for logging.

    :param text: The text to color.
    :param color: The color key to apply.
    :return: Colored text string.
    """
    return f"{COLORS[color]}{text}{COLORS['RESET']}"

def log_request(message):
    """
    Log a request message.

    :param message: The message to log.
    """
    logger.info(color_text(f"[Request] {message}", "HEADER"))

def log_retrieval(message):
    """
    Log a retrieval message.

    :param message: The message to log.
    """
    logger.info(color_text(f"[Retrieval] {message}", "INFO"))

def log_success(message):
    """
    Log a success message.

    :param message: The message to log.
    """
    logger.info(color_text(f"[Success] {message}", "SUCCESS"))

def log_warning(message):
    """
    Log a warning message.

    :param message: The message to log.
    """
    logger.warning(color_text(f"[Warning] {message}", "WARNING"))

def log_error(message):
    """
    Log an error message.

    :param message: The message to log.
    """
    logger.error(color_text(f"[Error] {message}", "ERROR"))

def encode_base64_image(image_path):
    """
    Convert an image file to a Base64 encoded string.

    :param image_path: Path to the image file.
    :return: Base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_damage_type_label(damage_type_int):
    """
    Convert an integer damage type code to a human-readable label.

    :param damage_type_int: Integer representing the damage type.
    :return: String label for the damage type.
    """
    damage_type_map = {
        0: "longitudinal crack",
        1: "alligator crack",
        2: "transverse crack",
        3: "other corruption",
        4: "pothole"
    }
    return damage_type_map.get(damage_type_int, "unknown")

def generate_random_geo():
    """
    Generate random geographic coordinates within a defined range.

    :return: A string containing "lat,lon".
    """
    lat = random.uniform(36.361, 36.369)
    lon = random.uniform(127.357, 127.370)
    return f"{lat:.6f},{lon:.6f}"
