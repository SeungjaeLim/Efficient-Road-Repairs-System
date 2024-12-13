def calculate_total_costs(parsed_result, lmm_input):
    """
    Calculate total repair costs based on parsed LMM result.
    Add 'Repair Cost', 'Dimensions', and 'Damage Type' fields.

    :param parsed_result: The dictionary returned by LMM.
    :param lmm_input: The dictionary with original dimensions and damage type.
    :return: The updated parsed_result dictionary with costs and additional info.
    """
    total_repair_cost = 0
    for item in parsed_result.get("Repair Items", []):
        quantity = item["Quantity"]
        unit_price = item["UnitPrice"]
        total_price = quantity * unit_price
        total_repair_cost += total_price
        item["TotalPrice"] = total_price

    parsed_result["Repair Cost"] = total_repair_cost
    parsed_result["Dimensions"] = {
        "Width": lmm_input["Width"],
        "Height": lmm_input["Height"]
    }
    parsed_result["Damage Type"] = lmm_input["Damage Type"]
    return parsed_result
