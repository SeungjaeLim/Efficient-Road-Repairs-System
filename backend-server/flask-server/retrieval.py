import json
import faiss
from sentence_transformers import SentenceTransformer
from config import DUMMY_DATA_FILE
from utils import log_retrieval, log_error

sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
faiss_index = None
sentences = []


def load_dummy_data():
    """
    Load dummy data from the DUMMY_DATA_FILE, encode them using SBERT,
    and build a FAISS index for similarity search.
    """
    global faiss_index, sentences
    try:
        with open(DUMMY_DATA_FILE, "r") as file:
            dummy_data = json.load(file)

        sentences = [json.dumps(item) for item in dummy_data if isinstance(item, dict)]
        unique_sentences = list(set(sentences))
        embeddings = sbert_model.encode(unique_sentences)

        dimension = embeddings.shape[1]
        faiss_index = faiss.IndexFlatL2(dimension)
        faiss_index.add(embeddings)

        print("Dummy data and FAISS index loaded successfully.")
    except Exception as e:
        log_error(f"Error loading dummy data: {e}")


def retrieve_similar_data(input_data):
    """
    Retrieve similar data entries from the FAISS index given an input object.

    :param input_data: Dictionary representing the input for similarity retrieval.
    :return: A list of similar data items.
    """
    if faiss_index is None:
        return []
    try:
        input_sentence = json.dumps(input_data)
        input_embedding = sbert_model.encode([input_sentence])
        D, I = faiss_index.search(input_embedding, k=3)
        log_retrieval(f"Retrieved indices: {I[0].tolist()}")
        similar_data = [json.loads(sentences[i]) for i in I[0] if i < len(sentences)]
        return similar_data
    except Exception as e:
        log_error(str(e))
        return []
