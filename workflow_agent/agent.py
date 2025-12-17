import logging

from google.adk.agents import ParallelAgent, SequentialAgent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.models.google_llm import Gemini
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional

from . import prompt

from .sub_agents.operational_anomaly_detection import operational_anomaly_detection_agent
from .sub_agents.cost_anomaly_detection import cost_anomaly_detection_agent
from .sub_agents.insights import insights_agent
from .sub_agents.presentation import presentation_agent

# Configure logging to show detailed traces from all agents.
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

def after_detector_runs(callback_context: CallbackContext) -> Optional[types.Content]:
    current_state = callback_context.state.to_dict()
    print(f"Agent state after agent runs: {current_state}")
    return None


def should_run_analysis(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Checks the output of the anomaly detection agents and decides whether to run the analysis agents.

    This function programmatically inspects the agent's state.

    Args:
        state: The current state dictionary of the agent, containing outputs from previous steps.

    Returns:
        The no anomaly detected or None to continue with the analysis agents.
    """
    current_state = callback_context.state.to_dict()
    # The output of the ParallelAgent is a dictionary of its sub-agents' outputs.
    detection_output = current_state.get("AnomalyDetectionRunner", {})
    op_result = detection_output.get("operational_anomaly_detection_agent", {})
    cost_result = detection_output.get("cost_anomaly_detection_agent", {})

    print(f"[Callback] {callback_context.state} Current State: {current_state}, op_result: {op_result}, cost_result: {cost_result}")

    # Check for an 'anomaly_detected' flag in the output of either detection agent.
    # NOTE: You must ensure your detection agents produce this structured output.
    if not(op_result.get("anomaly_detected") or cost_result.get("anomaly_detected")):
         return types.Content(
            parts=[types.Part(text=f"No anomaly detected.")],
            role="model" # Assign model role to the overriding response
        )
    return None #continue with normal execution

anomaly_detection_runner = ParallelAgent(
    name="anomaly_detection_runner",
    description="Runs operational and cost anomaly detection in parallel.",
    sub_agents=[
        operational_anomaly_detection_agent,
        cost_anomaly_detection_agent,
    ],
    after_agent_callback=after_detector_runs,
)

anomaly_report_runner = SequentialAgent(
    name="anomaly_report_runner",
    description="If an anomaly is detected by any of the anomaly detection agents, run the insights agent and the presentation agent.",
    sub_agents=[insights_agent, presentation_agent],
)

#router_agent = SequentialAgent(
#    name = "AnalysisRouterAgent",
#    description = "Check if the analysis agent should run or not",
#    sub_agents = [anomaly_analysis_runner],
#    before_agent_callback = should_run_analysis,
#)

watch_dog = LlmAgent(
    name="watch_dog",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description=(
        "Orchestrate multiple anomaly detection agents and produce insights into what is causing the anomalies"
    ),
    instruction=prompt.WATCH_DOG_PROMPT,
    output_key="anomaly_report",
    sub_agents=[anomaly_detection_runner, anomaly_report_runner],
)

root_agent = watch_dog
