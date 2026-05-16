from mcp.server.fastmcp import FastMCP

mcp = FastMCP("math")

@mcp.tool()
def add(n1: float, n2: float) -> float:
    """ Add two numbers together. """
    return n1 + n2

@mcp.tool()
def multiply(n1: float, n2: float) -> float:
    """ Multiply two numbers together. """
    return n1 * n2

@mcp.tool()
def subtract(n1: float, n2: float) -> float:
    """ Subtract two numbers. """
    return n1 - n2

@mcp.tool()
def divide(n1: float, n2: float) -> float:
    """ Divide two numbers. """
    if n2 == 0:
        raise ValueError("Cannot divide by zero.")
    return n1 / n2

@mcp.tool()
def power(base: float, exponent: float) -> float:
    """ Raise a number to a power. """
    return base ** exponent

mcp.run(transport="stdio")