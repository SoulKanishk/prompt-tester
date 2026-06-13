import time
import yaml
import os
from groq import Groq
from dotenv import load_dotenv
from db import init_db, log_result

load_dotenv()
client = Groq(api_key=os.getenv(""))

def score_output(output, expected):
    output_lower = output.lower()
    if "label:" in output_lower:
        output_lower = output_lower.split("label:")[-1].strip()
    return 1.0 if expected in output_lower else 0.0

def run_variant(variant, test_case, runs=3):
    for _ in range(runs):
        prompt = variant["user_template"].format(input=test_case["input"])

        start = time.time()
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": variant["system"]},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
        )
        latency = (time.time() - start) * 1000

        output = response.choices[0].message.content.strip()
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        log_result({
            "variant_id": variant["id"],
            "input": test_case["input"],
            "output": output,
            "expected": test_case["expected"],
            "accuracy": score_output(output, test_case["expected"]),
            "latency_ms": round(latency, 1),
            "cost_usd": 0.0,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "model": "llama-3.1-8b-instant",
        })
        time.sleep(1)

if __name__ == "__main__":
    init_db()
    with open("prompts/variants.yaml") as f:
        config = yaml.safe_load(f)

    for variant in config["variants"]:
        print(f"Running variant: {variant['id']}")
        for test_case in config["test_cases"]:
            run_variant(variant, test_case)
        print(f"Done: {variant['id']}")

    print("\nAll variants complete! Open the dashboard.")