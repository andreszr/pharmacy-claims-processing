from datetime import datetime

def validate_claim(claim):
    """
    Validates a claim event to ensure it complies with the schema.

    Args:
        claim (dict): The claim event to validate.

    Returns:
        bool: True if the claim is valid, False otherwise.
    """
    required_fields = ['id', 'npi', 'ndc', 'price', 'quantity', 'timestamp']
    for field in required_fields:
        # Check if required fields are present and not empty
        if field not in claim or claim[field] in [None, '']:
            return False
    # Convert data types and validate values
    try:
        claim['price'] = float(claim['price'])
        claim['quantity'] = float(claim['quantity'])
        if claim['quantity'] == 0:
            return False  # Exclude claims with zero quantity
        claim['timestamp'] = datetime.fromisoformat(claim['timestamp'])
    except ValueError:
        return False
    return True

def validate_revert(revert):
    """
    Validates a revert event to ensure it complies with the schema.

    Args:
        revert (dict): The revert event to validate.

    Returns:
        bool: True if the revert is valid, False otherwise.
    """
    required_fields = ['id', 'claim_id', 'timestamp']
    for field in required_fields:
        # Check if required fields are present and not empty
        if field not in revert or revert[field] in [None, '']:
            return False
    # Convert timestamp to datetime object
    try:
        revert['timestamp'] = datetime.fromisoformat(revert['timestamp'])
    except ValueError:
        return False
    return True

def filter_claims(claims, pharmacies):
    """
    Filters and validates claims, keeping only valid claims from known pharmacies.

    Args:
        claims (list): List of claim events.
        pharmacies (dict): Dictionary of valid pharmacies.

    Returns:
        list: List of validated and filtered claim events.
    """
    filtered_claims = []
    for claim in claims:
        if validate_claim(claim) and claim['npi'] in pharmacies:
            filtered_claims.append(claim)
    return filtered_claims

def filter_reverts(reverts, valid_claim_ids):
    """
    Filters and validates reverts, keeping only valid reverts for known claims.

    Args:
        reverts (list): List of revert events.
        valid_claim_ids (set): Set of valid claim IDs.

    Returns:
        list: List of validated and filtered revert events.
    """
    filtered_reverts = []
    for revert in reverts:
        if validate_revert(revert) and revert['claim_id'] in valid_claim_ids:
            filtered_reverts.append(revert)
    return filtered_reverts
