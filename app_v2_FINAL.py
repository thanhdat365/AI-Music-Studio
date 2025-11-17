import streamlit as st
from gtts import gTTS
import os
from pydub import AudioSegment
import io
import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCNh53nKFFYZN9AN3cZL7wFE69P7Gl2m_w"
genai.configure(api_key=GEMINI_API_KEY)

# Set page config
st.set_page_config(
    page_title="AI Music Studio",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    body { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #eaeaea; }
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
    .stSidebar { background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 100%); }
    .stButton > button {
        background: linear-gradient(90deg, #e94560 0%, #f39c12 100%);
        color: white; border: none; border-radius: 8px; padding: 10px 24px;
        font-size: 16px; font-weight: bold; transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 16px rgba(233, 69, 96, 0.3); }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<h1 style='text-align: center; background: linear-gradient(90deg, #e94560, #f39c12); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3em; margin-bottom: 10px;'>
🎵 AI MUSIC STUDIO - TAO NHAC GIONG SUNO
</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# Tab selection
tab1, tab2 = st.tabs(["🤖 TU DONG - AUTO LYRICS", "✏️ NHAP LUI - MANUAL LYRICS"])

with tab1:
    st.markdown("### 📋 CHE DO TU DONG: CHI CAN NHAP TIEU DE")
    st.info("💡 App se tu dong viet loi bai hat tu tieu de, sau do tao am thanh")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        song_title = st.text_input(
            "📝 TIEU DE BAI HAT:",
            placeholder="Vd: Nha Quang Ba Toan Nang",
            max_chars=100,
            key="title"
        )
        
        with st.sidebar:
            st.markdown("### ⚙️ CAU HINH")
            language = st.selectbox("🌐 Chon Ngon Ngu", ["Vietnamese", "English", "Francais", "Espanol", "Italiano"], key="lang")
            speed = st.slider("⏱️ Toc Do (0.5x - 2.0x)", 0.5, 2.0, 1.0, 0.1, key="speed")
            style = st.selectbox("🎨 Phong Cach Giong Noi", ["Binh Thuong", "Nam Tinh", "Nu Tinh", "Thon Gian", "Trang Trong"], key="style")
            emotion = st.selectbox("😊 Cam Xuc", ["Binh Thuong", "Vui Khoai", "Trang Trong", "Tham Thuc"], key="emotion")
            st.markdown("---")
            st.info("✨ Gemini AI se viet loi bai hat tu tieu de")
    
    with col2:
        st.markdown("### 📊 THONG TIN")
        st.info(f"Ngon ngu: {language}")
        st.info(f"Toc do: {speed}x")
        st.info(f"Phong cach: {style}")
        st.info(f"Cam xuc: {emotion}")
    
    if st.button("🤖 GENERATE LYRICS & MUSIC", use_container_width=True, key="auto_btn"):
        if song_title.strip():
            with st.spinner("🤖 Gemini AI dang viet loi bai hat..."):
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    prompt = f"""Hay viet mot bai hat Tieng Viet ve: '{song_title}'
                    
Yeu cau:
- Co 2-3 doan (verse + chorus)
- Moi doan 2-3 dong
- Nghe tu nhien, de thuong
- Lien quan den chu de
- Chi ghi loi, khong them chi tieu

Van ban:"""
                    
                    response = model.generate_content(prompt)
                    generated_lyrics = response.text
                    
                    st.success("✅ Gemini da viet xong loi bai hat!")
                    st.markdown("### 📝 LOI BAI HAT (Generated):")
                    st.text_area("Loi bai hat:", generated_lyrics, height=200, disabled=True)
                    
                    with st.spinner("🎵 Dang tao am thanh..."):
                        try:
                            tts = gTTS(text=generated_lyrics, lang="vi", slow=False)
                            audio_buffer = io.BytesIO()
                            tts.write_to_fp(audio_buffer)
                            audio_buffer.seek(0)
                            
                            try:
                                audio = AudioSegment.from_file(audio_buffer, format="mp3")
                                wav_buffer = io.BytesIO()
                                audio.export(wav_buffer, format="wav")
                                wav_buffer.seek(0)
                            except:
                                wav_buffer = audio_buffer
                            
                            st.success("✅ Tao am thanh thanh cong!")
                            st.markdown("### 🎧 NGHE BAI HAT")
                            audio_buffer.seek(0)
                            st.audio(audio_buffer, format="audio/mp3")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                audio_buffer.seek(0)
                                st.download_button(label="📥 Tai MP3", data=audio_buffer, file_name=f"{song_title}.mp3", mime="audio/mpeg", use_container_width=True)
                            
                            with col2:
                                wav_buffer.seek(0)
                                st.download_button(label="📥 Tai WAV", data=wav_buffer, file_name=f"{song_title}.wav", mime="audio/wav", use_container_width=True)
                        except Exception as e:
                            st.error(f"❌ Loi tao am thanh: {str(e)}")
                
                except Exception as e:
                    st.error(f"❌ Loi Gemini AI: {str(e)}")
        else:
            st.warning("⚠️ Vui long nhap tieu de bai hat")

with tab2:
    st.markdown("### ✏️ CHE DO THU CONG: NHAP LOI BAI HAT TRUC TIEP")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 NHAP BAI HAT")
        lyrics = st.text_area("Nhap van ban ban muon chuyen thanh am thanh:", height=200, max_chars=500, placeholder="Nhap loi bai hat o day...", key="lyrics")
        char_count = len(lyrics)
        st.caption(f"📊 Ky tu: {char_count}/500")
    
    with col2:
        st.markdown("### ⚙️ CAU HINH")
        language2 = st.selectbox("🌐 Chon Ngon Ngu", ["Vietnamese", "English", "Francais", "Espanol", "Italiano"], key="lang2")
        speed2 = st.slider("⏱️ Toc Do", 0.5, 2.0, 1.0, 0.1, key="speed2")
        style2 = st.selectbox("🎨 Phong Cach", ["Binh Thuong", "Nam Tinh", "Nu Tinh", "Thon Gian", "Trang Trong"], key="style2")
    
    if st.button("🎵 TAO NHAC", use_container_width=True, key="manual_btn"):
        if lyrics.strip():
            with st.spinner("⏳ Dang tao am thanh..."):
                try:
                    tts = gTTS(text=lyrics, lang="vi", slow=False)
                    audio_buffer = io.BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    
                    try:
                        audio = AudioSegment.from_file(audio_buffer, format="mp3")
                        wav_buffer = io.BytesIO()
                        audio.export(wav_buffer, format="wav")
                        wav_buffer.seek(0)
                    except:
                        wav_buffer = audio_buffer
                    
                    st.success("✅ Tao thanh cong!")
                    st.markdown("### 🎧 NGHE BAI HAT")
                    audio_buffer.seek(0)
                    st.audio(audio_buffer, format="audio/mp3")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        audio_buffer.seek(0)
                        st.download_button(label="📥 Tai MP3", data=audio_buffer, file_name="music.mp3", mime="audio/mpeg", use_container_width=True)
                    
                    with col2:
                        wav_buffer.seek(0)
                        st.download_button(label="📥 Tai WAV", data=wav_buffer, file_name="music.wav", mime="audio/wav", use_container_width=True)
                    
                except Exception as e:
                    st.error(f"❌ Loi: {str(e)}")
        else:
            st.warning("⚠️ Vui long nhap van ban")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px; margin-top: 20px;'>
    <p>🎵 AI Music Studio - Powered by Gemini AI & Google TTS & Streamlit</p>
    <p>© 2025 Nha Quang Ba Toan Nang - bigsell.com.vn</p>
</div>
""", unsafe_allow_html=True)
