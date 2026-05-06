from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression.
    Input must be a valid Python math expression, e.g. '2 + 2', '10 * 5 / 2', '3 ** 4'.
    Do NOT pass words — only numbers and operators.
    """
    allowed_names = {
        "abs": abs, "round": round, "min": min, "max": max,
        "pow": pow, "sum": sum,
    }
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"
