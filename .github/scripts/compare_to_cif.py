"""Compare two outputs of cryspy_to_cif.py.

A changed CrysPy output is an error (exit 1); a changed str() of
pycifstar is only a warning (a fix of the writer may change it).

    python compare_to_cif.py <before.json> <after.json>
"""
import difflib
import json
import sys


def main(f_before, f_after):
    with open(f_before) as fid:
        before = json.load(fid)
    with open(f_after) as fid:
        after = json.load(fid)
    n_diff, n_error = 0, 0
    for f_name in sorted(set(before) | set(after)):
        for key in ("pycifstar", "cryspy"):
            text_1 = before.get(f_name, {}).get(key, "")
            text_2 = after.get(f_name, {}).get(key, "")
            if text_1 != text_2:
                n_diff += 1
                level = "error" if key == "cryspy" else "warning"
                n_error += (level == "error")
                print(f"::{level}::{key} output of {f_name} changed")
                diff = difflib.unified_diff(
                    text_1.splitlines(), text_2.splitlines(), "before",
                    "after", lineterm="", n=1)
                print("\n".join(list(diff)[:40]))
    print(f"{len(after)} files compared, {n_diff} outputs changed, "
          f"{n_error} of them by CrysPy")
    return 1 if n_error else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
