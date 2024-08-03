import os
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import MarkdownElementNodeParser, SemanticSplitterNodeParser
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone.grpc import PineconeGRPC as Pinecone
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from pinecone import ServerlessSpec
import nest_asyncio

load_dotenv()

class Inference:
    def __init__(self):


        self.llm = OpenAI(model=os.getenv('openai_model'), api_key=os.getenv("OPENAI_API_KEY"))
        self.embed_model = OpenAIEmbedding(model=os.getenv('Embed_Model'), api_key=os.getenv("OPENAI_API_KEY"))
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model

        self.node_parser = MarkdownElementNodeParser(model=os.getenv('openai_model'), num_workers=8)

    def load_docs(self, path: str):
        nest_asyncio.apply()
        documents = LlamaParse(
            result_type='markdown',
            api_key=os.getenv('LLAMA_CLOUD_API_KEY')).load_data(file_path=path)
        return documents

    def get_chunks(self, documents):
        nodes = self.node_parser.get_nodes_from_documents(documents)
        return nodes

    def _create_pinecone_index(self, index_name):
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        if index_name not in pc.list_indexes().names():
            dimension = 1536  # Make configurable
            metric = "cosine"  # Make configurable
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
        return PineconeVectorStore(index_name=index_name)

    def _query_engine(self, pdf_path, ques):
        nest_asyncio.apply()
        docs = self.load_docs(pdf_path)
        nodes = self.get_chunks(docs)

        index_name = "advance-rag"
        vector_store = self._create_pinecone_index(index_name)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        reranker = FlagEmbeddingReranker(
            top_n=5,
            model=os.getenv('Reranker_model')
        )

        recursive_index = VectorStoreIndex.from_documents(docs,
                                                        node_parser=self.node_parser,
                                                        storage_context=storage_context,
                                                        verbose=True)

        reranker_recursive_index = recursive_index.as_query_engine(similarity_top_k=5,
                                                                node_postprocessors=[reranker],
                                                                verbose=True)

        response = reranker_recursive_index.query(ques)
        return response


inference = Inference()

path = 'cleaned_crawled_data.pdf'
questions = [
    "What has been the primary focus of Pratham's efforts over the last two decades?",
    "What approach has evolved from these efforts to address the learning crisis among children in India?",
    "What are the key elements of Pratham's approach towards Early Childhood Education?",
    "What are the main interventions and focus areas of the Chatham Council for Vulnerable Children (PCVC) in protecting child rights and safeguarding children?",
    "What was the primary reason for Rukmini Banerji being conferred the Doctor of Letters honors cause by Area University?"
]

responses = {}

for question in questions:
    response = inference._query_engine(path, ques=question)
    responses[question] = response

print(responses)