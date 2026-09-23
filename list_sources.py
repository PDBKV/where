import sys, pathlib

# Every Fortran extension you use. Case matters: .f and .F are different entries.
EXTS = {".f", ".F", ".for", ".f90"}

folder = pathlib.Path(sys.argv[1])
found = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix in EXTS)
print("\n".join(str(p) for p in found))
