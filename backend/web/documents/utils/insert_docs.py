import lancedb
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import LanceDB
from langchain_text_splitters import RecursiveCharacterTextSplitter

from web.documents.utils.custom import CustomEmbeddings

def insert_documents():
    loader = TextLoader('./web/documents/data.md', encoding='utf-8')
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    print(f"一切分成{len(texts)}个片段")

    embeddings = CustomEmbeddings()
    db = lancedb.connect('./web/documents/lancedb_storage')
    LanceDB.from_documents(documents=texts, embedding=embeddings, connection=db, table_name='my_knowledge_base', mode='overwrite')

    table = db.open_table('my_knowledge_base')
    table.create_fts_index('text', replace=True)

    print(f"已插入{table.count_rows()}行数据")
