from My_prompts import PROMPTS, SYSTEMS
from My_techniques import apply_cot, majority_vote, self_refine

def solve(problem):
    """
    This is the main function that runs my agent.
    Basically I build a prompt depending on the domain, 
    optionally add some chain-of-thought cues, run a few model attempts,
    and then clean up the final answer.
    """
    domain = problem["domain"]
    question = problem["input"]

    # Build the base prompt for this domain
    base_prompt = PROMPTS[domain] + "\n\nProblem:\n" + question
    system = SYSTEMS[domain]
    cot_prompt = apply_cot(base_prompt, domain=domain)

    # I pick here the token limits and number of attempts per domain
    if domain == "math":
        max_tokens = 1024
        attempts = 3
    elif domain == "coding":
        max_tokens = 512
        attempts = 3
    else:
        max_tokens = 256
        attempts = 3

    # Here it runs a few samples and takes the most common answer
    candidate_answer = majority_vote(
        cot_prompt, 
        system=system, 
        domain=domain, 
        attempts=attempts,
        max_tokens=max_tokens
    )

    # Clean up the answer if needed
    final_answer = self_refine(question, candidate_answer, domain)

    return final_answer