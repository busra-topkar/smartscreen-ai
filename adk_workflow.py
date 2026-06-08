import asyncio
import json
import threading
import uuid

from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from adk_agents import resume_screening_pipeline


APP_NAME = "smartscreen_ai"


def _extract_text_from_event(event):
    if not getattr(event, "content", None):
        return None

    if not getattr(event.content, "parts", None):
        return None

    text_parts = []

    for part in event.content.parts:
        text = getattr(part, "text", None)
        if text:
            text_parts.append(text)

    if not text_parts:
        return None

    return "\n".join(text_parts)


def _clean_json_text(text):
    if not text:
        return ""

    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

    return cleaned


async def run_resume_screening_async(job_text, cv_text):
    user_id = "streamlit_user"
    session_id = f"session_{uuid.uuid4().hex}"

    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
        state={
            "cv_text": cv_text
        }
    )

    runner = Runner(
        agent=resume_screening_pipeline,
        app_name=APP_NAME,
        session_service=session_service
    )

    user_message = Content(
        role="user",
        parts=[
            Part(text=job_text)
        ]
    )

    job_json_text = ""
    evaluation_result = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message
    ):
        if not event.is_final_response():
            continue

        event_text = _extract_text_from_event(event)

        if not event_text:
            continue

        author = getattr(event, "author", "")

        if author == "JobAnalysisAgent":
            job_json_text = event_text

        elif author == "CvEvaluationAgent":
            evaluation_result = event_text

        else:
            evaluation_result = event_text

    if not evaluation_result:
        raise RuntimeError("ADK pipeline değerlendirme sonucu üretemedi.")

    cleaned_job_json = _clean_json_text(job_json_text)

    try:
        parsed_job_json = json.loads(cleaned_job_json) if cleaned_job_json else None
    except json.JSONDecodeError:
        parsed_job_json = cleaned_job_json

    return {
        "job_json": parsed_job_json,
        "job_json_text": cleaned_job_json,
        "evaluation_result": evaluation_result
    }


def run_resume_screening(job_text, cv_text):
    """
    Streamlit içinden güvenli şekilde async ADK pipeline çalıştırır.
    Her çağrıda yeni session açıldığı için sistem stateless çalışır.
    """

    try:
        asyncio.get_running_loop()

    except RuntimeError:
        return asyncio.run(
            run_resume_screening_async(job_text, cv_text)
        )

    result_holder = {}
    error_holder = {}

    def _run():
        try:
            result_holder["result"] = asyncio.run(
                run_resume_screening_async(job_text, cv_text)
            )
        except Exception as e:
            error_holder["error"] = e

    thread = threading.Thread(target=_run)
    thread.start()
    thread.join()

    if "error" in error_holder:
        raise error_holder["error"]

    return result_holder["result"]