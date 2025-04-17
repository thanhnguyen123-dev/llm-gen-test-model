#!/usr/bin/env python3
from __future__ import annotations
import csv
import re
from pathlib import Path
from collections import defaultdict

# ––––– CONFIG –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
INPUT_CSV_RELATIVE_PATH   = "../Data/Generated_Test_Data.csv"
OUTPUT_CSV_RELATIVE_PATH  = "../Data/Formatted_Test_Data.csv"
LANG1_TEST_SRC_REL_PATH   = "lang_1_buggy/src/test/java"
TARGET_PACKAGE_PATH       = "org/apache/commons/lang3/"
# Output‐CSV header
OUTPUT_HEADER = [
    "FQN", "Signature", "Jimple Code Representation", "Generated Code",
    "Code After Formatting", "Saved Path"
]
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

def strip_code_fences(raw: str) -> str|None:
    if not raw or raw.strip().startswith("// ERROR:"):
        return None
    code = raw.strip()
    code = re.sub(r"^```(?:java)?\s*", "", code)
    code = re.sub(r"\s*```$", "", code)
    return code.strip() or None

def extract_class_name(code: str) -> str|None:
    m = re.search(r"^\s*class\s+([\w$]+)\s*\{", code, re.MULTILINE)
    return m.group(1) if m else None

def collect_components(code: str, class_name: str):
    lines = code.splitlines()
    pkg     = next((l for l in lines if l.startswith("package ")), "")
    imports = {l for l in lines if l.startswith("import ")}
    # find class decl
    try:
        idx = next(i for i,l in enumerate(lines)
                   if re.match(rf"\s*class\s+{re.escape(class_name)}\b", l))
    except StopIteration:
        return pkg, imports, None, None, []
    body = lines[idx+1:]
    if body and body[-1].strip() == "}":
        body = body[:-1]

    field_line = None
    setup_block = None
    test_blocks: list[list[str]] = []

    i = 0
    while i < len(body):
        line    = body[i]
        stripped = line.strip()

        # private field
        if field_line is None and re.match(
            rf"\s*private\s+{class_name[:-4]}\s+\w+;", line
        ):
            field_line = line.rstrip()
            i += 1
            continue

        # @BeforeEach
        if setup_block is None and stripped.startswith("@BeforeEach"):
            indent = re.match(r"^(\s*)", line).group(1)
            blk = []
            while i < len(body):
                blk.append(body[i].rstrip())
                if body[i].strip() == "}" and body[i].startswith(indent):
                    break
                i += 1
            setup_block = blk
            i += 1
            continue

        # @Test methods
        if stripped.startswith("@Test"):
            indent = re.match(r"^(\s*)", line).group(1)
            blk = []
            while i < len(body):
                blk.append(body[i].rstrip())
                if body[i].strip() == "}" and body[i].startswith(indent):
                    break
                i += 1
            test_blocks.append(blk)
            i += 1
            continue

        i += 1

    return pkg, imports, field_line, setup_block, test_blocks

def main():
    script_dir   = Path(__file__).parent.resolve()
    project_root = script_dir.parent.parent
    input_csv    = (script_dir / INPUT_CSV_RELATIVE_PATH).resolve()
    output_csv   = (script_dir / OUTPUT_CSV_RELATIVE_PATH).resolve()
    target_dir   = (project_root / LANG1_TEST_SRC_REL_PATH / TARGET_PACKAGE_PATH).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    # Read original CSV
    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows   = list(reader)

    # Prepare aggregator and CSV‑rows
    classes    = defaultdict(lambda: {
        "package": None, "imports": set(),
        "field": None, "setup": None, "tests": []
    })
    output_rows: list[list[str]] = []

    for row in rows:
        fqn, sig, jimple, raw = row
        code = strip_code_fences(raw)
        cls  = extract_class_name(code) if code else None

        # Determine saved‐path (even on failure) so CSV stays aligned
        saved_path = (
            f"{LANG1_TEST_SRC_REL_PATH}/{TARGET_PACKAGE_PATH}/{cls}.java"
            if cls else "N/A"
        )

        # Append to CSV data
        output_rows.append([
            fqn, sig, jimple, raw,
            code or "// ERROR: Formatting Failed",
            saved_path
        ])

        # If formatting failed, skip aggregation
        if not code or not cls:
            continue

        # Collect into per‐class buffer
        pkg, imps, fld, setup, tests = collect_components(code, cls)
        info = classes[cls]
        if pkg    and info["package"] is None: info["package"] = pkg
        info["imports"].update(imps)
        if fld    and info["field"]   is None: info["field"]   = fld
        if setup  and info["setup"]   is None: info["setup"]   = setup
        info["tests"].extend(tests)

    # Write out each aggregated test‑class
    for cls, info in classes.items():
        out_path = target_dir / f"{cls}.java"
        with open(out_path, "w", encoding="utf-8") as out:
            # package
            if info["package"]:
                out.write(info["package"] + "\n\n")
            # imports
            for imp in sorted(info["imports"]):
                out.write(imp + "\n")
            out.write("\n")
            # Javadoc + class
            out.write("/**\n")
            out.write(f" * Aggregated JUnit tests for {cls}.\n")
            out.write(" */\n")
            out.write(f"class {cls} " + "{\n\n")
            # single private field
            if info["field"]:
                out.write("    " + info["field"] + "\n\n")
            # single @BeforeEach
            if info["setup"]:
                for L in info["setup"]:
                    out.write("    " + L + "\n")
                out.write("\n")
            # every @Test block
            for blk in info["tests"]:
                for L in blk:
                    out.write("    " + L + "\n")
                out.write("\n")
            out.write("}\n")
        print(f"→ Wrote {out_path.relative_to(project_root)}")

    # Finally, write the Formatted_Test_Data.csv
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(OUTPUT_HEADER)
        writer.writerows(output_rows)
    print(f"→ Wrote {output_csv.relative_to(project_root)}")

if __name__ == "__main__":
    main()
