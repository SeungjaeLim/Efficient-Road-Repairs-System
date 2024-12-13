import requests
from datetime import datetime
from utils import generate_random_geo
import os

def send_to_epcis(parsed_result, lmm_input, boxed_image_path):
    """
    Send event data to the EPCIS server.

    :param parsed_result: The final dictionary containing cost info and damage details.
    :param lmm_input: The dictionary with dimension and damage type.
    :param boxed_image_path: Path to the boxed image file.
    :return: The text response from the EPCIS server.
    :raises Exception: If the EPCIS server returns a non-success status code.
    """
    epcis_post_data = {
        "@context": [
            "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
            {
                "https://yourdomain.com/damageType": "https://yourdomain.com/vocab/damageType",
                "https://yourdomain.com/dimensions": "https://yourdomain.com/vocab/dimensions",
                "https://yourdomain.com/repairCost": "https://yourdomain.com/vocab/repairCost",
                "https://yourdomain.com/repairItems": "https://yourdomain.com/vocab/repairItems",
                "https://yourdomain.com/filename": "https://yourdomain.com/vocab/filename"
            }
        ],
        "type": "ObjectEvent",
        "action": "ADD",
        "bizStep": "repairing",
        "disposition": "in_progress",
        "epcList": ["urn:epc:id:road:0012345"],
        "eventTime": datetime.now().isoformat() + "Z",
        "eventTimeZoneOffset": "+00:00",
        "readPoint": {
            "id": f"urn:epc:id:geo:{generate_random_geo()}"
        },
        "ilmd": {
            "https://yourdomain.com/dimensions": {
                "Width": lmm_input["Width"],
                "Height": lmm_input["Height"]
            },
            "https://yourdomain.com/damageType": lmm_input["Damage Type"],
            "https://yourdomain.com/repairCost": {
                "TotalCost": parsed_result.get("Repair Cost", 0),
                "items": parsed_result.get("Repair Items", [])
            },
            "https://yourdomain.com/filename": os.path.basename(boxed_image_path)
        }
    }

    headers = {
        "Content-Type": "application/json",
        "GS1-EPCIS-Version": "2.0.0",
        "GS1-CBV-Version": "2.0.0"
    }
    epcis_server_url = "http://192.168.4.7:8090/epcis/v2/events"
    response = requests.post(epcis_server_url, headers=headers, json=epcis_post_data)
    if response.status_code not in [200, 201, 202]:
        raise Exception(
            f"Failed to send POST request to EPCIS server "
            f"(Status {response.status_code}): {response.text}"
        )

    return response.text
