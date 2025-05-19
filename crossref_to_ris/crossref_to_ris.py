"""
crossref_to_ris.py

Author: Giorgio Casaburi
License: MIT

Description:
This script takes a plain-text list of references and queries the CrossRef API
for each entry to retrieve full citation metadata. Matched entries are exported
as an RIS file for use in citation managers (e.g., Zotero, EndNote). Unmatched
references are logged separately for review.

Usage:
    python crossref_to_ris.py <input_file> <output_ris_file> <not_found_file>

Example:
    python crossref_to_ris.py references.txt output.ris not_found.txt

Dependencies:
    - requests

Reference:
    CrossRef API documentation: https://api.crossref.org/swagger-ui/index.html
"""

import sys
import requests
import re
import time
from pathlib import Path

# Check command-line arguments
if len(sys.argv) != 4:
    print("Usage: python crossref_to_ris.py <input_file> <output_ris_file> <not_found_file>")
    sys.exit(1)

# Assign input/output paths
input_path = Path(sys.argv[1])
output_ris_path = Path(sys.argv[2])
not_found_path = Path(sys.argv[3])

# Read and clean the reference list
with open(input_path, "r") as f:
    references = [re.sub(r"^\d+\.\s*", "", line.strip()) for line in f if line.strip()]

# Define function to query CrossRef

def search_crossref(reference):
    url = "https://api.crossref.org/works"
    params = {"query.bibliographic": reference, "rows": 1}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        items = response.json().get("message", {}).get("items", [])
        return items[0] if items else None
    except Exception as e:
        print(f"⚠️ Error for: {reference[:60]}... ({e})")
        return None

# Define function to format metadata into RIS

def convert_to_ris(item):
    lines = ["TY  - JOUR"]

    if 'author' in item:
        for author in item['author']:
            family = author.get('family', '')
            given = author.get('given', '')
            if family or given:
                lines.append(f"AU  - {family}, {given}")

    lines.append(f"TI  - {item.get('title', [''])[0]}")
    lines.append(f"JO  - {item.get('container-title', [''])[0]}")
    lines.append(f"Y1  - {item.get('issued', {}).get('date-parts', [[None]])[0][0]}")
    lines.append(f"VL  - {item.get('volume', '')}")
    lines.append(f"IS  - {item.get('issue', '')}")

    if 'page' in item and '-' in item['page']:
        start, end = item['page'].split('-')
        lines.append(f"SP  - {start}")
        lines.append(f"EP  - {end}")

    lines.append(f"DO  - {item.get('DOI', '')}")
    lines.append("ER  - \n")

    return "\n".join(lines)

# Process references
not_found = []
success_count = 0

with open(output_ris_path, "w") as out:
    for i, ref in enumerate(references, 1):
        print(f"🔎 [{i}/{len(references)}] Searching: {ref[:70]}...")
        result = search_crossref(ref)
        if result:
            ris = convert_to_ris(result)
            out.write(ris + "\n")
            success_count += 1
        else:
            print("❌ Not found.")
            not_found.append(ref)
        time.sleep(1)  # Avoid API rate limits

# Save unmatched references
with open(not_found_path, "w") as nf:
    nf.write("\n".join(not_found))

# Final report
print("\n✅ Done.")
print(f"Matched: {success_count}")
print(f"Unmatched: {len(not_found)}")
if not_found:
    print("\nFirst few not found:")
    for nf in not_found[:5]:
        print(f" - {nf}")
