# session_manager.py
import streamlit as st
from config import SESSION_KEYS

class SessionManager:
    """Streamlit 세션 상태 관리 클래스"""
    
    @staticmethod
    def initialize():
        """세션 상태 초기화"""
        defaults = {
            SESSION_KEYS['recording']: False,
            SESSION_KEYS['recorder']: None,
            SESSION_KEYS['start_time']: None,
            SESSION_KEYS['stop_requested']: False,
            SESSION_KEYS['result_message']: None,
            SESSION_KEYS['audio_file_data']: None,
            SESSION_KEYS['transcript_content']: None,
            SESSION_KEYS['summary_content']: None
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @staticmethod
    def get(key):
        """세션 상태 값 가져오기"""
        return st.session_state.get(SESSION_KEYS.get(key, key))
    
    @staticmethod
    def set(key, value):
        """세션 상태 값 설정"""
        st.session_state[SESSION_KEYS.get(key, key)] = value
    
    @staticmethod
    def clear_results():
        """결과 관련 세션 상태 초기화"""
        result_keys = ['result_message', 'audio_file_data', 'transcript_content', 'summary_content', 'stop_requested']
        for key in result_keys:
            SessionManager.set(key, None if key != 'stop_requested' else False)
    
    @staticmethod
    def clear_all():
        """모든 세션 상태 초기화"""
        for key in SESSION_KEYS.values():
            if key in st.session_state:
                del st.session_state[key]
        SessionManager.initialize()
    
    @staticmethod
    def is_recording():
        """현재 녹음 중인지 확인"""
        return SessionManager.get('recording')
    
    @staticmethod
    def is_stop_requested():
        """중지 요청 여부 확인"""
        return SessionManager.get('stop_requested')
    
    @staticmethod
    def has_results():
        """결과 데이터가 있는지 확인"""
        return (SessionManager.get('transcript_content') is not None or 
                SessionManager.get('summary_content') is not None)