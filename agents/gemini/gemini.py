import os
import subprocess
import google.generativeai as genai
from typing import Annotated

# ============================================================================
# 1. Define Agent Tools (Functions the agent can call to interact with reality)
# ============================================================================

def read_file(file_path: str) -> str:
    """Reads the content of a file. Use this to inspect files before editing."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            # print(f"[Tool Execution] read_file({file_path}) -> {len(content)} bytes")
            return content
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(file_path: str, content: str) -> str:
    """Writes content to a file. Overwrites the file if it exists."""
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        # print(f"[Tool Execution] write_file({file_path})")
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {e}"

def execute_bash(command: str) -> str:
    """
    Executes a bash command and returns the standard output. 
    Can be used for things like creating directories, moving files, searching, or running curl for web requests.
    """
    # print(f"[Tool Execution] execute_bash:\n$ {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout if result.stdout else "Command executed successfully with no output."
    except subprocess.CalledProcessError as e:
        return f"Command failed with error code {e.returncode}. Error: {e.stderr}"

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

    # Configure the Gemini library
    genai.configure(api_key=api_key)

    # Initialize the model with our tools
    # We use gemini-2.5-flash as it is excellent at tool use and very fast
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        tools=[read_file, write_file, execute_bash]
    )

    # Start a chat session with automatic function calling enabled!
    # This means the SDK will automatically call our python functions above when the model requests them,
    # and feed the results straight back to the model without us having to write the loop manually.
    chat = model.start_chat(enable_automatic_function_calling=True)

    print("==========================================================")
    print("🤖 Gemini Agent Initialized")
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

            # Optional: You can inspect the chat history to see which tools it actually called!
            # for message in chat.history:
            #    print(message)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
