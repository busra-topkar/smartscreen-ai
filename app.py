import time
import tempfile
from pathlib import Path

import streamlit as st

from read_cv import read_cv
from adk_workflow import run_resume_screening


st.set_page_config(
    page_title="SmartScreen AI",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 SmartScreen AI")

st.markdown(
    "Google ADK tabanlı, iki ajanlı CV ön eleme sistemi"
)

st.divider()

job_text = st.text_area(
    "📋 İş İlanı",
    placeholder="İş ilanı metnini buraya yapıştırın...",
    height=220
)

uploaded_file = st.file_uploader(
    "📄 CV Yükle",
    type=["pdf", "docx"]
)

if st.button("🚀 Değerlendir", use_container_width=True, type="primary"):

    if not job_text.strip():
        st.error("İş ilanı giriniz.")
        st.stop()

    if uploaded_file is None:
        st.error("CV yükleyiniz.")
        st.stop()

    try:
        file_extension = Path(uploaded_file.name).suffix.lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_file_path = temp_file.name

        cv_text = read_cv(temp_file_path)

        if not cv_text.strip():
            st.error("CV dosyasından metin okunamadı.")
            st.stop()

        st.success("CV başarıyla yüklendi.")

        st.write("Yüklenen Dosya:")
        st.write(uploaded_file.name)

        with st.status("⚙️ Google ADK pipeline çalışıyor...", expanded=True) as status:
            st.write("Ajan 1: İş ilanı analiz ediliyor ve JSON kontrol listesi oluşturuluyor.")
            st.write("Ajan 2: CV, JSON kontrol listesine göre değerlendiriliyor.")

            result = None
            last_error = None

            for attempt in range(3):
                try:
                    result = run_resume_screening(
                        job_text=job_text,
                        cv_text=cv_text
                    )
                    break

                except Exception as e:
                    last_error = e

                    if "503" in str(e) or "UNAVAILABLE" in str(e):
                        st.warning(
                            f"Model yoğunluğu nedeniyle tekrar deneniyor... Deneme {attempt + 1}/3"
                        )
                        time.sleep(5)
                    else:
                        raise e

            if result is None:
                raise last_error

            status.update(
                label="✅ ADK pipeline tamamlandı.",
                state="complete"
            )

        st.subheader("📋 Ajan 1 Çıktısı — İş Gereksinimleri JSON")

        if isinstance(result["job_json"], dict):
            st.json(result["job_json"])
        else:
            st.code(result["job_json_text"])

        st.subheader("📊 Ajan 2 Çıktısı — CV Değerlendirme Sonucu")

        st.markdown(result["evaluation_result"])

    except Exception as e:
        st.error("Bir hata oluştu.")
        st.code(str(e))