import time

# Stores last few conversation events
context_memory = []

MAX_MEMORY = 20


def store_event(transcript):
    """
    Stores a speech event in memory
    """

    context_memory.append({
        "timestamp": time.time(),
        "transcript": transcript,
        "type": "speech"
    })

    if len(context_memory) > MAX_MEMORY:
        context_memory.pop(0)


def get_context():
    """
    Returns conversation memory
    """

    return context_memory


def should_interrupt_with_context():
    """
    Checks recent context for risky user actions
    """

    if not context_memory:
        return False, None

    latest = context_memory[-1]["transcript"].lower()

    risk_keywords = [
        "skip",
        "ignore",
        "doesn't matter",
        "no need",
        "i guess",
        "maybe later"
    ]

    for word in risk_keywords:
        if word in latest:
            return True, "you may be skipping something important"

    return False, None