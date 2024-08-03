"""
Embed_Model = text-embedding-3-small
Reranker_model = BAAI/bge-reranker-large
openai_model = gpt-3.5-turbo-0125
vector_database = Pinecone
Libraries used for RAG: Llamaindex, Llamaparse, nest_asycio
Libraries used for web crawler and data cleaning: requests, beautiful soup, nltk, re, textblob, hashlib etc.

{"What has been the primary focus of Pratham's efforts over the last two decades?":
Response(response="The primary focus of Pratham's efforts over the last two decades has been on improving the quality of education in India, particularly by addressing gaps in education systems and promoting the development of children through innovative interventions."
'What approach has evolved from these efforts to address the learning crisis among children in India?':
Response(response='The approach that has evolved from these efforts to address the learning crisis among children in India is focusing on the politic development of children and implementing innovative interventions to improve the quality of education.'
"What are the key elements of Pratham's approach towards Early Childhood Education?":
Response(response="The key elements of Pratham's approach towards Early Childhood Education include focusing on the political development of children and supporting girls and women.",
'What are the main interventions and focus areas of the Chatham Council for Vulnerable Children (PCVC) in protecting child rights and safeguarding children?':
Response(response= 'The main interventions and focus areas of the Chatham Council for Vulnerable Children (PCVC) in protecting child rights and safeguarding children include addressing gaps in education systems, focusing on the political development of children, supporting girls and women, and ensuring access to quality education for all children.'
'What was the primary reason for Rukmini Banerji being conferred the Doctor of Letters honors cause by Area University?':
Response(response='Rukmini Banerji was conferred the Doctor of Letters honors cause by Area University due to her contributions and achievements.',

GPT-3.5-Turbo-0125
Input Cost: $0.0005 per 1,000 tokens
Output Cost: $0.0015 per 1,000 tokens
For 1,500 tokens per user:

Input Cost: ( 1.5 \times 0.0005 = $0.00075 )
Output Cost: ( 1.5 \times 0.0015 = $0.00225 )
Total Cost per User: ( $0.00075 + $0.00225 = $0.003 )
For 1,000 users:

Total Cost: ( 1,000 \times $0.003 = $3 )
2. Text-Embedding-3-Small
Cost: $0.00002 per 1,000 tokens
For 1,500 tokens per user:

Cost per User: ( 1.5 \times 0.00002 = $0.00003 )
For 1,000 users:

Total Cost: ( 1,000 \times $0.00003 = $0.03 )

3. Azure V3 GPU
Cost: Approximately $3 per hour1
For 1 minute per user:

Cost per User: ( \frac{3}{60} = $0.05 )
For 1,000 users:

Total Cost: ( 1,000 \times $0.05 = $50 )
Total Cost for All Components
GPT-3.5-Turbo-0125: $3
Text-Embedding-3-Small: $0.03
Azure V3 GPU: $50
Grand Total: ( $3 + $0.03 + $50 = $53.03 )

"""