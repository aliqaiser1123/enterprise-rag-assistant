def chunk_data(docs, chunk_size, overlap):
    chunked_data = []
    for index, doc in enumerate(docs):
        chunks = []
        chunk_start_point = 0
        for source, data in doc.items():
            while chunk_start_point < len(data[0]):
                chunks.append(
                    data[0][chunk_start_point : chunk_start_point + chunk_size]
                )
                chunk_start_point += chunk_size - overlap
            chunked_data.append({source: chunks})
    return chunked_data
