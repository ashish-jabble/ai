# Exercise 03: Web Search and Summary

## Objective
Assess the agent's capability to search the web for real-time information and synthesize it meaningfully.

## Preparation
No formal setup necessary. Just run the agent with internet connectivity.

## Prompt to the Agent
> "Find the latest major tech news headlines from the past hour and summarize the top 3 with bullet points."

## Success Criteria
1. Agent executes a relevant web search query / curl request.
2. Agent parses HTML/JSON responses from its tools.
3. Summary is concise and strictly reflects the recent period requested.

## Failure Criteria
1. Synthesizing out-of-date or hallucinated information based purely on its training knowledge.
2. Refusing or failing to use internal HTTP request tools natively.
