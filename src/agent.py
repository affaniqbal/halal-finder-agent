import os
import anthropic
from src.tools import TOOL_DEFINITIONS, run_tool


def run_agent(query: str) -> str:
    """
    Run the halal restaurant finder agent.
    Takes a natural language query, calls tools as needed, returns a final answer.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    system_prompt = """You are a halal restaurant finder agent for London.
Your job is to help users find halal restaurants based on their query.

When finding restaurants:
1. Search for restaurants matching the query
2. For promising results, get place details to check for halal mentions in reviews
3. Assess halal status as one of:
   - LIKELY HALAL: multiple reviews confirm halal, or restaurant explicitly markets as halal
   - POSSIBLY HALAL: some halal mentions but limited evidence
   - UNVERIFIED: no halal information found — may still be halal but cannot confirm
4. Return a clean, structured list of results with name, address, halal status, rating, and maps link

Be honest about uncertainty. Do not claim a restaurant is halal unless there is clear evidence."""

    messages = [{"role": "user", "content": query}]

    print(f"\nAgent thinking...\n")

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            system=system_prompt,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        # If the model wants to use tools
        if response.stop_reason == "tool_use":
            # Add assistant's response to messages
            messages.append({"role": "assistant", "content": response.content})

            # Process each tool call
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  Calling tool: {block.name}({block.input})")
                    result = run_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            # Add tool results to messages
            messages.append({"role": "user", "content": tool_results})

        # If the model is done
        elif response.stop_reason == "end_turn":
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text
            return final_text

        else:
            return f"Unexpected stop reason: {response.stop_reason}"
