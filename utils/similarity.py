from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(embedding1, embedding2):
    """
    Calculates the cosine similarity between two embedding vectors.

    Parameters:
        embedding1 (numpy.ndarray): First embedding vector (e.g., job description)
        embedding2 (numpy.ndarray): Second embedding vector (e.g., a resume)

    Returns:
        float: A similarity score between -1 and 1 (typically 0 to 1 in practice)
    """
    score = cosine_similarity([embedding1], [embedding2])

    # Convert from numpy.float32 to a native Python float —
    # Streamlit's UI components (e.g. st.progress) require plain Python floats
    return float(score[0][0])
