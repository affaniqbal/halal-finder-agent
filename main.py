import sys
import json
import subprocess
from dotenv import load_dotenv
from src.agent import run_agent
from src.renderer import render_html

load_dotenv(override=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py \"halal Turkish near Shoreditch\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"Query: {query}")

    raw = run_agent(query)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Extract JSON if the model wrapped it in markdown code fences
        import re
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
        else:
            print("\nAgent response (could not parse as JSON):\n")
            print(raw)
            sys.exit(1)

    output_file = render_html(data)
    print(f"\nResults saved to {output_file}")
    subprocess.run(["open", output_file])
