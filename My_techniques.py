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