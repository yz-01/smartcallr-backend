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

        if not openai_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
        if not groq_key:
            logger.warning("GROQ_API_KEY not found in environment variables")

        self.openai_client = OpenAI(api_key=openai_key)
        self.groq_client = Groq(api_key=groq_key)

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
        Generate summary of transcription using Groq
        """
        try:
            prompt = f"""
            Please provide a concise and professional summary of the following phone call transcription. 
            Focus on key points, decisions made, and important information discussed:

            Transcription:
            {transcription_text}

            Summary:
            """

            chat_completion = self.openai_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="gpt-4o-mini",
                temperature=0.7
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
