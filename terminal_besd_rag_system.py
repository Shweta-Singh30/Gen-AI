
from dotenv import load_dotenv
from openai import OpenAI
import faiss
import numpy as np
from PyPDF2 import PdfReader
import tiktoken

 
load_dotenv()

client=OpenAI()


def num_tokens_from_string(string: str, model_name: str = embedding_model) -> int:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(string))


def split_text(text, max_tokens=chunk_size):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = tokens[i:i+max_tokens]
        chunks.append(encoding.decode(chunk))
    return chunks

def load_document(file_path):
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return " ".join([page.extract_text() for page in reader.pages])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise Exception("Unsupported file format")


def get_embedding(text):
    response = openai.Embedding.create(input=[text], model=embedding_model)
    return np.array(response['data'][0]['embedding'], dtype=np.float32)

def build_faiss_index(chunks):
    dimension = len(get_embedding("Test"))
    index = faiss.IndexFlatL2(dimension)
    embeddings = []
    for chunk in chunks:
        embeddings.append(get_embedding(chunk))
    index.add(np.array(embeddings))
    return index, embeddings


def rag_query(user_query, chunks, index, embeddings):
    query_vector = get_embedding(user_query)
    D, I = index.search(np.array([query_vector]), top_k)
    context = "\n".join([chunks[i] for i in I[0]])
    prompt = f"""Answer the question based on the context below:\n\nContext:\n{context}\n\nQuestion: {user_query}"""
    
    response = openai.ChatCompletion.create(
        model=completion_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=300
    )
    return response['choices'][0]['message']['content']


def main():
    file_path = input("Enter path to your PDF or TXT file: ")
    print("📄 Loading and chunking document...")
    full_text = load_document(file_path)
    chunks = split_text(full_text)
    
    print(f"📚 Total chunks created: {len(chunks)}")
    print("🔍 Creating FAISS vector index...")
    index, embeddings = build_faiss_index(chunks)

    print("\n✅ Ready! Ask your question (type 'exit' to quit)\n")
    while True:
        query = input("You: ")
        if query.lower() in ['exit', 'quit']:
            break
        answer = rag_query(query, chunks, index, embeddings)
        print("\nAssistant:", answer)
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()
