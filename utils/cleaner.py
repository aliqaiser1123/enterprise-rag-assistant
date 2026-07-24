import re


def clean_data(docs):
    for doc in docs:
        for source, data in doc.items():
            data[0] = re.sub(r"\s+", " ", data[0]).strip()
    return docs
