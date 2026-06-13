import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_summary, init_db

init_db()
st.set_page_config(page_title="Prompt A/B Tester", layout="wide")
st.title("Prompt A/B Testing Dashboard")

summary = get_summary()
if not summary:
    st.info("No results yet. Run `python runner.py` first.")
    st.stop()

df = pd.DataFrame(summary)

# ── Metric cards ──────────────────────────────────────────
best_acc = df.loc[df.avg_accuracy.idxmax(), "variant_id"]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Variants tested", len(df))
col2.metric("Best accuracy", f"{df.avg_accuracy.max()}%", f"({best_acc})")
col3.metric("Fastest (avg)", f"{df.avg_latency_ms.min():.0f} ms")
col4.metric("Cheapest total", f"${df.total_cost.min():.5f}")

st.divider()

# ── Charts ────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("Accuracy")
    fig = px.bar(df, x="variant_id", y="avg_accuracy",
                 color="avg_accuracy", color_continuous_scale="Teal",
                 labels={"avg_accuracy": "%", "variant_id": ""})
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Latency (ms)")
    fig = px.bar(df, x="variant_id", y="avg_latency_ms",
                 color="avg_latency_ms", color_continuous_scale="Reds_r",
                 labels={"avg_latency_ms": "ms", "variant_id": ""})
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with c3:
    st.subheader("Total cost ($)")
    fig = px.bar(df, x="variant_id", y="total_cost",
                 color="total_cost", color_continuous_scale="Purples",
                 labels={"total_cost": "USD", "variant_id": ""})
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Recommendation ────────────────────────────────────────
st.subheader("Recommendation")
# Score: normalise each metric, weight accuracy highest
df["score"] = (
    df.avg_accuracy / df.avg_accuracy.max() * 0.6 +
    (1 - df.avg_latency_ms / df.avg_latency_ms.max()) * 0.2 +
    (1 - df.total_cost / df.total_cost.max()) * 0.2
)
winner = df.loc[df.score.idxmax()]
st.success(f"Winner: **{winner.variant_id}** — {winner.avg_accuracy}% accuracy, "
           f"{winner.avg_latency_ms:.0f} ms avg latency, ${winner.total_cost:.5f} total cost")

# ── Raw data ──────────────────────────────────────────────
with st.expander("Raw data"):
    st.dataframe(df, use_container_width=True)
    st.download_button("Export CSV", df.to_csv(index=False), "results.csv")