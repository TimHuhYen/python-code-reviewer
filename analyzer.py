import ast

def analyze_file(filepath):
    """
        Using the filepath, open it in reading mode and encode it into a AST:
            - Walk all noces in the AST
            - Append all "problems" into issues list
    """
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
                    f"WARNING: Function '{node.name}' is too long: {len(node.body)} lines (line {node.lineno})"
                )

        # Case 2: Global var 
        if isinstance(node, ast.Global):
            issues.append(
                f"WARNING: Global variable used at line {node.lineno}"
            )

        # Case 3: No docstring
        if isinstance(node, ast.FunctionDef):
            if ast.get_docstring(node) is None:
                issues.append(
                 f"WARNING: No docstring detected in function at line {node.lineno}"
                )

        # Case 4: Generational nested loops
        if isinstance(node, ast.AST):
            check_nesting(node, 0, issues)  

        # Case 5: Unused imports
        if isinstance(node, ast.FunctionDef):
            not_used_imports = check_unused_imports(tree)
            for name in not_used_imports:
                issues.append(f"WARNING: Unused import: '{name}'")

    return issues   



def check_nesting(node, current_depth, issues):
    """
        Walk through the AST node function body
            Search for nested loops/ifs/whiles within loops
    """
    # No loop really needs to pass 3
        # No shot you got a 4D matrix
    if current_depth > 3:
        # 'Store' object has no attribute 'lineno'
            # AST nodes issue
        line = getattr(node, 'lineno', '?') 
        issues.append(f"WARNING: Deep nested loop detected at line {line}")
        return

    # Iterate through child of AST
        # Recurse, searching for nested loops
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            check_nesting(child, current_depth + 1, issues)
        else:
            check_nesting(child, current_depth, issues)


def check_unused_imports(tree):
    """
        Traverse the AST tree for each node
        In each child node, check for Imports or ImportFrom
            AST library
        Create a set to store from each class
            Imported = set()
            Imported_From = set()
            Used_Import = set()
        Check for declared and used variables from the set in the script
    """
    imported = set()
    imported_from = set()
    used_imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported_from.add(alias.name)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_imports.add(node.id)

    unused_imports = [name for name in (imported | imported_from) if name not in used_imports]
    return unused_imports
