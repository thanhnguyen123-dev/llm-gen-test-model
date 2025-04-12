# LLM_Test_Gen/Python_Scripts/format_and_save_tests.py
from __future__ import annotations

import csv
import os
import re # For extracting class/package names
import sys
from pathlib import Path

# --- Configuration ---
# Define paths relative to THIS script file (format_and_save_tests.py)
INPUT_CSV_RELATIVE_PATH = "../Data/Generated_Test_Data.csv" # Output from step 3.2
OUTPUT_CSV_RELATIVE_PATH = "../Data/Test_Data_Formatted.csv" # Final output for step 3.3

# Base directory within lang_1_buggy to save test files
# Relative path from the *project root* (thanh_nguyen_u7594144) - Calculated later
LANG1_TEST_SRC_REL_PATH = "lang_1_buggy/src/test/java"
# Specific package structure required by the task
TARGET_PACKAGE_PATH = "org/apache/commons/lang3"

# CSV Column Headers
INPUT_HEADER = ["FQN", "Signature", "Jimple Code Representation", "Generated Code"] # Expected input
OUTPUT_HEADER = ["FQN", "Signature", "Jimple Code Representation", "Generated Code", "Code After Formatting", "Saved Path"] # Final output

# --- Helper Function for Formatting and Info Extraction ---
def format_llm_code(raw_code: str) -> str | None:
    """
    Cleans raw code from LLM artifacts (markdown fences).

    Args:
        raw_code: The raw string potentially containing Java code and extra text.

    Returns:
        The cleaned code string, or None if input indicates an error or is empty.
    """
    if not raw_code or raw_code.strip().startswith("// ERROR:"):
        return None # Propagate previous errors or handle empty input

    # 1. Remove leading/trailing whitespace
    code = raw_code.strip()

    # 2. Remove ```java fence and optional 'java' language hint
    if code.startswith("```java"):
        code = code[len("```java"):].strip()
    elif code.startswith("```"):
        code = code[len("```"):].strip()

    # 3. Remove trailing ``` fence
    if code.endswith("```"):
        code = code[:-len("```")].strip()

    # Return the cleaned code, could still be empty if input was just fences
    return code if code else None


def extract_class_name(formatted_code: str) -> str | None:
    """
    Extracts the primary public or default class name ending in 'Test'.

    Args:
        formatted_code: The cleaned Java code string.

    Returns:
        The extracted class name (e.g., WordUtilsTest) or None if not found.
    """
    if not formatted_code:
        return None

    # Look for 'public class XxxTest {', 'class XxxTest {', etc.
    # Making it robust to different spacing and potential modifiers before 'class'
    class_match = re.search(
        r"^\s*(?:public\s+|final\s+)*class\s+([\w$]+Test)\s*(?:\{|\s+implements|\s+extends)",
        formatted_code,
        re.MULTILINE
    )
    if class_match:
        return class_match.group(1).strip()
    else:
        # Fallback: Maybe no 'Test' suffix was generated? Look for any class.
        # This is less ideal but might catch some cases.
        class_match_any = re.search(
             r"^\s*(?:public\s+|final\s+)*class\s+([\w$]+)\s*(?:\{|\s+implements|\s+extends)",
             formatted_code,
             re.MULTILINE
        )
        if class_match_any:
            print(f"WARNING: Found class name '{class_match_any.group(1)}' without 'Test' suffix. Using it anyway.")
            return class_match_any.group(1).strip()

    return None # No suitable class definition found


# --- Main Logic ---
if __name__ == "__main__":
    print("--- Starting Task 3.3: Test Code Formatting and Saving ---")

    # Calculate absolute paths
    try:
        script_dir = Path(__file__).parent.resolve()
        project_root = script_dir.parent.parent # Assumes script is in LLM_Test_Gen/Python_Scripts
        input_csv_path = (script_dir / INPUT_CSV_RELATIVE_PATH).resolve()
        output_csv_path = (script_dir / OUTPUT_CSV_RELATIVE_PATH).resolve()
        # Base directory to save .java test files inside lang_1_buggy
        base_test_save_dir = (project_root / LANG1_TEST_SRC_REL_PATH).resolve()

        print(f"Input CSV (Absolute): {input_csv_path}")
        print(f"Output CSV (Absolute): {output_csv_path}")
        print(f"Base Test Save Directory: {base_test_save_dir}")
    except Exception as e:
        print(f"FATAL ERROR: Could not calculate file paths: {e}")
        exit(1)

    # Verify input CSV exists
    if not input_csv_path.is_file():
        print(f"FATAL ERROR: Input CSV file not found at {input_csv_path}")
        exit(1)

    # Ensure base output directory exists
    try:
        # This creates lang_1_buggy/src/test/java if it doesn't exist
        base_test_save_dir.mkdir(parents=True, exist_ok=True)
        print(f"Ensured base test save directory exists: {base_test_save_dir}")
    except Exception as e:
        print(f"FATAL ERROR: Could not create base directory for saving tests: {base_test_save_dir}")
        print(f"             Error: {e}")
        exit(1)


    rows_processed = 0
    files_saved = 0
    formatting_errors = 0
    output_data = [] # Store results before writing

    # --- Read the input CSV ---
    try:
        print(f"Reading input CSV: {input_csv_path}...")
        with open(input_csv_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader) # Read header
            if len(header) != len(INPUT_HEADER) or header != INPUT_HEADER:
                 print(f"WARNING: Input CSV header mismatch.")
                 print(f"  Expected: {INPUT_HEADER}")
                 print(f"  Got:      {header}")
                 print(f"  Attempting to proceed using column indices 0, 1, 2, 3...")
                 # Fallback to indices if header is wrong, less robust
                 header_indices = {'fqn': 0, 'signature': 1, 'jimple': 2, 'generated': 3}
            else:
                 print("Input header validated.")
                 # Store indices based on correct header
                 header_indices = {
                     'fqn': header.index(INPUT_HEADER[0]),
                     'signature': header.index(INPUT_HEADER[1]),
                     'jimple': header.index(INPUT_HEADER[2]),
                     'generated': header.index(INPUT_HEADER[3]) # Index of Generated Code
                 }

            # Read all rows into memory first
            input_rows = list(reader)
            print(f"Read {len(input_rows)} data rows from input CSV.")

    except Exception as e:
        print(f"FATAL ERROR: Failed to read input CSV file '{input_csv_path}': {e}")
        exit(1)

    # --- Process each row ---
    for row_idx, row in enumerate(input_rows):
        rows_processed += 1
        if len(row) < max(header_indices.values()) + 1:
            print(f"WARNING: Skipping row {row_idx + 1} due to incorrect column count: {len(row)}")
            # Add placeholder data to output if necessary
            output_data.append(row + ["// ERROR: Invalid input row", "N/A"])
            formatting_errors += 1
            continue

        # Extract data using indices
        fqn = row[header_indices['fqn']]
        signature = row[header_indices['signature']]
        jimple = row[header_indices['jimple']]
        raw_generated_code = row[header_indices['generated']]

        print(f"\nProcessing row {row_idx + 1}: {fqn}")

        # Format code and extract info
        formatted_code = format_llm_code(raw_generated_code)
        class_name = extract_class_name(formatted_code) if formatted_code else None

        saved_path_str = "N/A" # Default

        if formatted_code and class_name:
            # Code was formatted and class name was extracted
            try:
                # Construct save path using the *required* package structure
                package_path = Path(TARGET_PACKAGE_PATH) # Use the defined constant
                save_dir = base_test_save_dir / package_path
                save_path = save_dir / f"{class_name}.java"

                # Create directory if it doesn't exist
                save_dir.mkdir(parents=True, exist_ok=True)

                # Save the formatted code
                with open(save_path, 'w', encoding='utf-8') as java_file:
                    java_file.write(formatted_code)

                # Store path relative to project root for CSV output
                saved_path_str = str(save_path.relative_to(project_root))
                print(f"  -> Saved formatted test to: {saved_path_str}")
                files_saved += 1

            except Exception as e:
                print(f"  -> ERROR saving file for {fqn}: {e}")
                saved_path_str = f"// ERROR saving file: {e}"
                formatting_errors += 1
        elif formatted_code is None:
             # This means the input row indicated a previous error
             print(f"  -> Skipping saving due to error in 'Generated Code'.")
             formatted_code = raw_generated_code # Keep the original error message
             saved_path_str = "N/A (Previous Error)"
             formatting_errors +=1
        else:
            # Formatting succeeded but couldn't extract class name
            print(f"  -> ERROR: Could not extract class name from formatted code for {fqn}.")
            saved_path_str = "// ERROR: Class Name Extraction Failed"
            formatting_errors += 1

        # Append results for this row to output data
        output_data.append([
            fqn,
            signature,
            jimple,
            raw_generated_code, # Original code from LLM
            formatted_code if formatted_code else "// ERROR: Formatting Failed or Input Error", # Formatted code
            saved_path_str      # Path or error/N/A
        ])

    # --- Write the final output CSV ---
    try:
        print(f"\nWriting results to output CSV: {output_csv_path}...")
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            writer.writerow(OUTPUT_HEADER) # Write the new 6-column header
            writer.writerows(output_data) # Write all processed rows
        print("Output CSV written successfully.")

    except Exception as e:
        print(f"\nFATAL ERROR: An error occurred writing the final output CSV '{output_csv_path}': {e}")
        exit(1)

    # --- Final Summary ---
    print("\n--- Task 3.3 Complete ---")
    print(f"Total rows processed: {rows_processed}")
    print(f"Java test files successfully saved: {files_saved}")
    print(f"Rows with formatting/saving errors or skipped: {formatting_errors}")
    print(f"Output CSV written to: {output_csv_path}")
    print("------------------------")