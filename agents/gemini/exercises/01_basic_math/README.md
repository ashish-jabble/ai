# Exercise 01: Basic Math & File I/O

## Objective
Verify the agent can correctly identify target files, extract text-based number representations, perform logic on them, and output to a new file accurately.

## Preparation
Create a setup that produces a file. E.g.:
```bash
echo "187, 423" > input_numbers.txt
```

## Prompt to the Agent
> "Read the two numbers from the file `input_numbers.txt`. Add them together and write the sum into a new file named `solution.txt`."

## Success Criteria
1. Agent queries the file `input_numbers.txt`.
2. Agent reads the numerical contents correctly (610).
3. Agent writes `610` to `solution.txt`.
4. Agent responds that the task is complete.

## Failure Criteria
1. Agent hallucinates the output without reading the file.
2. Agent tries to write incorrect strings to the final file.
