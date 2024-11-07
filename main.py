import argparse
import json
from pharmacy_app.data_reader import read_pharmacies, read_json_files
from pharmacy_app.data_validator import filter_claims, filter_reverts
from pharmacy_app.metrics_calculator import (
    calculate_metrics,
    calculate_chain_recommendations,
    calculate_common_quantities,
)


# Set up argument parser to accept command-line arguments for directories
parser = argparse.ArgumentParser(description='Process pharmacy, claims, and reverts data.')
parser.add_argument('--pharmacy_dirs', nargs='+', help='List of pharmacy data directories')
parser.add_argument('--claims_dirs', nargs='+', help='List of claims event directories')
parser.add_argument('--reverts_dirs', nargs='+', help='List of revert event directories')
args = parser.parse_args()

def main():
    # Read data from provided directories
    pharmacies = read_pharmacies(args.pharmacy_dirs)
    claims = read_json_files(args.claims_dirs)
    reverts = read_json_files(args.reverts_dirs)

    # Filter and validate claims and reverts
    filtered_claims = filter_claims(claims, pharmacies)
    valid_claim_ids = set(claim['id'] for claim in filtered_claims)
    filtered_reverts = filter_reverts(reverts, valid_claim_ids)

    # Goal 2: Calculate Metrics per NPI and NDC
    metrics = calculate_metrics(filtered_claims, filtered_reverts)
    with open('output/metrics_output.json', 'w') as outfile:
        json.dump(metrics, outfile, indent=4)

    # Goal 3: Calculate Top 2 Chain Recommendations per Drug
    recommendations = calculate_chain_recommendations(filtered_claims, pharmacies)
    with open('output/recommendations_output.json', 'w') as outfile:
        json.dump(recommendations, outfile, indent=4)

    # Goal 4: Identify Most Common Quantities Prescribed per Drug
    common_quantities = calculate_common_quantities(filtered_claims)
    with open('output/common_quantities_output.json', 'w') as outfile:
        json.dump(common_quantities, outfile, indent=4)

if __name__ == "__main__":
    main()
