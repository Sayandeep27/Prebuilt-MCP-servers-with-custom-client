import asyncio
import os

# Load environment variables from .env file
from dotenv import load_dotenv

# LangChain OpenAI chat model
from langchain_openai import ChatOpenAI

# MCP client that can connect to MULTIPLE MCP servers
from langchain_mcp_adapters.client import MultiServerMCPClient

# LangGraph imports for agent workflow
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

# -----------------------------------------------------
# Load environment variables
# -----------------------------------------------------
load_dotenv()


async def main():
    """
    Main async entry point for the MCP-powered agent.
    This function:
    - Connects to MCP servers
    - Fetches tools
    - Builds a LangGraph agent
    - Runs an interactive CLI loop
    """

    # -------------------------------------------------
    # Read API keys from environment variables
    # -------------------------------------------------
    openai_key = os.getenv("OPENAI_API_KEY")
    owm_key = os.getenv("OWM_API_KEY")

    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found in .env or environment variables.")

    if not owm_key:
        raise ValueError("OWM_API_KEY not found in .env or environment variables.")

    # -------------------------------------------------
    # Configure MCP servers
    # -------------------------------------------------
    # Each MCP server runs as a separate PROCESS.
    # Communication happens via stdio.
    # -------------------------------------------------
    client = MultiServerMCPClient(
        {
            # -------- Weather MCP Server (Go binary) --------
            "weather": {
                "transport": "stdio",
                "command": "E:/langraph_mcp-demo/mcp-openweather/mcp-weather.exe",
                "args": [],
                # Pass API key as environment variable
                "env": {
                    "OWM_API_KEY": owm_key
                }
            },

            # -------- Calculator MCP Server (Python module) --------
            "calculator": {
                "transport": "stdio",
                "command": "python",
                "args": ["-m", "mcp_server_calculator"]
            }
        }
    )

    # -------------------------------------------------
    # Fetch tools exposed by ALL MCP servers
    # -------------------------------------------------
    # This dynamically converts MCP tools → LangChain tools
    tools = await client.get_tools()

    # -------------------------------------------------
    # Initialize the LLM
    # -------------------------------------------------
    # The model does NOT know how to calculate or fetch weather.
    # It only decides WHEN to call tools.
    model = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openai_key
    )

    # -------------------------------------------------
    # LLM Node: decides whether to answer or call a tool
    # -------------------------------------------------
    def call_model(state: MessagesState):
        """
        This node:
        - Sends conversation history to the LLM
        - Allows the LLM to call MCP tools
        """
        response = model.bind_tools(tools).invoke(state["messages"])
        return {"messages": response}

    # -------------------------------------------------
    # Build LangGraph workflow
    # -------------------------------------------------
    builder = StateGraph(MessagesState)

    # Add nodes
    builder.add_node("call_model", call_model)
    builder.add_node("tools", ToolNode(tools))

    # Entry point
    builder.add_edge(START, "call_model")

    # Conditional routing:
    # If the LLM requests a tool → go to ToolNode
    # Else → end
    builder.add_conditional_edges(
        "call_model",
        tools_condition
    )

    # After tool execution, return back to LLM
    builder.add_edge("tools", "call_model")

    # Compile the graph
    graph = builder.compile()

    print("\n✅ MCP Agent Ready!")
    print("Type weather questions or math queries.")
    print("Type 'exit' or 'quit' to stop.")

    # -------------------------------------------------
    # Interactive CLI loop
    # -------------------------------------------------
    while True:
        user_question = input("\nAsk me anything → ")

        if user_question.strip().lower() in ["exit", "quit"]:
            print("Goodbye 👋")
            break

        print("\n🤖 Agent is thinking...\n")

        # Invoke LangGraph asynchronously
        result = await graph.ainvoke(
            {"messages": user_question}
        )

        # Print final response
        print("🧠 Answer:")
        print(result["messages"][-1].content)


# -----------------------------------------------------
# Script entry point
# -----------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
