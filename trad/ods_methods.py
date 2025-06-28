import json
import pandas as pd

def json_to_ods(base_filename):
    """
    Convert a JSON file (base_filename.json) to an ODS spreadsheet (base_filename.ods).
    """
    json_path = f"{base_filename}.json"
    ods_path = f"{base_filename}.ods"

    # Load the JSON data from the file
    with open(json_path, "r") as file:
        data = json.load(file)

    # Convert JSON data to a DataFrame
    df = pd.DataFrame(data)

    # Save DataFrame to an ODS file
    df.to_excel(ods_path, engine='odf', index=False)
    print(f"ODS file saved to: {ods_path}")

def ods_to_json(base_filename):
    """
    Convert an ODS spreadsheet (base_filename.ods) to a JSON file (base_filename.json).
    """
    ods_path = f"{base_filename}.ods"
    json_path = f"{base_filename}.json"

    # Read the ODS file into a DataFrame
    df = pd.read_excel(ods_path, engine='odf')

    # Convert DataFrame to JSON and save
    with open(json_path, "w") as file:
        json.dump(df.to_dict(orient="records"), file, indent=2)

    print(f"JSON file saved to: {json_path}")

# Example usage
# json_to_ods("/mnt/data/high_frontier_sites")
# ods_to_json("/mnt/data/high_frontier_sites")
