# SmartScreen AI

SmartScreen AI, Google ADK tabanlı çok ajanlı bir CV ön eleme sistemidir.

Bu sistem, küçük işletmelerin ve girişimlerin aday özgeçmişlerini iş ilanına göre daha hızlı ve tutarlı şekilde değerlendirmesine yardımcı olur. Kullanıcıdan iş ilanı metni ve CV dosyası alınır. Sistem önce iş ilanını analiz ederek yapılandırılmış bir JSON kontrol listesi üretir, ardından yüklenen CV’yi bu kontrol listesine göre değerlendirerek uygunluk skoru ve açıklama oluşturur.

## Özellikler

* İş ilanı metni girişi
* PDF ve DOCX formatında CV yükleme
* CV dosyasından metin çıkarma
* Google ADK tabanlı çok ajanlı yapı
* Ardışık çalışan iki ajanlı mimari
* JSON formatında iş gereksinimi kontrol listesi üretme
* CV’yi iş gereksinimlerine göre değerlendirme
* Uygunluk skoru üretme
* Güçlü ve eksik yön analizi
* Streamlit tabanlı web arayüzü
* Streamlit Community Cloud üzerinde canlı deploy

## Sistem Mimarisi

Sistem ardışık çalışan iki ajanlı bir mimariye sahiptir.

### 1. JobAnalysisAgent

JobAnalysisAgent, kullanıcı tarafından girilen iş ilanını analiz eder. İş ilanındaki pozisyon, zorunlu beceriler, tercih edilen beceriler, deneyim yılı, eğitim bilgisi, iş türü, sektör ve diğer gereksinimleri çıkararak yapılandırılmış bir JSON kontrol listesi üretir.

### 2. CvEvaluationAgent

CvEvaluationAgent, CV’den çıkarılan metni JobAnalysisAgent tarafından üretilen JSON kontrol listesi ile karşılaştırır. Bu karşılaştırma sonucunda aday için uygunluk skoru, güçlü yönler, eksik yönler ve genel değerlendirme üretir.

## Kullanılan Google ADK Bileşenleri

Çok ajanlı iş akışı Google ADK bileşenleri kullanılarak geliştirilmiştir:

* `LlmAgent`
* `SequentialAgent`
* `Runner`
* `InMemorySessionService`

Sistem her değerlendirme için yeni bir oturum oluşturur. Bu nedenle değerlendirmeler birbirinden bağımsız şekilde çalışır.

## Kullanılan Teknolojiler

* Python
* Streamlit
* Google ADK
* Gemini API
* PyPDF
* python-docx
* Streamlit Community Cloud

## Çalışma Akışı

1. Kullanıcı iş ilanı metnini girer.
2. Kullanıcı PDF veya DOCX formatında CV yükler.
3. Sistem CV dosyasından düz metin çıkarır.
4. JobAnalysisAgent iş ilanını analiz eder ve JSON kontrol listesi oluşturır.
5. CvEvaluationAgent CV’yi bu JSON kontrol listesine göre değerlendirir.
6. Sistem uygunluk skorunu, güçlü yönleri, eksik yönleri ve genel değerlendirmeyi Streamlit arayüzünde gösterir.

## Deploy

Uygulama Streamlit Community Cloud üzerinde deploy edilmiştir.

Gizli bilgiler Streamlit Secrets üzerinden yönetilir:

```toml
GOOGLE_API_KEY = "your_api_key"
```

## Projenin Amacı

Bu projenin amacı, işe alım sürecindeki ilk CV ön eleme aşamasını ajan tabanlı yapay zeka sistemiyle otomatikleştirmektir. Sistem, manuel CV inceleme süresini azaltmayı, değerlendirme sürecini daha tutarlı hale getirmeyi ve aday uygunluğunu daha hızlı analiz etmeyi hedefler.

Bu proje Uzman Sistemler dersi kapsamında geliştirilmiştir.
