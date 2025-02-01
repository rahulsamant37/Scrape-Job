import pandas as pd
import faiss
import pinecone

def load_dataset(csv_path):
    df = pd.read_csv(csv_path)
    return df

def preprocess_data(df):
    # Example preprocessing: lowercasing and removing special characters
    df['job_description'] = df['job_description'].str.lower().str.replace('[^a-zA-Z0-9 ]', '')
    return df

def create_faiss_index(df):
    # Example: using job descriptions for indexing
    job_descriptions = df['job_description'].tolist()
    vectorizer = ...  # Define your vectorizer here
    vectors = vectorizer.fit_transform(job_descriptions).toarray()
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    return index, vectorizer

def create_pinecone_index(df, index_name):
    pinecone.init(api_key='YOUR_PINECONE_API_KEY')
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=128)  # Adjust dimension as needed
    index = pinecone.Index(index_name)
    return index