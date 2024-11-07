# Pharmacy Claims Processing Application

## Description
This application processes pharmacy, claims, and reverts data to calculate metrics, make chain recommendations, and identify the most common quantities prescribed for drugs.

## Requirements
- **Python 3.x**
- Standard Python libraries: `json`, `csv`, `argparse`, `datetime`, `os`

## Setup

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    ```

2. **Navigate to the project directory**:
    ```bash
    cd pharmacy-claims-processing
    ```

3. **Ensure Python 3.x is installed** on your system.

## Usage

1. **Prepare your data directories**:
    - **Pharmacy Data**: Place your pharmacy CSV files in one or more directories.
    - **Claims Data**: Place your claims JSON files in one or more directories.
    - **Reverts Data**: Place your reverts JSON files in one or more directories.

2. **Run the application**:

    Execute the application by specifying the directories containing your data:
    ```bash
    python main.py \
    --pharmacy_dirs path/to/pharmacy_dir \
    --claims_dirs path/to/claims_dir \
    --reverts_dirs path/to/reverts_dir
    ```

    - Replace `path/to/pharmacy_dir`, `path/to/claims_dir`, and `path/to/reverts_dir` with the paths to your actual data directories.
    - The `--output_dir` argument specifies where the output files will be saved. If not provided, output files will be saved in the current directory.

3. **Example Command**:
    ```bash
    python main.py \
    --pharmacy_dirs data/pharmacies \
    --claims_dirs data/claims \
    --reverts_dirs data/reverts
    ```

    This command reads data from the specified directories and writes output files to the `output` directory.

## Output Files

The application will generate the following JSON files in the specified output directory:

- `metrics_output.json`: Metrics per NPI and NDC.
- `recommendations_output.json`: Top 2 chain recommendations per drug.
- `common_quantities_output.json`: Most common quantities prescribed per drug.
