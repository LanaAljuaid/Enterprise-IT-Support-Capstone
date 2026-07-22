"""
Entry Point
===========
Standalone runner for the three implemented agents — no LangGraph
dependency required. Useful for local testing before this is wired into
the full 7-agent LangGraph workflow (see graph.py for that wiring).
"""

import json
from typing import Optional

from agents.issue_classification import issue_classification_agent
from agents.priority_assessment import priority_assessment_agent
from agents.ticket_intake import ticket_intake_agent
from state import SharedState


def run_pipeline(raw_ticket_text: str, department: Optional[str] = None) -> SharedState:
    """Runs the three agents in sequence, manually threading the shared
    state through each one.

    `department` simulates the internal user-database lookup that would
    normally happen at authentication time, before the Ticket Intake Agent
    ever runs — it is NOT extracted from the ticket text.
    """
    state: SharedState = {"raw_ticket_text": raw_ticket_text, "department": department}

    state.update(ticket_intake_agent(state))
    state.update(issue_classification_agent(state))
    state.update(priority_assessment_agent(state))

    return state


if __name__ == "__main__":
    sample_ticket = (
        "Hi, I can't send or receive emails on Outlook since this morning. "
        "I keep getting an error that says 'Cannot connect to server'. "
        "I'm on my work laptop, Windows 11, based in the Chicago office."
    )

    # In a real system this would come from the authenticated employee's
    # profile in the internal user database — not from the ticket text.
    employee_department = "Finance"

    final_state = run_pipeline(sample_ticket, department=employee_department)
    print(json.dumps(final_state, indent=2))
