#
# -*- coding: utf-8 -*-
# Example s40 escalation rule
# This matches the pattern: s40_.*\.py

from crule.api import crule, scope
from crule.api import priorities, EscalationLevel


MITRE_MAPPING = {"T1059.001": "Command and Scripting Interpreter: PowerShell"}


def add_list_to_field(source_dict, field, list_values):
    """Helper function to add values to a list field."""
    source_values = source_dict.get(field, [])
    if not isinstance(source_values, list):
        source_values = [source_values]
    source_values.extend(list_values)
    source_dict[field] = list(dict.fromkeys(source_values))


@crule(EscalationLevel.TEST)
@scope("source-event-type:sysmon")
def escalate_example(source):
    """Example escalation rule for testing."""
    return False
