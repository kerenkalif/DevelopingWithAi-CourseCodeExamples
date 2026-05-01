from langchain_community .document_loaders  import WebBaseLoader

URL = "https://en.wikipedia.org/wiki/LLM"

loader = WebBaseLoader(URL)
docs = loader.load()
print(docs[0].page_content.title)
print("~~~~~~~~~~~~~~~~~~~~~~~~")
print(docs[0].page_content)
