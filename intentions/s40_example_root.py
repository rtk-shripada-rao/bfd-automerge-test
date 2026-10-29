#
# -*- coding: utf-8 -*-
# Example s40 root-level rule
# This matches the pattern: intentions/s40_.*\.py

from crule.api import crule, scope
from crule.api import priorities, EscalationLevel


@crule(EscalationLevel.TEST)
@scope("source-event-type:example")
def escalate_root_example(source):
    """Example root-level escalation rule."""
    return False
