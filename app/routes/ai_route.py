from flask import Blueprint, request, Response, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

ai_bp = Blueprint('ai', __name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def stream_gemini_text_response(response):
    try:
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n[Error streaming response: {str(e)}]"


@ai_bp.route('/api/ai/ask', methods=['POST'])
def ask_sidi():
    try:
        data = request.get_json()
        question = data.get('question', '')

        # System prompt for the SIDI assistant
        system_prompt = (
            "You are SIDI, an advanced investment and economic analysis assistant. "
            "You assist users in understanding global markets, foreign direct investment (FDI) trends, economic indicators, and potential investment opportunities. "
            "Provide insightful, data-driven, and actionable responses to help users make informed decisions. "
            "Leverage your expertise in data visualization, market analysis, and investment strategies while ensuring clarity and precision in your responses."
        )

        # Combine system prompt and user question
        prompt = f"{system_prompt}\n\nUser's question: {question}"

        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            top_k=40,
            max_output_tokens=2048,
        )

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            stream=True
        )

        return Response(stream_gemini_text_response(response), mimetype='text/plain')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_bp.route('/api/ai/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@ai_bp.route('/api/ai/test-gemini', methods=['GET'])
def test_gemini():
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello!")
        return jsonify({"status": "success", "response": response.text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})