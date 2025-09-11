# audio_recorder.py
import pyaudio
import threading
import wave
import tempfile
import os
from config import AUDIO_CONFIG

class PerfectRecorder:
    def __init__(self):
        self.frames = []
        self.audio = None
        self.stream = None
        self.is_recording = False
        
    def start_recording(self):
        """녹음 시작"""
        try:
            self.audio = pyaudio.PyAudio()
            self.frames = []
            self.is_recording = True
            
            # pyaudio 상수 매핑
            format_map = {
                'paInt16': pyaudio.paInt16,
                'paInt32': pyaudio.paInt32,
                'paFloat32': pyaudio.paFloat32
            }
            
            self.stream = self.audio.open(
                format=format_map.get(AUDIO_CONFIG['format'], pyaudio.paInt16),
                channels=AUDIO_CONFIG['channels'],
                rate=AUDIO_CONFIG['rate'],
                input=True,
                frames_per_buffer=AUDIO_CONFIG['chunk']
            )
            
            self.thread = threading.Thread(target=self._record)
            self.thread.daemon = True
            self.thread.start()
            
            return True, "녹음 시작 성공"
        except Exception as e:
            return False, f"녹음 시작 실패: {str(e)}"
    
    def _record(self):
        """녹음 스레드"""
        while self.is_recording:
            try:
                data = self.stream.read(AUDIO_CONFIG['chunk'])
                self.frames.append(data)
            except:
                break
    
    def stop_recording(self):
        """녹음 중지 및 파일 생성"""
        try:
            # 녹음 중지
            self.is_recording = False
            
            # 스레드 종료 대기
            if hasattr(self, 'thread'):
                self.thread.join(timeout=3)
            
            # 스트림 정리
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            
            # PyAudio 정리
            if self.audio:
                self.audio.terminate()
            
            # 데이터 확인
            frame_count = len(self.frames)
            if frame_count == 0:
                return None, "녹음된 데이터가 없습니다"
            
            # WAV 파일 생성
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_filename = temp_file.name
            temp_file.close()
            
            # WAV 파일 쓰기
            wf = wave.open(temp_filename, 'wb')
            wf.setnchannels(AUDIO_CONFIG['channels'])
            wf.setsampwidth(2)  # 16비트
            wf.setframerate(AUDIO_CONFIG['rate'])
            wf.writeframes(b''.join(self.frames))
            wf.close()
            
            # 파일 크기 확인
            file_size = os.path.getsize(temp_filename)
            
            if file_size > 44:  # WAV 헤더보다 큰지 확인
                # 파일을 메모리로 읽기
                with open(temp_filename, 'rb') as f:
                    file_data = f.read()
                
                return file_data, temp_filename
            else:
                os.unlink(temp_filename)
                return None, f"파일이 너무 작습니다 ({file_size} bytes)"
                
        except Exception as e:
            return None, f"녹음 종료 실패: {str(e)}"