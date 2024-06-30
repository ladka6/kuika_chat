from flask import Blueprint, request, jsonify, session
from pydantic import ValidationError
from kuika.main.controllers.schemas.chat_schemas import StartChatDTO, ChatDTO
from kuika.main.services.chat_service import ChatService
from kuika.main.services.schemas.chat_service_schemas import ChatInput
import uuid

chat_blueprint = Blueprint("chat", __name__)
chat_service = ChatService()


@chat_blueprint.route("/start", methods=["GET"])
def start():
    config_id = uuid.uuid4()
    session["config_id"] = str(config_id)
    return jsonify({"message": "Chat started", "config_id": session["config_id"]})


@chat_blueprint.route("/start_chat", methods=["POST"])
def start_chat():
    try:
        data = request.json
        dto = StartChatDTO(**data)
    except ValidationError as e:
        return jsonify({"error": str(e)}, 400)
    result = chat_service.start_chat(dto.job_description)
    return jsonify({"message": result})


@chat_blueprint.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        dto = ChatDTO(**data)
    except ValidationError as e:
        return jsonify({"error": str(e)}, 400)
    service_input = ChatInput(
        current_step=dto.current_step,
        job_description=dto.job_description,
        message=dto.message,
        requirements=dto.requirements,
    )
    result = chat_service.chat(service_input)
    return jsonify(result)


@chat_blueprint.route("/generate_report", methods=["POST"])
def generate_report():
    report = chat_service.generate_report()
    return report.report
