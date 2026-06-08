from google.adk.agents import LlmAgent, SequentialAgent


job_analysis_agent = LlmAgent(
    name="JobAnalysisAgent",
    model="gemini-2.5-flash",
    instruction="""
Sen İş Analiz Ajanısın.

Görevin:
Kullanıcının gönderdiği iş ilanını analiz et ve makine tarafından okunabilir bir JSON kontrol listesi üret.

Kurallar:
- Sadece geçerli JSON döndür.
- Markdown kullanma.
- Açıklama yazma.
- Eksik bilgi varsa "belirtilmemiş" yaz veya boş liste kullan.

JSON alanları:
- pozisyon
- zorunlu_beceriler
- tercih_edilen_beceriler
- deneyim_yili
- egitim
- is_turu
- sektor
- diger_gereksinimler
""",
    output_key="job_requirements_json"
)


cv_evaluation_agent = LlmAgent(
    name="CvEvaluationAgent",
    model="gemini-2.5-flash",
    instruction="""
Sen Özgeçmiş Değerlendirme Ajanısın.

Ajan 1 tarafından üretilen iş gereksinimleri JSON kontrol listesi:
{job_requirements_json}

Sistem tarafından CV dosyasından çıkarılan özgeçmiş metni:
{cv_text}

Görevin:
JSON kontrol listesindeki gereksinimleri CV metniyle karşılaştır.

Aşağıdaki formatta cevap ver:

Uygunluk Skoru: XX/100

Güçlü Yönler:
- ...

Eksik Yönler:
- ...

Genel Değerlendirme:
...
""",
    output_key="evaluation_result"
)


resume_screening_pipeline = SequentialAgent(
    name="ResumeScreeningPipeline",
    sub_agents=[
        job_analysis_agent,
        cv_evaluation_agent
    ]
)