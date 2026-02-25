# Gemini Agent Evaluator & Exercise Plan

This repository contains a comprehensive plan for building small exercises to evaluate what a Gemini-based agent can do. The goal is to provide the agent with carefully scoped tasks (from simple to complex) and observe its capabilities, reasoning, and tool-use effectiveness.

## Objectives
1. **Assess Tool Use**: Verify if the agent accurately selects and uses tools like `read_file`, `write_file`, `run_command`, etc.
2. **Evaluate Reasoning**: Check how well the agent breaks down instructions and formulates a step-by-step plan.
3. **Safety & Guardrails**: Observe if the agent respects boundaries (e.g., executing potentially destructive commands).
4. **Context Window Limitations**: Test how well the agent retains information across multiple turns and files.

## Directory Structure
- [`diagrams/`](./diagrams/) - Contains Mermaid diagrams illustrating the overall architecture and exercise flow.
- [`exercises/`](./exercises/) - A suite of small evaluation tasks for the agent.
- `gemini.py` - The core script (assumed) to bootstrap or interact with the Gemini API/agent.

## Proposed Exercises

| Exercise | Description | Target Capabilities | Difficulty |
|----------|-------------|---------------------|------------|
| **01 Basic Math** | Ask the agent to read two numbers from a file, add them, and write the output. | File I/O, Basic logic | 🟢 Easy |
| **02 File Manipulation**| Ask the agent to organize a messy directory by file extension into subfolders. | Bash scripting, Tool usage | 🟡 Medium |
| **03 Web Search** | Ask the agent to look up today's weather or recent news and summarize it. | HTTP requests, Web scraping/search | 🟡 Medium |
| **04 Code Refactoring** | Provide a heavily nested, inefficient Python script and ask the agent to refactor it. | Code analysis, Python | 🔴 Hard |

## How to Run

**1. Setup Environment**
Run the following commands in the root of the project to create a Python virtual environment and install the required dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**2. Configure API Key**
Export your Gemini API key in the terminal session:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**3. Start the Agent**
Run the interactive agent script:
```bash
python gemini.py
```

**4. Test an Exercise**
- Read the prompt from one of the exercises (e.g. `exercises/01_basic_math/README.md`).
- Feed the prompt to the running Gemini agent.
- Evaluate the agent's output against the expected results documented in the exercise.
---

*See the `diagrams/` folder for visual workflows detailing how the agent parses instructions and executes tasks.*
