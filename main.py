import sys
from dotenv import load_dotenv
from src.agent import run_agent

load_dotenv(override=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py \"halal Turkish near Shoreditch\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"Query: {query}")

    result = run_agent(query)
    print("\n" + result)
