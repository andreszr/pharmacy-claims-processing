def calculate_metrics(claims, reverts):
    """
    Calculates metrics for each combination of NPI and NDC.

    Args:
        claims (list): List of validated claim events.
        reverts (list): List of validated revert events.

    Returns:
        list: List of dictionaries containing metrics per NPI and NDC.
    """
    metrics = {}
    # Create sets for efficient lookup
    claim_ids = set(claim['id'] for claim in claims)
    reverted_claim_ids = set(revert['claim_id'] for revert in reverts)

    for claim in claims:
        npi = claim['npi']
        ndc = claim['ndc']
        key = (npi, ndc)
        unit_price = claim['price'] / claim['quantity']

        if key not in metrics:
            # Initialize metrics for this NPI and NDC combination
            metrics[key] = {
                'npi': npi,
                'ndc': ndc,
                'fills': 0,
                'reverted': 0,
                'total_unit_price': 0.0,
                'total_price': 0.0,
            }
        # Update metrics
        metrics[key]['fills'] += 1
        metrics[key]['total_unit_price'] += unit_price
        metrics[key]['total_price'] += claim['price']

        if claim['id'] in reverted_claim_ids:
            metrics[key]['reverted'] += 1

    # Calculate average unit price for each NPI and NDC
    output = []
    for key in metrics:
        fills = metrics[key]['fills']
        total_unit_price = metrics[key]['total_unit_price']
        avg_price = total_unit_price / fills
        metrics[key]['avg_price'] = avg_price

        # Prepare the output entry
        entry = metrics[key]
        output.append({
            'npi': entry['npi'],
            'ndc': entry['ndc'],
            'fills': entry['fills'],
            'reverted': entry['reverted'],
            'avg_price': round(entry['avg_price'], 2),
            'total_price': round(entry['total_price'], 2)
        })

    return output

def calculate_chain_recommendations(claims, pharmacies):
    """
    Calculates the top 2 chains per drug based on the lowest average unit price.

    Args:
        claims (list): List of validated claim events.
        pharmacies (dict): Dictionary mapping NPIs to chain names.

    Returns:
        list: List of dictionaries containing the top 2 chains per drug.
    """
    ndc_chain_prices = {}

    for claim in claims:
        npi = claim['npi']
        ndc = claim['ndc']
        chain = pharmacies.get(npi)
        unit_price = claim['price'] / claim['quantity']

        if (ndc, chain) not in ndc_chain_prices:
            # Initialize data for this NDC and chain combination
            ndc_chain_prices[(ndc, chain)] = {'total_unit_price': 0.0, 'count': 0}

        # Update total unit price and count
        ndc_chain_prices[(ndc, chain)]['total_unit_price'] += unit_price
        ndc_chain_prices[(ndc, chain)]['count'] += 1

    # Calculate average unit prices per chain and drug
    ndc_chain_avg_prices = {}
    for (ndc, chain), data in ndc_chain_prices.items():
        avg_price = data['total_unit_price'] / data['count']
        if ndc not in ndc_chain_avg_prices:
            ndc_chain_avg_prices[ndc] = []
        # Append the average price for this chain
        ndc_chain_avg_prices[ndc].append({'name': chain, 'avg_price': round(avg_price, 2)})

    # Select the top 2 chains with the lowest average unit price for each drug
    recommendations = []
    for ndc, chains in ndc_chain_avg_prices.items():
        sorted_chains = sorted(chains, key=lambda x: x['avg_price'])
        recommendations.append({'ndc': ndc, 'chain': sorted_chains[:2]})

    return recommendations

def calculate_common_quantities(claims):
    """
    Identifies the most common quantities prescribed for each drug.

    Args:
        claims (list): List of validated claim events.

    Returns:
        list: List of dictionaries containing the most common quantities per drug.
    """
    ndc_quantities = {}

    for claim in claims:
        ndc = claim['ndc']
        quantity = claim['quantity']
        if ndc not in ndc_quantities:
            # Initialize quantity counts for this NDC
            ndc_quantities[ndc] = {}
        if quantity not in ndc_quantities[ndc]:
            ndc_quantities[ndc][quantity] = 0
        # Increment the count for this quantity
        ndc_quantities[ndc][quantity] += 1

    # Get the top 5 most common quantities for each drug
    common_quantities = []
    for ndc, quantities in ndc_quantities.items():
        sorted_quantities = sorted(quantities.items(), key=lambda x: x[1], reverse=True)
        top_quantities = [q[0] for q in sorted_quantities[:5]]
        common_quantities.append({'ndc': ndc, 'most_prescribed_quantity': top_quantities})

    return common_quantities
