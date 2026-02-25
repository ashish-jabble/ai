import os
import subprocess
from google import genai
from google.genai import types

# ============================================================================
# 1. Define Agent Tools (Functions the agent can call to interact with reality)
# ============================================================================

def read_file(file_path: str) -> str:
    """Reads the content of a file. Use this to inspect files before editing."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            return content
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(file_path: str, content: str) -> str:
    """Writes content to a file. Overwrites the file if it exists."""
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {e}"

def execute_bash(command: str) -> str:
    """
    Executes a bash command and returns the standard output. 
    Can be used for things like creating directories, moving files, searching, or running curl requests.
    NOTE: Automatically times out after 15 seconds. Use explicit error handling in your commands if needed.
    """
    try:
        # Added timeout to prevent the agent from hanging infinitely on bad curls/commands!
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True, timeout=15)
        return result.stdout if result.stdout else "Command executed successfully with no output."
    except subprocess.TimeoutExpired:
        return f"Command failed: Timed out after 15 seconds. Are you hanging on a network request without an explicit timeout?"
    except subprocess.CalledProcessError as e:
        return f"Command failed with error code {e.returncode}. Error: {e.stderr}"
    except Exception as e:
        return f"Command execution error: {e}"

# ============================================================================
# 2. Setup the Agent Loop
# ============================================================================

def main():
    # Ensure the user has their API key set
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not found.")
        print("Please run: export GEMINI_API_KEY='your-api-key-here'")
        return

    # Initialize the new SDK client
    client = genai.Client(api_key=api_key)
    
    # Configure the Gemini library (gemini-2.5-flash is excellent at tool use)
    config = types.GenerateContentConfig(
        tools=[read_file, write_file, execute_bash],
        system_instruction=(
            "You are an autonomous AI agent with access to the user's terminal via the execute_bash tool. "
            "If the user asks for live information or web content, DO NOT say you lack internet access. "
            "Instead, use the execute_bash tool to run `curl` to fetch and parse the requested data from the internet. "
            "IMPORTANT: When running `curl`, strongly prefer appending `-sL` to silence the progress bar and follow redirects."
        ),
        # Automatically invoke exactly one or more tools repeatedly until it formulates an answer
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
    )

    # Start a chat session!
    chat = client.chats.create(model='gemini-2.5-flash', config=config)

    print("==========================================================")
    print("🤖 Gemini Agent Initialized (using new google-genai SDK)")
    print("Tools Available: read_file, write_file, execute_bash")
    print("Type 'exit' to quit.")
    print("==========================================================\n")

    while True:
        try:
            prompt = input("\n👤 You: ")
            if prompt.strip().lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            if not prompt.strip():
                continue

            print("\n🤖 Agent is thinking... (and possibly executing tools)")
            
            # Send the message to the model
            response = chat.send_message(prompt)
            
            # Print the final response
            print(f"\n🤖 Agent: {response.text}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
