from sklearn.feature_extraction.text import TfidfVectorizer

# Fallback keyword list — used ONLY if TF-IDF extraction
# returns too few keywords (e.g. very short job description)
FALLBACK_KEYWORDS = [
    "python", "java", "sql", "machine learning", "deep learning",
    "nlp", "data analysis", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "git", "docker", "aws", "azure",
    "communication", "teamwork", "problem solving", "leadership",
]


def extract_keywords_from_text(text, top_n=20):
    """
    Dynamically extracts the most important keywords from any text
    using TF-IDF scoring — works for any domain (tech, HR, marketing, etc.)

    Parameters:
        text (str): The text to extract keywords from (usually job description)
        top_n (int): How many top keywords to extract

    Returns:
        set: A set of important keyword strings (lowercased)
    """
    # TfidfVectorizer converts text into TF-IDF scores per word
    # stop_words="english" automatically filters out common words
    # like "the", "and", "is", "a" — they have low IDF scores anyway
    # ngram_range=(1,2) captures both single words ("python")
    # and two-word phrases ("machine learning", "data analysis")
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=500
    )

    try:
        # fit_transform learns the vocabulary and scores from our text
        # We wrap text in a list because TfidfVectorizer expects
        # a list of documents, even if we only have one
        tfidf_matrix = vectorizer.fit_transform([text])

        # Get the feature names (the actual words/phrases)
        feature_names = vectorizer.get_feature_names_out()

        # Get the TF-IDF scores for our single document
        # .toarray()[0] converts sparse matrix to a flat array of scores
        scores = tfidf_matrix.toarray()[0]

        # Pair each word with its score, sort by score descending,
        # take the top_n highest scoring words
        top_keywords = sorted(
            zip(feature_names, scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

        # Return just the words (not the scores) as a set
        keywords = {word for word, score in top_keywords if score > 0}

        # If we got enough keywords, return them
        if len(keywords) >= 5:
            return keywords

        # If JD was too short/vague, fall back to our manual list
        return set(FALLBACK_KEYWORDS)

    except Exception as e:
        print(f"TF-IDF extraction failed: {e}")
        return set(FALLBACK_KEYWORDS)


def extract_skills(text, skill_list=None):
    """
    Checks which keywords from skill_list appear in the given text.

    Parameters:
        text (str): Resume text to search through
        skill_list (set): Keywords to look for (from JD's TF-IDF extraction)

    Returns:
        set: Keywords found in the text
    """
    if skill_list is None:
        skill_list = set(FALLBACK_KEYWORDS)

    text_lower = text.lower()
    found = set()

    for keyword in skill_list:
        if keyword.lower() in text_lower:
            found.add(keyword.lower())

    return found


def get_missing_skills(jd_skills, resume_skills):
    """
    Returns skills required by JD but absent from the resume.
    """
    return jd_skills - resume_skills


def calculate_ats_score(jd_skills, resume_skills):
    """
    Calculates what percentage of JD keywords appear in the resume.

    Returns:
        float: Percentage from 0 to 100
    """
    if not jd_skills:
        return 0.0

    matched = jd_skills.intersection(resume_skills)
    return (len(matched) / len(jd_skills)) * 100
