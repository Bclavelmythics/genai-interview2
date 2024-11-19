# genai-interview2
Second set of problems revolved around Generative AI 

## Prerequisites

* Sign up on together.ai and obtain an API key
    * clone this repository git clone https://github.com/Bclavelmythics/genai-interview2.git
* Use python 3.11 and install requirements
    * pip3.11 install -r requirements.txt
* If installing requirements fail run the following commands instead
    * pip3.11 install streamlit
    * pip3.11 install langchain
    * pip3.11 install langchain_community




## Problem 1: Document Chunking

Current Implementation
```python
def chunk_document(text):
    return CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        separator=" "
    ).split_text(text)
```
This basic implementation fails to maintain context across sections and loses hierarchical document structure.

### Task
Implement improved chunking that:

* Preserves section headers and hierarchical relationships
* Maintains technical details together (setup instructions, code blocks)
* Implements appropriate chunk overlap


## Problem 2: Context Retrieval

Current Implementation
```python
def get_context(query, vectordb):
    return vectordb.similarity_search(query, k=5)[0].page_content
```
Simple similarity search fails to capture complex relationships in technical documentation.

### Task
Design a retrieval system that:

* Handles multi-intent questions about service relationships
* Retrieves setup instructions with related security best practices
* Implements hybrid search (semantic + keyword)



## Problem 3: Prompt Engineering

Current Implementation
```python
template="""
Here's some context: {context}
Answer this question: {question}
"""
```
Basic prompt template lacks guidance for technical documentation Q&A.

### Task
Create a prompt template that:

* Provides framework for technical explanations
* Handles security-specific terminology
* Enables step-by-step instruction delivery



## Bonus Problem: Conversation Management

Application is not able to recall conversation history therefore is unable to participate in interactive conversation with user

### Task
Implement conversation handling that:

* Maintains context across multiple questions about the same service
* Tracks setup instruction progress
* Handles clarification questions
* Manages conversation state for complex technical discussions



## Example Questions for LLM to test Application Performance
* What's the recommended way to manage encryption keys and secrets across multiple OCI services?
* How can I automate security scanning in my CI/CD pipeline using OCI's vulnerability scanning service?
* How can I set up automated remediation for common security issues?
