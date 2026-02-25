# Exercise 04: Code Refactoring and Analysis

## Objective
Evaluate how well the agent parses context syntax (specifically Python) and whether it can rewrite complex statements into clean, PEP-8 compliant code.

## Preparation
Create a file named `messy_script.py` containing a highly embedded/undesirable function:
```python
def calc(a,b,op):
  if op=='+': return a+b
  elif op=='-':return a-b
  elif op=='*':return a*b
  else:
   if op=='/':
    if b!=0: return a/b
    else: return "Err"
   else: return None
```

## Prompt to the Agent
> "Please review the script `messy_script.py`. Refactor it to be clean, idiomatic Python using a `match` statement (if available) or a dictionary mapping, include proper type hints, and write the result back into `clean_script.py`. Also handle the divide by zero gracefully with Python exceptions."

## Success Criteria
1. Agent reads `messy_script.py`.
2. Outputs beautiful Python code with `def calc(a: float, b: float, op: str) -> float | str:`.
3. Replaces deep nesting with simplified conditions.
4. Identifies to write it accurately back into `clean_script.py`.
