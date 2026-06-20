# A curated reference list of common technical and soft skills relevant
# to data/tech roles. This acts as our "vocabulary" for keyword matching.
SKILL_KEYWORDS = [
    "python", "java", "c++", "sql", "r", "javascript", "html", "css",
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "data analysis", "data visualization", "pandas",
    "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
    "power bi", "tableau", "excel", "statistics", "data structures",
    "algorithms", "git", "github", "docker", "kubernetes", "aws", "azure",
    "gcp", "cloud computing", "rest api", "flask", "django", "streamlit",
    "fastapi", "mongodb", "mysql", "postgresql", "data cleaning",
    "data preprocessing", "feature engineering", "model evaluation",
    "communication", "teamwork", "problem solving", "leadership",
    "project management", "agile", "scrum",
]


def extract_skills(text, skill_list=SKILL_KEYWORDS):
    """
    Finds which skills from skill_list appear in the given text.

    Parameters:
        text (str): The text to search (job description or resume)
        skill_list (list): List of skill keywords to search for

    Returns:
        set: Skills found in the text (lowercased)
    """
    text_lower = text.lower()
    found_skills = set()

    for skill in skill_list:
        if skill.lower() in text_lower:
            found_skills.add(skill.lower())

    return found_skills


def get_missing_skills(jd_skills, resume_skills):
    """
    Returns skills required by the job description but absent from the resume.
    """
    return jd_skills - resume_skills


def calculate_ats_score(jd_skills, resume_skills):
    """
    Calculates the percentage of job-description skills found in the resume.

    Returns:
        float: A percentage from 0 to 100
    """
    if not jd_skills:
        return 0.0

    matched_skills = jd_skills.intersection(resume_skills)
    return (len(matched_skills) / len(jd_skills)) * 100