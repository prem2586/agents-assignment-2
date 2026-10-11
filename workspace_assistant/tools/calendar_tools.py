"""
Option A: Calendar Assistant Tools

Implement at least 3 tools for Google Calendar operations.
"""

from typing import Optional
from google.adk.tools import FunctionTool
from workspace_assistant.tools.auth import get_calendar_service

from datetime import datetime
from uuid import uuid4


# TODO: Implement your calendar tools
# Define each tool as a plain Python function with a clear docstring and type
# hints (ADK reads these to build the tool schema and auto-wraps the function),
# then add it to the list below. Each tool should return a dict with 'status'
# and relevant data. Wrapping with FunctionTool(func=my_function) is optional
# and only needed when you want explicit control over the tool.
# def list_upcoming_events(max_results: int = 10) -> dict:
#     """List upcoming calendar events.


#     Args:
#         max_results: Maximum number of events to return.

#     Returns:
#         dict with 'status' and 'events' keys.
#     """
#     try:
#         service = get_calendar_service()
#         events_result = service.events().list(
#             calendarId='primary', maxResults=max_results, timeMin="2026-10-10T00:00:00Z"
#         ).execute()
#         return {"status": "success", "events": events_result.get("items", [])}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}
    

# def add_event(summary:str,start_time: str,
#     end_time: str,
#     description: str = "",
#     location: str = "",
#     timezone: str = "America/Los_Angeles",
#     attendees: list[str] | None = None,
#     create_meet: bool = False) -> dict:
#     """Create a calendar event.

#     Args:
#         summary: Title of the event.
#         start_time: Start datetime in ISO format, e.g. 2026-10-15T10:00:00.
#         end_time: End datetime in ISO format, e.g. 2026-10-15T11:00:00.
#         description: Description of the event.
#         location: Physical address or meeting location.
#         timezone: IANA time zone, e.g. America/Los_Angeles.
#         attendees: List of attendee email addresses.
#         create_meet: Whether to generate a Google Meet link.

#     Returns:
#         Dictionary containing status and event details.
#     """
#     try:
#         start = datetime.fromisoformat(start_time)
#         end = datetime.fromisoformat(end_time)
#         service = get_calendar_service()
#         event = {
#             "summary": summary,
#             "description": description,
#             "location": location,
#             "start": {
#                 "dateTime": start_time,
#                 "timeZone": timezone,
#             },
#             "end": {
#                 "dateTime": end_time,
#                 "timeZone": timezone,
#             },
#         }

#         if attendees:
#             event["attendees"] = [
#                 {"email": email} for email in attendees
#             ]

#         if create_meet:
#             event["conferenceData"] = {
#                 "createRequest": {
#                     "requestId": str(uuid4()),
#                     "conferenceSolutionKey": {
#                         "type": "hangoutsMeet"
#                     },
#                 }
#             }
#         events_result = service.events().insert(
#             calendarId="primary",
#             body=event,
#             conferenceDataVersion=1 if create_meet else 0,
#             sendUpdates="all" if attendees else "none",
#         ).execute()

#         return {
#             "status": "success",
#             "event_id": events_result.get("id"),
#             "summary": events_result.get("summary"),
#             "event_link": events_result.get("htmlLink"),
#             "meet_link": events_result.get("hangoutLink"),
#         }
#     except Exception as e:
#         return {"status": "error", "message": str(e)}


# def delete_calendar_event(summary: str, confirmed: bool = False) -> dict:
#     """
#     Delete a Google Calendar event by its exact title.

#     Args:
#         summary: Exact event title to delete.
#         confirmed: True only after the user confirms deletion.

#     Returns:
#         Dictionary with deletion status and event details.
#     """
#     try:
#         service = get_calendar_service()
#         matching_events = []
#         page_token = None

#         while True:
#             result = service.events().list(
#                 calendarId="primary",
#                 q=summary,
#                 maxResults=250,
#                 singleEvents=True,
#                 pageToken=page_token,
#             ).execute()

#             for event in result.get("items", []):
#                 if event.get("summary", "").strip().casefold() == summary.strip().casefold():
#                     matching_events.append(event)

#             page_token = result.get("nextPageToken")
#             if not page_token:
#                 break

#         if not matching_events:
#             return {
#                 "status": "not_found",
#                 "message": f"No event found with title '{summary}'"
#             }

#         if len(matching_events) > 1:
#             return {
#                 "status": "multiple_matches",
#                 "message": "Multiple events have the same title. Select the event to delete.",
#                 "events": [
#                     {
#                         "event_id": event["id"],
#                         "summary": event.get("summary"),
#                         "start": event.get("start"),
#                         "end": event.get("end"),
#                     }
#                     for event in matching_events
#                 ],
#             }

#         event = matching_events[0]

#         if not confirmed:
#             return {
#                 "status": "confirmation_required",
#                 "message": "Ask the user to confirm deletion.",
#                 "event_id": event["id"],
#                 "summary": event.get("summary"),
#                 "start": event.get("start"),
#                 "end": event.get("end"),
#             }

#         service.events().delete(
#             calendarId="primary",
#             eventId=event["id"],
#             sendUpdates="all",
#         ).execute()

#         return {
#             "status": "success",
#             "message": f"Deleted event '{summary}'",
#             "event_id": event["id"],
#         }

#     except Exception as e:
#         return {
#             "status": "error",
#             "message": str(e),
#         }

# calendar_tools = [
#     list_upcoming_events,add_event,delete_calendar_event
# ]
