# CSE476-NLP

Name: Revanth Kumar Alimela

GitHub Repo: https://github.com/ralimela/CSE476-NLP.git

## Overview

This project implements an inference-time reasoning agent that can answer problems across multiple domains such as math, commonsense, coding, planning, and future prediction. The agent does not train any model; instead, it improves reasoning quality by applying inference-time techniques on top of the provided LLM API.

My implementation is organized into multiple Python files for readability and modularity. The agent uses three inference-time techniques:

 - Domain-specific prompting + Chain-of-Thought (CoT)

 - Self-Consistency via Majority Voting

 - Self-Refinement (answer cleanup)

I chose these techniques to work together to encourage more stable, interpretable answers with fewer errors and less noise.


## File Structure

Below is an explanation of each file in my GitHub repository:

## My_agent.py

This is the main agent loop.
It performs:

 - Domain classification (detect_domain)

 - Builds the full prompt (PROMPTS[domain])

 - Applies Chain-of-Thought (apply_cot)

 - Performs majority voting (majority_vote)

 - Performs a final refinement pass (self_refine)

 Main Function here is - def solve(problem)   {This is the core entry point used by the test generation script}


## My_prompts.py

Contains domain-specific user prompts and system messages.

Example:

 - Math problems require step-by-step reasoning and a final answer.

 - Coding problems request raw Python code with no explanations.

 - Commonsense problems request a direct final answer.

These templates help guide the LLM’s behavior depending on the question.


## My_techniques.py

Implements the three inference-time techniques:

1. Chain-of-Thought: apply_cot(prompt, domain)
Adds simple reasoning cues such as “Let's solve this step by step.”
I only add them for math and planning, since other domains often do better with short answers.

2. Majority Voting: majority_vote(prompt, system, domain, attempts=3)
Runs the model multiple times and chooses the most common cleaned answer.
This reduces randomness and stabilizes predictions.

3. Self-Refinement: self_refine(question, answer, domain)
Asks the model to extract only the final answer from its own response.
Useful for removing full-sentence answers in commonsense questions.


## My_utils.py

Handles two things:

1. API Call Function: call_model(prompt, system, temperature, max_tokens)
A simple wrapper around the provided ASU /v1/chat/completions API.

2. Final Answer Extraction: extract_final_answer(text, domain)
Cleans and extracts final answers differently depending on the domain


## generate_answer_template.py

This script loads the final test set, calls solve(), and writes the output JSON in the exact format required by the auto-grader.

I only replaced the build_answers() logic so it calls my agent.


## Running Instructions

To run the agent on the final test data: python generate_answer_template.py


This produces: cse_476_final_project_answers.json

The file is validated automatically and ready for submission.

## Conclusion

My agent is simple, modular, and uses exactly three inference-time techniques. It follows all project rules, uses only the provided LLM API, and keeps the call budget low. While performance varies across domains, the agent works robustly and produces clean final answers suitable for auto-grading.