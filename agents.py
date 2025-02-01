from tools import load_dataset, preprocess_data, create_faiss_index, create_pinecone_index
import crewai

class JobSuggestionAgent:
    def __init__(self, csv_path, use_faiss=True):
        self.df = load_dataset(csv_path)
        self.df = preprocess_data(self.df)
        self.use_faiss = use_faiss
        if use_faiss:
            self.index, self.vectorizer = create_faiss_index(self.df)
        else:
            self.index = create_pinecone_index(self.df, 'job_index')

    def suggest_jobs(self, query):
        query_vector = self.vectorizer.transform([query]).toarray()
        if self.use_faiss:
            D, I = self.index.search(query_vector, k=5)
            return self.df.iloc[I[0]]
        else:
            results = self.index.query(query_vector.tolist(), top_k=5)
            return [self.df.iloc[result['id']] for result in results]

    def perform_ocr_and_suggest_jobs(self, pdf_path):
        ocr_text = crewai.ocr(pdf_path)
        return self.suggest_jobs(ocr_text)