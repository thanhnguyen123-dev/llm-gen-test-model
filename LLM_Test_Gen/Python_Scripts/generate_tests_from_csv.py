import csv
import sys
import time
import os
from pathlib import Path

script_dir = Path(__file__).parent.resolve() # Directory containing this script
service_parent_dir = script_dir.parent # Go up to Python_Scripts
sys.path.insert(0, str(service_parent_dir)) # Add Python_Scripts to the path

from gpt_services import openai_service


# --- Configuration ---
# Define paths relative to THIS script file (generate_tests_from_csv.py)
INPUT_CSV_RELATIVE_PATH = "../Data/Test_Data.csv"
OUTPUT_CSV_RELATIVE_PATH = "../Data/Generated_Test_Data.csv"

# Fully qualified prefixes of the classes to process
TARGET_CLASS_PREFIXES = [
    "org.apache.commons.lang3.CharRange.",
    "org.apache.commons.lang3.CharSetUtils.",
    "org.apache.commons.lang3.text.WordUtils."
]

# CSV Column Headers
INPUT_HEADER = ["FQN", "Signature", "Jimple Code Representation"]
OUTPUT_HEADER = ["FQN", "Signature", "Jimple Code Representation", "Generated Code"]

# Delay between API calls (in seconds) to avoid rate limits
API_CALL_DELAY = 1 # Adjust as needed

# --- Main Logic ---
if __name__ == "__main__":
    print("--- Starting Test Generation from CSV (Using Absolute Paths) ---")

    # Calculate absolute paths based on this script's location
    try:
        # script_dir is already defined above for the import
        input_csv_path = (script_dir / INPUT_CSV_RELATIVE_PATH).resolve()
        output_csv_path = (script_dir / OUTPUT_CSV_RELATIVE_PATH).resolve()
        print(f"Script Directory: {script_dir}")
        print(f"Input CSV (Absolute): {input_csv_path}")
        print(f"Output CSV (Absolute): {output_csv_path}")
    except Exception as e:
        print(f"FATAL ERROR: Could not calculate file paths: {e}")
        print(f"           Script directory might not be determined correctly.")
        exit(1)

    # Verify input CSV exists using the calculated absolute path
    if not input_csv_path.is_file():
        print(f"FATAL ERROR: Input CSV file not found at calculated path: {input_csv_path}")
        print(f"           Current Working Directory: {os.getcwd()}") # Still useful info
        exit(1)

    # Ensure parent directory for output CSV exists
    try:
        output_csv_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Ensured output directory exists: {output_csv_path.parent}")
    except Exception as e:
        print(f"FATAL ERROR: Could not create parent directory for output CSV: {output_csv_path.parent}")
        print(f"             Error: {e}")
        exit(1)


    methods_to_process = []
    header_indices = {}

    # --- Read the input CSV using the absolute path ---
    try:
        print("Reading input CSV...")
        with open(input_csv_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)

            try:
                header_indices['fqn'] = header.index(INPUT_HEADER[0])
                header_indices['signature'] = header.index(INPUT_HEADER[1])
                header_indices['jimple'] = header.index(INPUT_HEADER[2])
            except ValueError as e:
                print(f"FATAL ERROR: Missing expected column in input CSV: {e}. Expected: {INPUT_HEADER}")
                exit(1)

            for row in reader:
                if len(row) < max(header_indices.values()) + 1:
                    print(f"WARNING: Skipping malformed row: {row}")
                    continue

                fqn = row[header_indices['fqn']]
                process_this_row = any(fqn.startswith(prefix) for prefix in TARGET_CLASS_PREFIXES)

                if process_this_row:
                    methods_to_process.append({
                        'fqn': fqn,
                        'signature': row[header_indices['signature']],
                        'jimple': row[header_indices['jimple']]
                    })

        print(f"Found {len(methods_to_process)} methods matching target classes.")

    except Exception as e:
        print(f"FATAL ERROR: Failed to read input CSV file '{input_csv_path}': {e}")
        exit(1)

    # --- Process methods and write output CSV using the absolute path ---
    if not methods_to_process:
        print("No methods found to process. Exiting.")
        exit(0)

    print(f"\nGenerating tests for {len(methods_to_process)} methods...")
    processed_count = 0
    error_count = 0

    try:
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            writer.writerow(OUTPUT_HEADER)

            for method_data in methods_to_process:
                fqn = method_data['fqn']
                signature = method_data['signature']
                jimple = method_data['jimple']

                print(f"\nProcessing method {processed_count + 1}/{len(methods_to_process)}: {fqn}")

                # --- Call the OpenAI service ---
                # Assumes openai_service.py handles its own template path correctly
                generated_code = openai_service.generate_test_for_prompt_template(
                    fqn, signature, jimple
                )

                # --- Check for errors and Write ---
                if generated_code.strip().startswith("// ERROR:"):
                    error_count += 1
                    print(f"  -> Service returned an error.")
                else:
                     print(f"  -> Test code generated successfully.")

                writer.writerow([fqn, signature, jimple, generated_code])
                processed_count += 1

                # --- Add delay ---
                if processed_count < len(methods_to_process):
                    print(f"  -> Waiting for {API_CALL_DELAY} second(s)...")
                    time.sleep(API_CALL_DELAY)

    except Exception as e:
        print(f"\nFATAL ERROR: An error occurred during test generation or writing to output CSV '{output_csv_path}': {e}")
        import traceback
        traceback.print_exc()
        exit(1)

    # --- Final Summary ---
    print("\n--- Processing Complete ---")
    print(f"Total methods processed: {processed_count}")
    print(f"Methods resulting in errors from OpenAI service: {error_count}")
    print(f"Output written to: {output_csv_path}")
    print("----------------------------")