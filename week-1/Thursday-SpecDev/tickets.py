from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Ticket:
    id: str
    customer: str
    subject: str
    priority: str  # "Normal" or "Urgent"
    status: str  # "open" or "closed"
    created_at: datetime
    last_customer_reply_at: datetime
    reply_deadline: datetime
    closed_by: Optional[str] = None


def _days_ago(n: int) -> datetime:
    return datetime.now() - timedelta(days=n)


def close_stale_tickets(
    tickets: List[Ticket],
    *,
    closed_by: str = "system (auto-close)",
    now: Optional[datetime] = None,
) -> List[Ticket]:
    """Auto-close open tickets whose reply deadline has passed.

    A ticket gets closed automatically when all of these hold:
      - it is still "open" (already-closed tickets are left untouched)
      - its `reply_deadline` has passed, relative to `now`
      - it is not "Urgent" priority

    Urgent tickets are deliberately exempt. A customer going quiet on
    something like a live production outage doesn't mean the problem is
    resolved, so those are left open for a human to review and close
    explicitly, no matter how overdue the reply is.

    Tickets are mutated in place (`status` set to "closed", `closed_by`
    stamped with `closed_by`); the function also returns the list of
    tickets it closed, so callers can report/log what happened.

    Args:
        tickets: Tickets to check.
        closed_by: Value recorded in `closed_by` for tickets this closes.
        now: Reference time for the deadline check. Defaults to
            `datetime.now()`; pass an explicit value in tests so results
            don't depend on when the test happens to run.

    Returns:
        The subset of `tickets` that were closed by this call.
    """
    now = now if now is not None else datetime.now()
    closed: List[Ticket] = []
    for ticket in tickets:
        if ticket.status != "open":
            continue
        if ticket.priority == "Urgent":
            continue
        if ticket.reply_deadline >= now:
            continue
        ticket.status = "closed"
        ticket.closed_by = closed_by
        closed.append(ticket)
    return closed


def load_sample_tickets() -> List[Ticket]:
    """Return a fresh list of sample tickets, dated relative to today."""
    return [
        Ticket(
            id="HD-1001",
            customer="Priya Shah",
            subject="Invoice PDF won't download",
            priority="Normal",
            status="open",
            created_at=_days_ago(20),
            last_customer_reply_at=_days_ago(14),
            reply_deadline=_days_ago(-2),
        ),
        Ticket(
            id="HD-1002",
            customer="Callum Reid",
            subject="Can't reset account password",
            priority="Normal",
            status="open",
            created_at=_days_ago(15),
            last_customer_reply_at=_days_ago(13),
            reply_deadline=_days_ago(-4),
        ),
        Ticket(
            id="HD-1003",
            customer="Aiswarya Menon",
            subject="Production integration returning 500s",
            priority="Urgent",
            status="open",
            created_at=_days_ago(45),
            last_customer_reply_at=_days_ago(40),
            reply_deadline=_days_ago(30),
        ),
        Ticket(
            id="HD-1004",
            customer="Ben Okafor",
            subject="Question about billing cycle",
            priority="Normal",
            status="closed",
            created_at=_days_ago(60),
            last_customer_reply_at=_days_ago(35),
            reply_deadline=_days_ago(20),
            closed_by="Jamie Ochieng",
        ),
        Ticket(
            id="HD-1005",
            customer="Freya Lindqvist",
            subject="Export button does nothing",
            priority="Normal",
            status="open",
            created_at=_days_ago(33),
            last_customer_reply_at=_days_ago(30),
            reply_deadline=_days_ago(18),
        ),
        Ticket(
            id="HD-1006",
            customer="Marcus Tan",
            subject="Feature request: dark mode",
            priority="Normal",
            status="open",
            created_at=_days_ago(10),
            last_customer_reply_at=_days_ago(2),
            reply_deadline=_days_ago(-5),
        ),
        Ticket(
            id="HD-1007",
            customer="Nadia Hassan",
            subject="Login page intermittently blank",
            priority="Urgent",
            status="open",
            created_at=_days_ago(6),
            last_customer_reply_at=_days_ago(5),
            reply_deadline=_days_ago(-1),
        ),
    ]
