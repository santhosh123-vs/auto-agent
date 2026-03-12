import streamlit as st
import requests
import json
import time
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="AutoAgent Dashboard",
    page_icon="\U0001f916",
    layout="wide"
)

API_URL = "https://auto-agent-9th8.onrender.com"


st.markdown("""
<style>
    .main-header {font-size: 2.5rem; font-weight: 700; text-align: center; margin-bottom: 0;}
    .sub-header {font-size: 1.1rem; color: #666; text-align: center; margin-bottom: 2rem;}
    .agent-card {padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;}
    .step-done {border-left: 4px solid #28a745; padding-left: 1rem; margin: 1rem 0;}
    .step-fail {border-left: 4px solid #dc3545; padding-left: 1rem; margin: 1rem 0;}
</style>
""", unsafe_allow_html=True)


def run_workflow(task, context=None, agents=None):
    try:
        payload = {"task": task}
        if context:
            payload["context"] = context
        if agents:
            payload["agents"] = agents
        return requests.post(f"{API_URL}/api/v1/workflow", json=payload, timeout=120).json()
    except Exception as e:
        return {"error": str(e)}


def get_summary():
    try:
        return requests.get(f"{API_URL}/api/v1/summary", timeout=10).json()
    except:
        return None


def get_history(limit=10):
    try:
        return requests.get(f"{API_URL}/api/v1/workflows?limit={limit}", timeout=10).json()
    except:
        return None


def get_agents():
    try:
        return requests.get(f"{API_URL}/api/v1/agents", timeout=10).json()
    except:
        return None


with st.sidebar:
    st.markdown("## \U0001f916 AutoAgent")
    st.markdown("Multi-Agent Orchestration")
    st.markdown("---")
    page = st.radio("Navigate", [
        "\U0001f680 Run Workflow",
        "\U0001f4ca Dashboard",
        "\U0001f4cb History",
        "\U0001f916 Agents Info"
    ])
    st.markdown("---")
    st.markdown("**Built by Kethavath Santhosh**")
    st.markdown("[GitHub](https://github.com/santhosh123-vs)")


if page == "\U0001f680 Run Workflow":
    st.markdown('<p class="main-header">\U0001f680 Run Multi-Agent Workflow</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Chain AI agents to complete complex tasks</p>', unsafe_allow_html=True)

    task = st.text_area(
        "What do you want the agents to do?",
        placeholder="Example: Research the latest trends in renewable energy and write a professional report with recommendations",
        height=100
    )

    context = st.text_area(
        "Additional context (optional)",
        placeholder="Any specific focus, constraints, or background information",
        height=80
    )

    st.markdown("### Select Agents")
    st.markdown("Choose which agents to use and their order:")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        use_researcher = st.checkbox("\U0001f50d Researcher", value=True)
        st.caption("Gathers information")
    with col2:
        use_analyzer = st.checkbox("\U0001f4ca Analyzer", value=True)
        st.caption("Analyzes data")
    with col3:
        use_writer = st.checkbox("\u270d\ufe0f Writer", value=True)
        st.caption("Creates content")
    with col4:
        use_reviewer = st.checkbox("\u2705 Reviewer", value=True)
        st.caption("Reviews quality")

    agents = []
    if use_researcher:
        agents.append("researcher")
    if use_analyzer:
        agents.append("analyzer")
    if use_writer:
        agents.append("writer")
    if use_reviewer:
        agents.append("reviewer")

    if st.button("\U0001f680 Run Workflow", type="primary", use_container_width=True):
        if not task:
            st.warning("Please enter a task!")
            st.stop()
        if not agents:
            st.warning("Please select at least one agent!")
            st.stop()

        st.markdown("---")
        st.markdown("### Workflow Execution")

        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.markdown(f"\U0001f504 Starting workflow with {len(agents)} agents...")
        progress_bar.progress(10)

        with st.spinner("Agents are working..."):
            result = run_workflow(task, context if context else None, agents)

        progress_bar.progress(100)

        if "error" in result:
            st.error(f"Workflow failed: {result['error']}")
            st.stop()

        status_text.markdown(f"\u2705 Workflow completed!")

        # Summary metrics
        st.markdown("### Results Summary")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Status", result.get("status", "unknown"))
        with m2:
            st.metric("Total Cost", f"${result.get('total_cost_usd', 0):.6f}")
        with m3:
            st.metric("Total Time", f"{result.get('total_latency_ms', 0):.0f}ms")
        with m4:
            total_tok = result.get("total_tokens", {})
            st.metric("Total Tokens", total_tok.get("total", 0))

        st.markdown("---")

        # Agent execution trace
        st.markdown("### Agent Execution Trace")

        steps = result.get("steps", [])
        for i, step in enumerate(steps):
            status_icon = "\u2705" if step.get("status") == "completed" else "\u274c"
            
            with st.expander(f"{status_icon} Step {i+1}: {step.get('agent_name', 'Unknown')} ({step.get('latency_ms', 0):.0f}ms)", expanded=(i == len(steps)-1)):
                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    st.metric("Tokens", step.get("tokens_used", {}).get("total", 0))
                with sc2:
                    st.metric("Cost", f"${step.get('cost_usd', 0):.6f}")
                with sc3:
                    st.metric("Latency", f"{step.get('latency_ms', 0):.0f}ms")
                
                st.markdown("**Output:**")
                st.markdown(step.get("output_text", "No output"))

        st.markdown("---")

        # Final output
        st.markdown("### Final Output")
        st.markdown(result.get("final_output", "No output"))

        # Download
        st.markdown("### Download")
        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                "\U0001f4c4 Download as TXT",
                data=result.get("final_output", ""),
                file_name=f"autoagent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with dl2:
            st.download_button(
                "\U0001f4be Download Full JSON",
                data=json.dumps(result, indent=2),
                file_name=f"autoagent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )


elif page == "\U0001f4ca Dashboard":
    st.markdown('<p class="main-header">\U0001f4ca AutoAgent Dashboard</p>', unsafe_allow_html=True)

    summary = get_summary()

    if not summary:
        st.error("Cannot connect to AutoAgent server. Make sure it is running on port 8001.")
        st.stop()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Workflows", summary.get("total_workflows", 0))
    with col2:
        st.metric("Total Cost", f"${summary.get('total_cost', 0):.6f}")
    with col3:
        st.metric("Total Tokens", summary.get("total_tokens_used", 0))
    with col4:
        st.metric("Avg Latency", f"{summary.get('average_latency_ms', 0):.0f}ms")

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Workflows by Status")
        status_data = summary.get("workflows_by_status", {})
        if status_data:
            st.bar_chart(pd.DataFrame({
                "Status": list(status_data.keys()),
                "Count": list(status_data.values())
            }).set_index("Status"))
        else:
            st.info("No workflows yet")

    with c2:
        st.markdown("### Agent Usage")
        agent_data = summary.get("agents_usage", {})
        if agent_data:
            st.bar_chart(pd.DataFrame({
                "Agent": list(agent_data.keys()),
                "Times Used": list(agent_data.values())
            }).set_index("Agent"))
        else:
            st.info("No agent usage yet")


elif page == "\U0001f4cb History":
    st.markdown('<p class="main-header">\U0001f4cb Workflow History</p>', unsafe_allow_html=True)

    history = get_history(20)

    if history and history.get("workflows"):
        workflows = history["workflows"]
        st.markdown(f"**Total workflows:** {history.get('total', 0)}")

        for w in reversed(workflows):
            status_icon = "\u2705" if w.get("status") == "completed" else "\u274c"
            with st.expander(f"{status_icon} {w.get('task', 'Unknown')[:80]}... | ${w.get('total_cost_usd', 0):.6f} | {w.get('total_latency_ms', 0):.0f}ms"):
                st.markdown(f"**ID:** {w.get('workflow_id', '')}")
                st.markdown(f"**Agents:** {w.get('agents_used', 0)}")
                st.markdown(f"**Tokens:** {w.get('total_tokens', {}).get('total', 0)}")
                st.markdown(f"**Created:** {w.get('created_at', '')[:19]}")
                st.markdown("---")
                st.markdown("**Final Output:**")
                st.markdown(w.get("final_output", "")[:1000])
    else:
        st.info("No workflows yet. Run your first workflow!")


elif page == "\U0001f916 Agents Info":
    st.markdown('<p class="main-header">\U0001f916 Available Agents</p>', unsafe_allow_html=True)

    agents_data = get_agents()

    if agents_data:
        agent_icons = {
            "researcher": "\U0001f50d",
            "analyzer": "\U0001f4ca",
            "writer": "\u270d\ufe0f",
            "reviewer": "\u2705"
        }

        for name, info in agents_data.items():
            icon = agent_icons.get(name, "\U0001f916")
            with st.expander(f"{icon} {info.get('name', name)}", expanded=True):
                st.markdown(f"**Role:** {info.get('role', '')}")
                st.markdown(f"**Model:** {info.get('model', '')}")
                st.markdown(f"**Description:** {info.get('description', '')}")

        st.markdown("---")
        st.markdown("### How It Works")
        st.markdown("""
        ```
        User Task
           |
           v
        [Researcher] → Gathers information
           |
           v  
        [Analyzer] → Organizes and analyzes
           |
           v
        [Writer] → Creates polished content
           |
           v
        [Reviewer] → Reviews and improves
           |
           v
        Final Output
        ```
        """)
    else:
        st.error("Cannot connect to server.")


st.markdown("---")
st.markdown("<div style=\"text-align:center;color:#888;\">AutoAgent v1.0 | Multi-Agent Orchestration | Built by Kethavath Santhosh</div>", unsafe_allow_html=True)
