# recording_controller.py
import time
import os
from audio_recorder import PerfectRecorder
from session_manager import SessionManager

class RecordingController:
    """녹음 제어 로직을 담당하는 클래스"""
    
    def __init__(self, transcription_service):
        self.transcription_service = transcription_service
    
    def start_recording(self):
        """녹음 시작 처리"""
        # 이전 결과 초기화
        SessionManager.clear_results()
        
        # 녹음 시작
        recorder = PerfectRecorder()
        success, message = recorder.start_recording()
        
        if success:
            SessionManager.set('recorder', recorder)
            SessionManager.set('recording', True)
            SessionManager.set('start_time', time.time())
            SessionManager.set('result_message', "✅ 녹음이 시작되었습니다!")
            return True
        else:
            SessionManager.set('result_message', f"❌ {message}")
            return False
    
    def stop_recording(self):
        """녹음 중지 및 처리"""
        # 종료 요청 플래그 설정
        SessionManager.set('stop_requested', True)
        
        recorder = SessionManager.get('recorder')
        if not recorder:
            return False
        
        # 녹음 시간 계산
        start_time = SessionManager.get('start_time')
        recording_duration = time.time() - start_time if start_time else 0
        
        # 녹음 종료 처리
        result = recorder.stop_recording()
        
        # 상태 초기화
        SessionManager.set('recording', False)
        SessionManager.set('recorder', None)
        SessionManager.set('start_time', None)
        SessionManager.set('stop_requested', False)
        
        if result and len(result) == 2:
            file_data, temp_audio_path = result
            file_size = len(file_data)
            SessionManager.set('result_message', 
                f"🎉 녹음 성공! 파일 크기: {file_size/1024:.1f} KB (녹음 시간: {recording_duration:.1f}초)")
            SessionManager.set('audio_file_data', file_data)
            
            # 자동으로 음성 처리 시작
            if self.transcription_service.is_available() and temp_audio_path:
                self._process_audio(temp_audio_path)
            
            # 임시 파일 정리
            try:
                os.unlink(temp_audio_path)
            except:
                pass
            
            return True
        else:
            SessionManager.set('result_message', "❌ 녹음 실패: 데이터가 없습니다")
            SessionManager.set('audio_file_data', None)
            return False
    
    def _process_audio(self, audio_path):
        """녹음된 오디오를 처리하여 녹취록과 요약 생성"""
        try:
            # 1. 음성 인식
            transcript_data, error = self.transcription_service.transcribe_audio(audio_path)
            if error:
                SessionManager.set('result_message', f"❌ {error}")
                return
            
            # 2. 화자 분리
            segments, error = self.transcription_service.process_segments(transcript_data)
            if error:
                SessionManager.set('result_message', f"❌ {error}")
                return
            
            # 3. 녹취록 생성
            transcript, error = self.transcription_service.create_transcript(segments)
            if error:
                SessionManager.set('result_message', f"❌ {error}")
                return
            
            SessionManager.set('transcript_content', transcript)
            
            # 4. 요약 생성
            summary, error = self.transcription_service.create_summary(transcript)
            if error:
                # 요약 실패는 경고로 처리 (녹취록은 성공했으므로)
                summary = "요약 생성에 실패했습니다."
            
            SessionManager.set('summary_content', summary)
            
        except Exception as e:
            SessionManager.set('result_message', f"❌ 처리 중 오류 발생: {str(e)}")
    
    def reset_all(self):
        """전체 상태 초기화"""
        # 녹음 중이면 먼저 중지
        if SessionManager.is_recording():
            recorder = SessionManager.get('recorder')
            if recorder:
                recorder.is_recording = False
        
        SessionManager.clear_all()
        return True