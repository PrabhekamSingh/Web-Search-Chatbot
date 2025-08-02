from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()

# Initialize Tavily Search Tool
@tool
def tavily_search_tool(query: str) -> str:
    """Search the web using Tavily for current information."""
    tavily_search = TavilySearch(
        max_results=5,
        api_key=os.getenv("TAVILY_API_KEY")  # Make sure you have this in your .env file
    )
    try:
        results = tavily_search.invoke({"query": query})
        return f"Search results for '{query}': {results}"
    except Exception as e:
        return f"Search failed: {str(e)}"

# Define the tools list
tools = [tavily_search_tool]

# Initialize LLM with tools
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",  # Updated model name
    temperature=0.1,
    max_tokens=1000,
    google_api_key=os.getenv("GOOGLE_API_KEY")
).bind_tools(tools=tools)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    """Main chat node that processes messages and can call tools."""
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

def tool_node(state: ChatState):
    """Node to execute tool calls."""
    messages = state['messages']
    last_message = messages[-1]
    
    # Execute tool calls if present
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        tool_outputs = []
        for tool_call in last_message.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            
            if tool_name == 'tavily_search_tool':
                result = tavily_search_tool.invoke(tool_args)
                tool_outputs.append({
                    "tool_call_id": tool_call['id'],
                    "output": result
                })
        
        # Create tool message
        from langchain_core.messages import ToolMessage
        tool_messages = [
            ToolMessage(content=output["output"], tool_call_id=output["tool_call_id"])
            for output in tool_outputs
        ]
        return {"messages": tool_messages}
    
    return {"messages": []}

def should_continue(state: ChatState):
    """Determine if we should continue to tool execution or end."""
    messages = state['messages']
    last_message = messages[-1]
    
    # If the last message has tool calls, go to tool node
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    # Otherwise, end the conversation
    return END

# Create the graph
graph = StateGraph(ChatState)

# Add nodes
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

# Add edges
graph.add_edge(START, "chat_node")
graph.add_conditional_edges(
    "chat_node",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)
graph.add_edge("tools", "chat_node")

# Compile with checkpointer
checkpointer = InMemorySaver()
chatbot = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    # Example usage with proper message format
    config = {"configurable": {"thread_id": "1"}}
    
    # Create proper HumanMessage instead of string
    initial_state = {
        "messages": [HumanMessage(content="Hi, how's the weather today in Hyderabad?")]
    }
    
    try:
        response = chatbot.invoke(initial_state, config=config)
        print("Response messages:")
        for msg in response['messages']:
            print(f"- {type(msg).__name__}: {msg.content}")
    except Exception as e:
        print(f"Error: {e}")
        
    # Example of continuing the conversation
    print("\n" + "="*50 + "\n")
    
    follow_up_state = {
        "messages": [HumanMessage(content="What about the weather in Mumbai?")]
    }
    
    try:
        response2 = chatbot.invoke(follow_up_state, config=config)
        print("Follow-up response:")
        for msg in response2['messages']:
            print(f"- {type(msg).__name__}: {msg.content}")
    except Exception as e:
        print(f"Error: {e}")