import streamlit as st
import pandas as pd
import plotly.express as px
from utils.pdf_extractor import extract_text_from_pdf
from utils.embeddings import get_embedding
from utils.similarity import calculate_similarity
from utils.skills import extract_skills, get_missing_skills, calculate_ats_score

st.title("Resume Ranker")

job_description = st.text_area("Enter Job Description")

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)",
    type="pdf",
    accept_multiple_files=True
)

if st.button("Analyze Resumes"):

    if not job_description:
        st.warning("Please enter a job description first.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        job_embedding = get_embedding(job_description)
        jd_skills = extract_skills(job_description)

        results = []

        for uploaded_file in uploaded_files:
            resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text:
                st.error(f"Could not extract text from {uploaded_file.name}")
                continue

            resume_embedding = get_embedding(resume_text)
            score = calculate_similarity(job_embedding, resume_embedding)

            resume_skills = extract_skills(resume_text)
            ats_score = calculate_ats_score(jd_skills, resume_skills)
            missing_skills = get_missing_skills(jd_skills, resume_skills)

            results.append((uploaded_file.name, score, ats_score, missing_skills))

        ranked_results = sorted(results, key=lambda item: item[1], reverse=True)

        st.markdown("---")

        if not ranked_results:
            st.info("No resumes could be successfully analyzed.")
        else:
            # Build a DataFrame for charting
            chart_data = pd.DataFrame({
                "Resume": [r[0] for r in ranked_results],
                "Similarity Score": [r[1] for r in ranked_results],
                "ATS Match (%)": [r[2] for r in ranked_results],
            })

            st.subheader("Score Comparison")
            fig = px.bar(
                chart_data,
                x="Resume",
                y="Similarity Score",
                color="ATS Match (%)",
                color_continuous_scale="Blues",
                text="Similarity Score",
            )
            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            fig.update_layout(yaxis_range=[0, 1])
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Ranked Candidates")
            for rank, (filename, score, ats_score, missing_skills) in enumerate(ranked_results, start=1):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**#{rank} — {filename}**")
                    st.progress(min(max(score, 0.0), 1.0))
                    st.caption(f"ATS Keyword Match: {ats_score:.0f}%")

                    if missing_skills:
                        st.caption("Missing skills: " + ", ".join(sorted(missing_skills)))
                    else:
                        st.caption("All identified JD skills present.")

                with col2:
                    st.metric(label="Similarity", value=f"{score:.2f}")
