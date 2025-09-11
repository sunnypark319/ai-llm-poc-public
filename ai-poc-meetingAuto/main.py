# main.py
import streamlit as st
from config import APP_CONFIG
from session_manager import SessionManager
from transcription_service import TranscriptionService
from recording_controller import RecordingController
from ui_components import UIComponents

def main():
    """메인 애플리케이션"""
    
    # 페이지 설정
    st.set_page_config(
        page_title=APP_CONFIG['page_title'],
        page_icon=APP_CONFIG['page_icon']
    )
    
    # 세션 상태 초기화
    SessionManager.initialize()
    
    # 서비스 초기화
    transcription_service = TranscriptionService()
    recording_controller = RecordingController(transcription_service)
    
    # 메인 타이틀
    st.title(f"{APP_CONFIG['page_icon']} {APP_CONFIG['page_title']}")
    st.write("녹음 + 자동 음성 인식 + 녹취록/요약 생성까지 한번에!")
    
    # UI 컴포넌트들 표시
    UIComponents.show_status(transcription_service)
    
    st.markdown("---")
    
    # 버튼 제어
    start_clicked, stop_clicked, reset_clicked = UIComponents.show_control_buttons()
    
    # 버튼 이벤트 처리
    if start_clicked:
        if recording_controller.start_recording():
            st.rerun()
    
    if stop_clicked:
        if recording_controller.stop_recording():
            st.rerun()
    
    if reset_clicked:
        if recording_controller.reset_all():
            st.rerun()
    
    st.markdown("---")
    
    # 결과 표시
    UIComponents.show_results()
    
    # 오디오 파일 다운로드
    UIComponents.show_audio_download()
    
    st.markdown("---")
    
    # 사용 방법
    UIComponents.show_instructions()
    
    # 수동 새로고침 버튼 (녹음 중일 때만)
    UIComponents.show_refresh_button()
    
    # 성공 메시지
    UIComponents.show_success_message()

if __name__ == "__main__":
    main()