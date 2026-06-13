# ⚽ Football Prompt A/B Testing Dashboard

A data-driven tool to scientifically compare prompt engineering strategies on football sentiment analysis using LLMs.

Built by **Kanishk Singh** | B.Tech IT @ I2IT Pune

---

## 🔍 What it does

Most people use LLMs by guessing which prompt works best. This tool measures it.

It tests 3 different prompt strategies on the same football news headlines and compares them across:
- ✅ Accuracy (does the model classify correctly?)
- ⚡ Latency (how fast does it respond?)
- 💰 Cost (how many tokens does it use?)

---

## 📊 Results (Sample)

| Variant | Accuracy | Avg Latency |
|---|---|---|
| v1_zero_shot | 83.3% | 363 ms |
| v2_fan_perspective | 72.0% | 1024 ms |
| v3_expert_cot | 83.3% | 2100 ms |

**Key insight:** Zero-shot matched expert chain-of-thought accuracy at 3x the speed. Fan-perspective framing reduced accuracy by 11%, showing emotional framing introduces bias in LLM outputs.

---

## 🛠️ Tech Stack

- **Python** — core logic
- **Groq API** — LLM inference (Llama 3.1)
- **SQLite** — results storage
- **Streamlit** — interactive dashboard
- **Plotly** — charts
- **YAML** — prompt version control

---

## 📁 Project Structure
prompt-tester/

├── prompts/

│   └── variants.yaml     ← prompt versions live here

├── evals/

│   └── scorers.py        ← accuracy scoring functions

├── runner.py             ← calls LLM, logs results

├── dashboard.py          ← Streamlit dashboard

├── db.py                 ← SQLite setup

└── requirements.txt
---

## 🚀 How to run

**1. Clone the repo**
```bash
git clone https://github.com/SoulKanishk/prompt-tester.git
cd prompt-tester
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Groq API key**

Create a `.env` file:GROQ_API_KEY=your_key_here

Get a free key at [console.groq.com](https://console.groq.com)

**4. Run the tests**
```bash
python runner.py
```

**5. Launch the dashboard**
```bash
streamlit run dashboard.py
```

---

## 💡 Prompt Design Decisions

| Variant | Strategy | Why I tested it |
|---|---|---|
| v1_zero_shot | Direct classification | Baseline — minimal instruction |
| v2_fan_perspective | Emotional role-play | Tests if persona affects accuracy |
| v3_expert_cot | Step-by-step reasoning | Tests if reasoning improves output |

**What I learned:** For simple classification tasks, zero-shot is optimal. Chain-of-thought adds latency without accuracy gains. Emotional personas introduce bias.

---

## 📬 Connect

- LinkedIn: [Kanishk Singh](https://linkedin.com/in/your-profile)
- GitHub: [SoulKanishk](https://github.com/SoulKanishk)
