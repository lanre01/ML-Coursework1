#!/usr/bin/env python3
"""
Conservative notebook repair script.
Creates a backup: <notebook>.ipynb.bak
Finds the first occurrence of '"data": {' after a code cell source and removes the entire block up to the next '   "source": [' (start of following cell),
then inserts a close of the source array ("],") so the JSON becomes valid again.

Run from repo root (PowerShell):
python repair_nb_remove_data_block.py CW2\CW2_preprocessing.ipynb
"""
from pathlib import Path
import sys

START_MARKERS = ['\n     "data": {', '\n    "data": {', '\n   "data": {', '\n"data": {', '"data": {']
NEXT_SOURCE_MARKER = '\n   "source": ['


def find_start(text):
    for m in START_MARKERS:
        idx = text.find(m)
        if idx != -1:
            return idx, m
    return -1, None


def main():
    if len(sys.argv) < 2:
        print("Usage: python repair_nb_remove_data_block.py path/to/notebook.ipynb")
        sys.exit(1)
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"File not found: {p}")
        sys.exit(1)

    text = p.read_text(encoding='utf-8', errors='replace')
    bak = p.with_suffix(p.suffix + '.bak')
    bak.write_text(text, encoding='utf-8')
    print(f"Backup written to {bak}")

    idx, marker = find_start(text)
    if idx == -1:
        print("No 'data' block marker found. No changes made.")
        return
    print(f"Found marker {repr(marker)} at index {idx}")

    # find next occurrence of the next cell's source marker after idx
    pos_next_source = text.find(NEXT_SOURCE_MARKER, idx)
    if pos_next_source == -1:
        print("Couldn't find the following cell '   \"source\": [' marker after the data block. Aborting to avoid corrupting file.")
        return

    # We'll close the current source array by inserting '\n   ],' at idx, and remove the block in between
    prefix = text[:idx]
    suffix = text[pos_next_source:]

    repaired = prefix + '\n   ],' + suffix

    # Quick sanity check: ensure we haven't left the original marker
    if '"data": {' in repaired[idx: idx + 2000]:
        print("Warning: 'data' still present in repaired region. Aborting write.")
        return

    p.write_text(repaired, encoding='utf-8')
    print(f"Wrote repaired notebook to {p}")
    print("Please open the notebook in Jupyter. If something looks odd, restore the backup and share it for a more targeted repair.")


if __name__ == '__main__':
    main()
