from langchain_text_splitters import RecursiveCharacterTextSplitter

class HybridChunker:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            # Priority: Sections -> Paragraphs -> Sentences -> Words
            separators=["\n\n", "\n", ". ", " ", ""],
            add_start_index=True
        )

    def chunk_documents(self, raw_documents):
        """
        Takes list of {'content': str, 'metadata': dict}
        Returns list of chunks with merged metadata.
        """
        all_chunks = []

        for doc in raw_documents:
            content = doc.get('content', '')
            base_metadata = doc.get('metadata', {})

            # Apply the structural + sliding window split
            chunks = self.splitter.create_documents([content])

            for i, chunk in enumerate(chunks):
                # Build unified metadata for each chunk
                chunk_metadata = base_metadata.copy()
                chunk_metadata.update({
                    'chunk_index': i,
                    'start_index': chunk.metadata.get('start_index', 0)
                })

                all_chunks.append({
                    'content': chunk.page_content,
                    'metadata': chunk_metadata
                })

        return all_chunks