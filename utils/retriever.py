def retrieve_data(model, query, database, n_results):
    query_embedding = model.encode(query)
    results = database.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results,
        include=["distances", "documents", "metadatas"],
    )
    return results
