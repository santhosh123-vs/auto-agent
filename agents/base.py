import time
from groq import Groq
from typing import Dict, Tuple
from config import GROQ_API_KEY, DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE


client = Groq(api_key=GROQ_API_KEY)


COST_PER_1K = {
    "llama-3.3-70b-versatile": {"input": 0.00059, "output": 0.00079},
    "llama-3.1-8b-instant": {"input": 0.00005, "output": 0.00008},
    "mixtral-8x7b-32768": {"input": 0.00024, "output": 0.00024},
}


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    costs = COST_PER_1K.get(model, {"input": 0.001, "output": 0.002})
    return round((input_tokens / 1000) * costs["input"] + (output_tokens / 1000) * costs["output"], 6)


class BaseAgent:
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.model = DEFAULT_MODEL

    def run(self, input_text: str, context: str = "") -> Tuple[str, Dict, float, float]:
        """
        Run the agent on input text.
        Returns: (output, tokens_used, cost, latency_ms)
        """
        full_input = input_text
        if context:
            full_input = f"CONTEXT FROM PREVIOUS AGENT:\n{context}\n\nCURRENT TASK:\n{input_text}"

        start = time.time()

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": full_input}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        latency_ms = (time.time() - start) * 1000

        output = response.choices[0].message.content
        tokens = {
            "input": response.usage.prompt_tokens,
            "output": response.usage.completion_tokens,
            "total": response.usage.total_tokens
        }
        cost = calculate_cost(self.model, tokens["input"], tokens["output"])

        return output, tokens, cost, latency_ms
