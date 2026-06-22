## 🎯 Resume Ranker

A smart resume ranking tool that matches resumes against a job description — powered by NLP and transformer embeddings.

🔗 https://resume-ranker-mahekgelra.streamlit.app/

---

## 📌 Features

-  Extracts text from uploaded resume PDFs
-  Converts resumes and job description into embeddings using `all-MiniLM-L6-v2`
-  Calculates semantic similarity using Cosine Similarity
-  Ranks resumes from best to worst match
-  ATS keyword matching with missing skills detection
-  Visual score comparison chart using Plotly

---

## 🛠️ Built With

- Streamlit
- PyPDF2
- Sentence-Transformers
- Scikit-learn
- Pandas
- Plotly

---

## How To Use

1. Paste the job description in the text area
2. Upload one or more resume PDFs using the file uploader
3. Click **Analyze Resumes**
4. View ranked candidates with similarity scores, ATS match % and missing skills

---

## Run Locally

```bash
git clone https://github.com/MahekGelra/resume-ranker
cd resume-ranker
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
streamlit run app.py
```

