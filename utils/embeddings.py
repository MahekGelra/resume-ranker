from sentence_transformers import SentenceTransformer

# Load the model once when this module is imported.
# Loading is slow (a few seconds) — we don't want to repeat this on every call.
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(text):
    """
    Converts a piece of text into a numeric embedding vector.

    Parameters:
        text (str): The input text (job description or resume text)

    Returns:
        numpy.ndarray: A 384-dimensional vector representing the text's meaning
    """
    embedding = model.encode(text)
    return embedding