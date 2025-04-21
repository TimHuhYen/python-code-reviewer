import sys
from utils import get_py_files
from analyzer import analyze_file

if len(sys.argv) != 2:
    print("(Extremely Loud Wrong Buzzer) Usage: python review.py <folder or file_path>")
    sys.exit(1)

path = sys.argv[1]
files = get_py_files(path)

for file in files:
    print(f"Found Python file: {file}")
    issues = analyze_file(file)
    for issue in issues:
        print(f"[CODE] {issue}")