"""
Graph Wiring
============
Builds the LangGraph StateGraph.
Currently wires the first four implemented agents.
that are implemented so far. Teammates adding Agents 4-7 should add
their nodes and edges here (after priority_assessment, before END).
"""

from agents.issue_classification import issue_classification_agent
from agents.priority_assessment import priority_assessment_agent
from agents.ticket_intake import ticket_intake_agent
from state import SharedState
from agents.troubleshooting import troubleshooting_agent


def build_graph():
    """Builds and compiles the LangGraph StateGraph."""
    from langgraph.graph import END, StateGraph

    graph = StateGraph(SharedState)

    graph.add_node("ticket_intake", ticket_intake_agent)
    graph.add_node("issue_classification", issue_classification_agent)
    graph.add_node("priority_assessment", priority_assessment_agent)
    graph.add_node("troubleshooting", troubleshooting_agent)

    graph.set_entry_point("ticket_intake")
    graph.add_edge("ticket_intake", "issue_classification")
    graph.add_edge("issue_classification", "priority_assessment")
    graph.add_edge("priority_assessment", "troubleshooting")

    # TODO (teammates): add_node/add_edge for troubleshooting, action,
    # verification (with conditional branching for resolved/not resolved),
    # and escalation, then point the last edge at END instead of this one.
    graph.add_edge("troubleshooting", END)

    return graph.compile()
