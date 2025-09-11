# transcription_service.py
import streamlit as st
from datetime import datetime, timedelta
from openai import OpenAI
from config import OPENAI_CONFIG

class TranscriptionService:
    def __init__(self):
        self.client = None
        if OPENAI_CONFIG['api_key']:
            self.client = OpenAI(api_key=OPENAI_CONFIG['api_key'])
    
    def is_available(self):
        """서비스 사용 가능 여부 확인"""
        return self.client is not None
    
    def transcribe_audio(self, audio_path):
        """OpenAI Whisper로 음성 인식"""
        try:
            st.write("🎤 음성 인식 중...")
            
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=OPENAI_CONFIG['whisper_model'],
                    file=audio_file,
                    response_format="verbose_json",
                    language="ko"
                )
            
            st.write("✅ 음성 인식 완료!")
            return transcript, None
        except Exception as e:
            return None, f"음성 인식 실패: {str(e)}"
    
    def format_timestamp(self, seconds):
        """타임스탬프 포맷팅"""
        try:
            time_obj = timedelta(seconds=seconds)
            hours = int(time_obj.total_seconds() // 3600)
            minutes = int((time_obj.total_seconds() % 3600) // 60)
            seconds = int(time_obj.total_seconds() % 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except:
            return "00:00:00"
    
    def process_segments(self, transcript_data):
        """화자 분리 (간단 버전)"""
        try:
            st.write("👥 화자 분리 중...")
            
            segments = transcript_data.segments
            processed_segments = []
            current_speaker = 1
            last_end_time = 0
            
            for i, segment in enumerate(segments):
                start_time = getattr(segment, 'start', 0)
                end_time = getattr(segment, 'end', 0)
                text = getattr(segment, 'text', '').strip()
                
                # 2초 이상 침묵시 화자 변경 가능성
                if start_time - last_end_time > 2.0 and len(text.split()) > 5:
                    current_speaker = (current_speaker % 3) + 1
                
                processed_segments.append({
                    'start_time': self.format_timestamp(start_time),
                    'end_time': self.format_timestamp(end_time),
                    'speaker': f"참석자 {current_speaker}",
                    'text': text
                })
                
                last_end_time = end_time
            
            st.write("✅ 화자 분리 완료!")
            return processed_segments, None
        except Exception as e:
            return None, f"화자 분리 실패: {str(e)}"
    
    def create_transcript(self, segments):
        """구조화된 녹취록 생성"""
        try:
            st.write("📝 녹취록 생성 중...")
            
            content = f"""📋 회의 녹취록
생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== 화자별 발언 내용 ===
"""
            
            for segment in segments:
                content += f"\n[{segment['start_time']}-{segment['end_time']}] {segment['speaker']}: {segment['text']}"
            
            st.write("✅ 녹취록 생성 완료!")
            return content, None
        except Exception as e:
            return None, f"녹취록 생성 실패: {str(e)}"
    
    def create_summary(self, transcript):
        """GPT로 회의 요약 생성"""
        try:
            st.write("📄 요약 생성 중...")
            
            # 텍스트 길이 제한 (2000자)
            text_to_summarize = transcript[:2000]
            
            prompt = f"""다음 회의 녹취록을 요약해주세요:

{text_to_summarize}

요약 형식:
1. 회의 개요
2. 주요 논의사항
3. 결론 및 다음 단계"""
            
            response = self.client.chat.completions.create(
                model=OPENAI_CONFIG['gpt_model'],
                messages=[{"role": "user", "content": prompt}],
                temperature=OPENAI_CONFIG['temperature'],
                max_tokens=OPENAI_CONFIG['max_tokens']
            )
            
            st.write("✅ 요약 생성 완료!")
            return response.choices[0].message.content, None
        except Exception as e:
            return None, f"요약 생성 실패: {str(e)}"