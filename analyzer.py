import ast

def analyze_file(filepath):
    # open file path in reading mode
    # universal decoding type 'utf-8'
    with open(filepath, "r", encoding="utf-8")as f:
        code = f.read()

    # try to turn it into tree
    try:
        tree = ast.parse(code, filename=filepath)
    except SyntaxError as e:
        return [f"SyntaxError in {filepath}: {e}"]
    
    issues = []

    # walk through node in tree
    # im walkin it
    for node in ast.walk(tree):
        # Case 1: long function
        if isinstance(node, ast.FunctionDef):
            if len(node.body) > 50:
                issues.append(
                    f"Function '{node.name}' is too long: {len(node.body)} lines (line {node.lineno})"
                )

        # Case 2: Global var 
        if isinstance(node, ast.Global):
            issues.append(
                f"Global variable used at line {node.lineno}"
            )

    return issues   