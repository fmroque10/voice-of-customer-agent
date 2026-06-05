# Simple MCP-style wrappers

def mcp_severity_tool(df, severity_tool):
    return severity_tool(df)


def mcp_trend_tool(df, trend_tool):
    return trend_tool(df)


def mcp_count_tool(df, count_complaints):
    return count_complaints(df)


def mcp_complaint_tool(df, get_complaints):
    return get_complaints(df)
