
"""
AI Meeting Summarizer
Convert meeting audio/text to summaries and update Confluence.
"""
import os
import tempfile
import torch
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import requests
import json
import markdown

class MeetingSummarizerService:
    def __init__(self):
        # Load whisper model for transcription
        self.transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base")
        
        # Load BART model for summarization
        self.summarizer_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
        self.summarizer_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

    def transcribe_audio(self, audio_file):
        """Transcribe audio file to text using Whisper"""
        try:
            # Create temporary file for uploaded audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_audio.write(audio_file.read())
                temp_audio_path = temp_audio.name
            
            # Transcribe audio with whisper
            result = self.transcriber(temp_audio_path)
            transcription = result.get("text", "")
            
            # Clean up temporary file
            os.unlink(temp_audio_path)
            
            return {"status": "success", "transcription": transcription}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def summarize_text(self, text, max_length=150, min_length=50):
        """Summarize text using BART model"""
        try:
            # Tokenize and generate summary
            inputs = self.summarizer_tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
            
            summary_ids = self.summarizer_model.generate(
                inputs.input_ids, 
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                num_beams=4
            )
            
            summary = self.summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            
            # Extract key points (simplified approach)
            sentences = summary.split(". ")
            key_points = [f"- {sentence.strip()}." for sentence in sentences if len(sentence) > 10]
            
            return {
                "status": "success", 
                "summary": summary,
                "key_points": key_points
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def generate_markdown_report(self, meeting_data):
        """Generate markdown report from meeting data"""
        markdown_content = f"""# Meeting Summary: {meeting_data.get('title', 'Untitled Meeting')}

## Meeting Details
- **Date**: {meeting_data.get('date', 'N/A')}
- **Duration**: {meeting_data.get('duration', 'N/A')}
- **Participants**: {', '.join(meeting_data.get('participants', ['N/A']))}

## Summary
{meeting_data.get('summary', 'No summary available')}

## Key Points
"""
        
        for point in meeting_data.get('key_points', []):
            markdown_content += f"{point}\n"
        
        if 'action_items' in meeting_data and meeting_data['action_items']:
            markdown_content += "\n## Action Items\n"
            for item in meeting_data['action_items']:
                markdown_content += f"- {item}\n"
        
        if 'decisions' in meeting_data and meeting_data['decisions']:
            markdown_content += "\n## Decisions\n"
            for decision in meeting_data['decisions']:
                markdown_content += f"- {decision}\n"
        
        return {"status": "success", "markdown": markdown_content}

    def upload_to_confluence(self, page_id, markdown_content, base_url, auth_token):
        """Upload markdown summary to Confluence"""
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        # First, get the current version of the page
        version_url = f"{base_url}/rest/api/content/{page_id}"
        
        try:
            response = requests.get(version_url, headers=headers)
            response.raise_for_status()
            
            page_data = response.json()
            current_version = page_data.get("version", {}).get("number", 1)
            
            # Convert markdown to HTML
            html_content = markdown.markdown(markdown_content)
            
            # Update the page
            update_data = {
                "version": {
                    "number": current_version + 1
                },
                "title": page_data.get("title", "Meeting Summary"),
                "type": "page",
                "body": {
                    "storage": {
                        "value": html_content,
                        "representation": "storage"
                    }
                }
            }
            
            update_url = f"{base_url}/rest/api/content/{page_id}"
            update_response = requests.put(
                update_url, 
                headers=headers, 
                data=json.dumps(update_data)
            )
            update_response.raise_for_status()
            
            return {"status": "success", "message": "Summary uploaded to Confluence"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
