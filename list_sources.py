import argparse, pathlib

p = argparse.ArgumentParser()
p.add_argument("folder")
p.add_argument("skip", nargs="*", help="file names to leave out")
p.add_argument("--ext", action="append", help="extension to match (repeatable)")
a = p.parse_args()

exts = set(a.ext or [".f", ".F", ".for", ".f90"])   # Fortran by default
found = sorted(q for q in pathlib.Path(a.folder).iterdir()
               if q.is_file() and q.suffix in exts and q.name not in a.skip)
print("\n".join(str(q) for q in found))