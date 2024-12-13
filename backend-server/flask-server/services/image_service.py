import os
from datetime import datetime
from PIL import Image, ImageDraw
from utils import encode_base64_image, get_damage_type_label
from config import CROPPED_FOLDER


def generate_timestamp():
    """
    Generate a timestamp string.

    :return: A timestamp string in the format YYYYmmdd_HHMMSS.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_original_image(image_file, image_folder, timestamp):
    """
    Save the original uploaded image to the specified folder.

    :param image_file: The uploaded image file.
    :param image_folder: The folder path to save the image.
    :param timestamp: Timestamp string to use in the filename.
    :return: Full path to the saved original image.
    """
    original_image_path = os.path.join(image_folder, f"original_{timestamp}.png")
    image_file.save(original_image_path)
    return original_image_path


def process_image(original_image_path, x1, y1, x2, y2, damage_type_int, timestamp):
    """
    Process the original image: crop the ROI, resize it, draw a bounding box,
    and prepare the LMM input data.

    :param original_image_path: Path to the original image file.
    :param x1: X-coordinate of top-left corner of the ROI.
    :param y1: Y-coordinate of top-left corner of the ROI.
    :param x2: X-coordinate of bottom-right corner of the ROI.
    :param y2: Y-coordinate of bottom-right corner of the ROI.
    :param damage_type_int: Integer representing the damage type.
    :param timestamp: Timestamp string for file naming.
    :return: A tuple (image_paths_dict, lmm_input_dict).
    """
    damage_type = get_damage_type_label(damage_type_int)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    with Image.open(original_image_path) as img:
        # Crop image
        cropped_img = img.crop((x1, y1, x2, y2))
        cropped_image_path = os.path.join(CROPPED_FOLDER, f"cropped_{timestamp}.png")
        cropped_img.save(cropped_image_path)

        # Resize (thumbnail)
        cropped_img.thumbnail((256, 256))
        resized_image_path = os.path.join(CROPPED_FOLDER, f"resized_{timestamp}.png")
        cropped_img.save(resized_image_path)

        # Draw bounding box on original image
        draw = ImageDraw.Draw(img)
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        boxed_image_path = os.path.join(CROPPED_FOLDER, f"boxed_{timestamp}.png")
        img.save(boxed_image_path)

    resized_image_base64 = encode_base64_image(resized_image_path)

    lmm_input = {
        "Damage Type": damage_type,
        "Width": width,
        "Height": height,
        "CroppedImage": f"data:image/png;base64,{resized_image_base64}"
    }

    return {
        "cropped": cropped_image_path,
        "resized": resized_image_path,
        "boxed": boxed_image_path
    }, lmm_input
