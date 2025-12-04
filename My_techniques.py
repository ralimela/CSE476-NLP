from My_utils import call_model, extract_final_answer

def apply_cot(prompt, domain="math"):
    """
    Here it adds a simple Chain-of-Thought cue depending on the domain.
    I only add it for math and planning since those benefit the most.
    """
    if domain == "math":
        #I tried to do step-by-step reasoning for math problems
        return prompt + "\n\nLet's solve this step by step."
    elif domain == "planning":
        return prompt + "\n\nLet's think about what actions are needed."
    else:
        # For other domains I just kept the prompt as-is
        return prompt


def majority_vote(prompt, system, domain, attempts=3, temperature=0.7, max_tokens=512):
    """
    This runs the model multiple times and picks the most common answer.
    Basically if the model answers the same thing more than once, it's probably the correct one.
    """
    answers = []
    
    for _ in range(attempts):
        raw = call_model(prompt, system=system, temperature=temperature, max_tokens=max_tokens)
        cleaned = extract_final_answer(raw, domain=domain)
        answers.append(cleaned)
    
    # Return most frequent answer
    if answers:
        return max(set(answers), key=answers.count)
    return ""


def self_refine(question, answer, domain):
    """
    Here I am asking the model to clean up its own answer.
    I mostly use this to trim long, sentence-like answers into the final.
    Coding and planning don't need this since their output format is fixed.
    """
    
    if domain in ["coding", "planning"]:
        return answer
    
    # Ask the model to extract only the final short answer
    refine_prompt = f"""I answered a question earlier but the response might be too long.
    Please extract ONLY the final answer (no explanation).

    Question: {question}
    My Answer: {answer}

    Return ONLY the exact answer (a number, name, or short phrase). Nothing else."""

    system = "You are a precise assistant. Return only the extracted answer, nothing more."
    
    refined = call_model(refine_prompt, system=system, temperature=0.0, max_tokens=64)
    
    # Clean up the refined answer
    refined = refined.strip().strip('"').strip("'").strip('.')
    
    # If refinement failed or returned empty, this keeps the original output
    if not refined or len(refined) > len(answer) * 2:
        return answer
    
    return refined