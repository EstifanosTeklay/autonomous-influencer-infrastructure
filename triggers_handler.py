# triggers_handler.py

def handle_trigger(event, call_tool):
    """
    event: dict with keys like 'type' and 'data'
    call_tool: function to call MCP tools
    """

    if event["type"] == "performance_outlier":
        response = call_tool("log_performance_outlier_trigger", event["data"])
        print("*****************************************")
        print("Analysis Feedback:", response.get("summary", "No summary"))
        print("Statistics:", response.get("stats", "No stats"))
        print("*****************************************")

    elif event["type"] == "passage_time":
        response = call_tool("log_passage_time_trigger", event["data"])
        # Do not display response, just process internally
        process_passage_time(response)


def process_passage_time(response):
    # Internal handling only, no user output
    pass
