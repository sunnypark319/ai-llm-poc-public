# ui_components.py
import streamlit as st
import time
from datetime import datetime
from session_manager import SessionManager

class UIComponents:
    """UI 컴포넌트들을 관리하는 클래스"""
    
    @staticmethod
    def show_status(transcription_service):
        """현재 상태 표시"""
        st.header("📊 현재 상태")
        
        # API 상태 확인
        if transcription_service.is_available():
            st.success("✅ OpenAI API 연결됨")
        else:
            st.error("❌ OpenAI API 연결 실패 - .env 파일의 OPENAI_API_KEY를 확인하세요")
        
        # 녹음 상태에 따른 표시
        if SessionManager.is_recording():
            if SessionManager.is_stop_requested():
                st.warning("⏳ 녹음 종료 및 처리 중...")
            else:
                st.success("🔴 녹음 중...")
                
                # 시간 표시
                start_time = SessionManager.get('start_time')
                if start_time:
                    elapsed = time.time() - start_time
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("녹음 시간", f"{int(elapsed)}초")
                    with col2:
                        recorder = SessionManager.get('recorder')
                        if recorder:
                            frame_count = len(recorder.frames)
                            st.metric("녹음된 데이터", f"{frame_count} 프레임")
        else:
            st.info("⚪ 대기 중")
        
        # 결과 메시지 표시
        result_message = SessionManager.get('result_message')
        if result_message:
            if "성공" in result_message:
                st.success(result_message)
            else:
                st.error(result_message)
    
    @staticmethod
    def show_control_buttons():
        """녹음 제어 버튼들"""
        st.header("🎛️ 녹음 제어")
        
        col1, col2, col3 = st.columns(3)
        
        # 녹음 시작 버튼
        with col1:
            start_clicked = st.button(
                "🎤 녹음 시작", 
                disabled=SessionManager.is_recording(),
                use_container_width=True,
                type="primary"
            )
        
        # 녹음 종료 버튼
        with col2:
            stop_clicked = st.button(
                "⏹️ 녹음 종료", 
                disabled=not SessionManager.is_recording() or SessionManager.is_stop_requested(),
                use_container_width=True,
                type="secondary"
            )
        
        # 초기화 버튼
        with col3:
            reset_clicked = st.button("🗑️ 전체 초기화", use_container_width=True)
        
        return start_clicked, stop_clicked, reset_clicked
    
    @staticmethod
    def show_results():
        """처리 결과 표시"""
        if SessionManager.has_results():
            st.header("📋 처리 결과")
            
            # 탭으로 구분
            tab1, tab2 = st.tabs(["📝 녹취록", "📄 요약"])
            
            with tab1:
                transcript_content = SessionManager.get('transcript_content')
                if transcript_content:
                    st.text_area(
                        "녹취록 내용", 
                        transcript_content, 
                        height=400,
                        key="transcript_area"
                    )
                    
                    # 다운로드 버튼
                    st.download_button(
                        "📥 녹취록 다운로드 (.txt)",
                        transcript_content,
                        file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                else:
                    st.info("녹취록이 아직 생성되지 않았습니다.")
            
            with tab2:
                summary_content = SessionManager.get('summary_content')
                if summary_content:
                    st.text_area(
                        "요약 내용", 
                        summary_content, 
                        height=400,
                        key="summary_area"
                    )
                    
                    # 다운로드 버튼
                    st.download_button(
                        "📥 요약 다운로드 (.txt)",
                        summary_content,
                        file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                else:
                    st.info("요약이 아직 생성되지 않았습니다.")
    
    @staticmethod
    def show_audio_download():
        """WAV 파일 다운로드"""
        audio_file_data = SessionManager.get('audio_file_data')
        if audio_file_data:
            st.header("📥 녹음 파일 다운로드")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    "📥 WAV 파일 다운로드",
                    audio_file_data,
                    file_name=f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav",
                    mime="audio/wav",
                    use_container_width=True
                )
            
            with col2:
                file_size = len(audio_file_data)
                st.metric("파일 크기", f"{file_size/1024:.1f} KB")
    
    @staticmethod
    def show_instructions():
        """사용 방법"""
        st.header("📋 사용 방법")
        st.write("""
        1. **"🎤 녹음 시작"** 클릭
        2. **5-10초간 말하기** (회의 내용)
        3. **"⏹️ 녹음 종료"** 클릭
        4. **자동으로 음성 인식 및 녹취록/요약 생성**
        5. **결과 확인 및 다운로드**
        """)
    
    @staticmethod
    def show_refresh_button():
        """수동 새로고침 버튼 (녹음 중일 때만)"""
        if SessionManager.is_recording() and not SessionManager.is_stop_requested():
            st.header("🔄 수동 새로고침")
            if st.button("🔄 녹음 시간 업데이트", use_container_width=True):
                st.rerun()
            
            st.info("💡 녹음 중에는 이 버튼을 눌러서 시간을 확인할 수 있습니다. 종료 버튼은 언제든 즉시 작동합니다!")
    
    @staticmethod
    def show_success_message():
        """성공 메시지"""
        st.success("🎉 이 버전에서는 녹음 + 녹취록/요약이 자동으로 한번에 처리됩니다!")