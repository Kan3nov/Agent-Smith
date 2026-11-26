try:
    from mcp.server import MCPServer
except Exception as e:
    print("=" * 5, "Import Error", "=" * 5)
    print(e)
    exit()

mcp = MCPServer("mbpp")


@mcp.tool()
def run_tests(code: str, test_list: list[str]):
    results = {}
    exec(code)
    results["success"] = True
    for test in test_list:
        try:
            exec(test)
        except AssertionError:
            results["success"] = False
    return str(results)


if __name__ == "__main__":
    mcp.run(transport="stdio")
