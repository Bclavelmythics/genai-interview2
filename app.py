import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import Together
from langchain.chains import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import os

# ============ USER CONFIG SECTION ============
VECTOR_DB_PATH = "oci_security_db"
TOGETHER_API_KEY = "a85b803f2f7e8fdb3d7681d77c6d399cd273d2bbebede92ba9e795a7ba730833"  # User should modify this
# =============================================

os.environ["TOGETHER_API_KEY"] = TOGETHER_API_KEY

def chunk_document(text):
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=0, 
        separator=" "     
    )
    return text_splitter.split_text(text)

def initialize_vectordb():
    if not VECTOR_DB_PATH:
        return None
    
    # Load document content
    with open("./docs/oci_security.md", "r") as f:
        content = f.read()
    
    # Create chunks
    chunks = chunk_document(content)
    
    # Initialize basic embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create and return vector store
    return Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )

def get_context(query, vectordb=None):
    if vectordb is None:
        return ""
    
    results = vectordb.similarity_search(
        query=query,
        k=5  
    )
    
    return results[0].page_content if results else ""

def display_context(context):
    """
    Display retrieved context in an expandable section with formatting
    """
    with st.expander("📚 View Retrieved Context", expanded=False):
        st.markdown("### Retrieved Document Chunks")
        st.markdown("---")
        st.markdown(context)
        st.markdown("---")
        st.caption("Note: This shows the raw context chunks used to generate the response.")

def main():
    st.title("OCI Security Services")
    
    # Initialize vector database
    vectordb = initialize_vectordb()
    
    if vectordb:
        st.info("Vector database loaded successfully! Using contextual responses.")
    else:
        st.info("No vector database configured. The assistant will provide general responses.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    query = st.chat_input("Enter your question about OCI security services:")
    
    if query:
        # Display user message
        with st.chat_message("user"):
            st.markdown(query)
        
        
        context = get_context(query, vectordb) if vectordb else ""
        
        if context:
            display_context(context)

        try:
            llm = Together(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                max_tokens=500
            )
            prompt = PromptTemplate(
                template="""
                Here's some context: {context}
                Answer this question: {question}
                """,
                input_variables=["context", "question"]
            )
            
            chain = LLMChain(llm=llm, prompt=prompt)
            response = chain.run(
                context=context if context else "",
                question=query
            )
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)

    
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()