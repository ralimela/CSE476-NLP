PROMPTS = {
    "math": (
        "Solve this math problem step by step. Show your reasoning clearly. "
        "At the end, put your final numerical answer inside \\boxed{}, "
        "for example: \\boxed{42}"
    ),

    "common_sense": (
        "Answer this question directly and concisely. "
        "Give only the final answer."
    ),

    "coding": (
        "Write the Python code to complete this task. "
        "Return ONLY the code, no explanations or markdown."
    ),

    "planning": (
        "Find the sequence of actions to achieve the goal. "
        "Output one action per line in the format: (action arg1 arg2)"
    ),

    "future_prediction": (
        "Make your best prediction based on available information. "
        "End your answer with \\boxed{your_prediction}"
    ),
}

# System messages per domain
SYSTEMS = {
    "math": "You are a math expert. Think step by step and show your work.",
    "common_sense": "You are a knowledgeable assistant. Give direct answers.",
    "coding": "You are an expert Python programmer. Write clean, correct code.",
    "planning": "You are a planning agent. Output only the action sequence.",
    "future_prediction": "You are a forecasting assistant. Make reasonable predictions.",
}