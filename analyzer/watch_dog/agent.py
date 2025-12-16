from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.operational_anomaly_detection import (
    operational_anomaly_detection_agent,
)

MODEL = "gemini-2.5-pro"


watch_dog = LlmAgent(
    name="watch_dog",
    model=MODEL,
    description=(
        "Orchestrate multiple anomaly detection agents and produce insights into what is causing the anomalies"
    ),
    instruction=prompt.WATCH_DOG_PROMPT,
    output_key="seminal_paper",
    tools=[
        AgentTool(agent=operational_anomaly_detection_agent),
    ],
)

root_agent = watch_dog
