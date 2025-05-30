import os
import logging
from decouple import config
from openai import OpenAI
from groq import Groq

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        openai_key = config('OPENAI_API_KEY', default='')
        groq_key = config('GROQ_API_KEY', default='')
        openai_model = config('OPENAI_MODEL', default='gpt-4o-mini')

        if not openai_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
        if not groq_key:
            logger.warning("GROQ_API_KEY not found in environment variables")

        self.openai_client = OpenAI(api_key=openai_key)
        self.groq_client = Groq(api_key=groq_key)
        self.openai_model = openai_model

    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file using OpenAI Whisper
        """
        try:
            if not os.path.exists(audio_file_path):
                return {
                    'success': False,
                    'error': 'Audio file not found'
                }

            with open(audio_file_path, 'rb') as audio_file:
                transcription = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )

            logger.info(f"Audio transcription completed for {audio_file_path}")
            return {
                'success': True,
                'transcription': transcription
            }

        except Exception as e:
            logger.error(f"Failed to transcribe audio: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def summarize_transcription(self, transcription_text):
        """
        Generate summary of transcription using OpenAI
        """
        try:
            prompt = f"""
            You are an AI assistant specializing in business call analysis. Please analyze the following phone call transcription and provide a comprehensive summary.

            **Instructions:**
            - Create a well-structured summary that captures the essence of the conversation
            - Focus on actionable items, decisions, and key outcomes
            - Identify the main purpose/topic of the call
            - Note any follow-up actions or commitments made
            - Highlight important dates, numbers, or specific details mentioned
            - Keep the tone professional and concise
            - If this appears to be a sales/lead call, note the lead's interest level and next steps

            **Call Transcription:**
            {transcription_text}

            **Please provide your summary in the following format:**

            **Call Purpose:** [Brief description of why the call took place]

            **Key Discussion Points:**
            • [Main topic 1]
            • [Main topic 2]
            • [Main topic 3]

            **Decisions Made:**
            • [Decision 1]
            • [Decision 2]

            **Action Items:**
            • [Action item 1 - who is responsible]
            • [Action item 2 - who is responsible]

            **Next Steps:**
            [What happens next, follow-up timeline, etc.]

            **Additional Notes:**
            [Any other important information, contact details, dates, numbers mentioned]
            """

            chat_completion = self.openai_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional business call analyst. Your job is to create clear, actionable summaries of phone conversations that help users quickly understand what was discussed and what needs to be done next."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.openai_model,
                temperature=0.3,
                max_tokens=1000
            )

            summary = chat_completion.choices[0].message.content

            logger.info("Call summary generated successfully")
            return {
                'success': True,
                'summary': summary
            }

        except Exception as e:
            logger.error(f"Failed to generate summary: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
