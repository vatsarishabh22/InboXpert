

def schedule_meeting(attendees: list[str], topic: str, duration_minutes: int) -> dict:
    """
    Schedules a meeting in the user's calendar.
    
    Args:
        attendees: A list of email addresses of people to invite.
        topic: The subject of the meeting.
        duration_minutes: The length of the meeting in minutes.
    """
    print(f"ACTION: Scheduling a {duration_minutes}-minute meeting about '{topic}' with {', '.join(attendees)}.")
    # TODO: Google Calendar API Integration
    return {"status": "success", "meeting_id": "cal_123abc"}

def draft_reply(recipient: str, original_subject: str, body: str) -> dict:
    """
    Drafts a reply email in the user's Gmail.
    
    Args:
        recipient: The email address of the person to reply to.
        original_subject: The subject of the email being replied to.
        body: The content of the draft.
    """
    print(f"ACTION: Drafting reply to {recipient} with subject 'Re: {original_subject}'.")
    print(f"  -> Body: {body}")
    # TODO: Gmail API flow to create a draft reply
    return {"status": "success", "draft_id": "draft_456def"}

def add_to_todo_list(task_name: str, due_date: str = None) -> dict:
    """
    Adds a task to the user's to-do list application.
    
    Args:
        task_name: The name of the task.
        due_date: The date the task is due, in YYYY-MM-DD format (optional).
    """
    due_str = f" by {due_date}" if due_date else ""
    print(f"ACTION: Adding task '{task_name}' to to-do list{due_str}.")
    # TODO: Todoist/Asana/etc. API Integration
    return {"status": "success", "task_id": "todo_789ghi"}


AVAILABLE_TOOLS = {
    "schedule_meeting": schedule_meeting,
    "draft_reply": draft_reply,
    "add_to_todo_list": add_to_todo_list,
}