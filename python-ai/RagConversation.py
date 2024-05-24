from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# does only work with OPENAI_API_KEY set
question = "Are Harley Quinn and Thanos righteous characters in the Avengers?"
documents = SimpleDirectoryReader("./data").load_data()
node_parser = VectorStoreIndex.from_documents(documents)
query_engine = node_parser.as_query_engine()
response = query_engine.query(question)
print(f"base query result: {response}")

# Output
#base query result: No, Harley Quinn and Thanos are not depicted as righteous characters in the Avengers series.