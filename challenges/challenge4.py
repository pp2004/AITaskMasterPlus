import streamlit as st
import os
import tempfile
from pathlib import Path
import PyPDF2
import io
from utils.ai_client import AzureOpenAIClient
from utils.prompt_templates import SECURITY_VULNERABILITIES

def render_challenge4():
    st.header("🛡️ Challenge 4: RAG & Security Implementation")
    st.markdown("Build a secure RAG pipeline with Azure Blob Storage considerations")
    
    ai_client = AzureOpenAIClient()
    
    # Task 1: Local RAG Setup
    st.subheader("1. Local RAG Document Processing")
    
    # File upload for RAG documents
    uploaded_files = st.file_uploader(
        "Upload documents for RAG processing",
        type=['txt', 'md', 'pdf'],
        accept_multiple_files=True,
        help="Upload text files that will be used for RAG demonstration"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} document(s) uploaded successfully!")
        
        # Process documents
        documents = []
        for file in uploaded_files:
            try:
                if file.type == "text/plain":
                    content = str(file.read(), "utf-8")
                elif file.type == "application/pdf":
                    # Process PDF files
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                    content = ""
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n"
                    if not content.strip():
                        content = f"[{file.name}] - PDF processed but no text could be extracted"
                elif file.name.endswith('.md'):
                    content = str(file.read(), "utf-8")
                else:
                    content = f"[{file.name}] - Unsupported file format. Supported formats: .txt, .md, .pdf"
                
                documents.append({
                    "filename": file.name,
                    "content": content[:500] + "..." if len(content) > 500 else content,
                    "full_content": content
                })
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
                documents.append({
                    "filename": file.name,
                    "content": f"[{file.name}] - Error: {str(e)}",
                    "full_content": f"Error processing file: {str(e)}"
                })
        
        # Display document summaries
        with st.expander("📄 View Document Summaries"):
            for doc in documents:
                st.markdown(f"**{doc['filename']}**")
                st.text(doc['content'])
                st.markdown("---")
        
        # RAG Query Interface
        st.markdown("### 🔍 Query Your Documents")
        user_query = st.text_input("Ask a question about your uploaded documents:",
                                  placeholder="e.g., What are the main topics covered in these documents?")
        
        if st.button("🚀 Process RAG Query", key="rag_query") and user_query:
            with st.spinner("Searching documents and generating response..."):
                # Combine document contents
                combined_content = "\n\n".join([f"Document: {doc['filename']}\n{doc['full_content']}" for doc in documents])
                
                # RAG prompt
                rag_prompt = f"""
                Based on the following documents, answer the user's question. If the information is not available in the documents, clearly state that.
                
                Documents:
                {combined_content}
                
                User Question: {user_query}
                
                Please provide a comprehensive answer based only on the information in the provided documents.
                """
                
                messages = [
                    {"role": "system", "content": "You are a helpful assistant that answers questions based strictly on provided documents."},
                    {"role": "user", "content": rag_prompt}
                ]
                
                response = ai_client.get_completion(messages, max_completion_tokens=1000)
                if response:
                    st.success("RAG Response Generated!")
                    st.markdown("### 📋 Answer:")
                    st.markdown(response)
    else:
        # Provide sample documents option
        if st.button("📁 Create Sample Documents", key="create_samples"):
            sample_docs = {
                "cybersecurity_basics.txt": """
                Cybersecurity Fundamentals
                
                Network Security: Protecting computer networks from intrusion, whether targeted attacks or opportunistic malware.
                
                Encryption: The process of converting information into a secret code that hides the information's true meaning.
                
                Authentication: The process of verifying the identity of a user, process, or device.
                
                Firewalls: Network security devices that monitor and filter incoming and outgoing network traffic.
                """,
                "ai_security_trends.txt": """
                AI Security Trends 2024
                
                Machine Learning Security: Protecting ML models from adversarial attacks and data poisoning.
                
                Automated Threat Detection: Using AI to identify and respond to security threats in real-time.
                
                Privacy-Preserving AI: Techniques like federated learning and differential privacy to protect user data.
                
                Supply Chain Security: Ensuring the integrity of AI models and training data throughout the development lifecycle.
                """,
                "compliance_frameworks.txt": """
                Security Compliance Frameworks
                
                NIST Cybersecurity Framework: A policy framework of computer security guidance for how private sector organizations can assess and improve their ability to prevent, detect, and respond to cyber attacks.
                
                ISO 27001: International standard for information security management systems (ISMS).
                
                SOC 2: Auditing procedure that ensures service providers securely manage data to protect the interests of the organization and the privacy of its clients.
                
                GDPR: European Union regulation on data protection and privacy for all individuals within the EU and European Economic Area.
                """
            }
            
            st.session_state.sample_docs = sample_docs
            st.success("✅ Sample documents created! You can now query them below.")
    
    # Sample documents RAG
    if hasattr(st.session_state, 'sample_docs'):
        st.markdown("### 📚 Sample Documents Available")
        
        sample_query = st.text_input("Query sample documents:",
                                   placeholder="e.g., What is NIST Cybersecurity Framework?",
                                   key="sample_query")
        
        if st.button("🔍 Query Sample Documents", key="sample_rag") and sample_query:
            with st.spinner("Processing query against sample documents..."):
                combined_sample_content = "\n\n".join([f"Document: {filename}\n{content}" 
                                                      for filename, content in st.session_state.sample_docs.items()])
                
                rag_prompt = f"""
                Based on the following cybersecurity documents, answer the user's question:
                
                {combined_sample_content}
                
                Question: {sample_query}
                
                Provide a detailed answer based on the information in the documents.
                """
                
                messages = [
                    {"role": "system", "content": "You are a cybersecurity expert answering questions based on provided documentation."},
                    {"role": "user", "content": rag_prompt}
                ]
                
                response = ai_client.get_completion(messages, max_completion_tokens=1000)
                if response:
                    st.markdown("### 📋 Answer from Sample Documents:")
                    st.markdown(response)
    
    st.markdown("---")
    
    # Task 2: Azure Integration Research
    st.subheader("2. Azure Services for RAG Scaling")
    
    if st.button("🔍 Research Azure RAG Services", key="azure_research"):
        with st.spinner("Researching Azure services for RAG implementation..."):
            azure_prompt = """
            Research and propose Azure services for building a production-ready RAG (Retrieval-Augmented Generation) pipeline. 
            
            Focus on:
            1. Azure AI Search - for vector search and document indexing
            2. Azure Cognitive Services - for entity recognition and content processing
            3. Azure Blob Storage - for document storage
            4. Azure OpenAI - for embeddings and completions
            5. Azure Functions - for serverless processing
            
            Provide:
            - Service descriptions
            - How they work together in a RAG pipeline
            - Cost considerations
            - Performance benefits
            - Security features
            """
            
            messages = [
                {"role": "system", "content": "You are an Azure solutions architect specializing in AI and search services."},
                {"role": "user", "content": azure_prompt}
            ]
            
            response = ai_client.get_completion(messages, max_completion_tokens=700)
            if response:
                st.success("Azure RAG Architecture Research Complete!")
                st.markdown(response)
    
    st.markdown("---")
    
    # Task 3: Security Mitigations
    st.subheader("3. Security Vulnerability Mitigations")
    
    st.markdown("### 🛡️ Key AI/RAG Security Vulnerabilities and Mitigations")
    
    # Display vulnerability table
    vulnerability_data = []
    for vuln, details in SECURITY_VULNERABILITIES.items():
        vulnerability_data.append({
            "Vulnerability": vuln,
            "Description": details["description"],
            "Mitigation Strategy": details["mitigation"]
        })
    
    for vuln_info in vulnerability_data:
        with st.expander(f"🚨 {vuln_info['Vulnerability']}"):
            st.markdown(f"**Description:** {vuln_info['Description']}")
            st.markdown(f"**Mitigation:** {vuln_info['Mitigation Strategy']}")
    
    # Deep dive analysis
    selected_vulnerability = st.selectbox("Select vulnerability for detailed analysis:",
                                        list(SECURITY_VULNERABILITIES.keys()))
    
    if st.button("🔬 Analyze Security Vulnerability", key="security_analysis"):
        with st.spinner("Generating detailed security analysis..."):
            vuln_details = SECURITY_VULNERABILITIES[selected_vulnerability]
            
            analysis_prompt = f"""
            Provide a comprehensive analysis of the "{selected_vulnerability}" vulnerability in AI/RAG systems:
            
            Current understanding:
            - Description: {vuln_details['description']}
            - Basic Mitigation: {vuln_details['mitigation']}
            
            Please expand on:
            1. Technical details of how this attack works
            2. Real-world examples or case studies
            3. Advanced mitigation strategies beyond the basic approach
            4. Implementation considerations for Azure-based RAG systems
            5. Monitoring and detection methods
            6. Compliance implications (GDPR, SOC2, etc.)
            """
            
            messages = [
                {"role": "system", "content": "You are a cybersecurity expert specializing in AI security and threat mitigation."},
                {"role": "user", "content": analysis_prompt}
            ]
            
            response = ai_client.get_completion(messages, max_completion_tokens=700)
            if response:
                st.success("Detailed Security Analysis Complete!")
                st.markdown(f"### 🛡️ Deep Dive: {selected_vulnerability}")
                st.markdown(response)
    
    # Code examples
    with st.expander("💻 Implementation Examples"):
        st.markdown("### Document Processing Code Example")
        st.code('''
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores import FAISS

# Load documents
loader = DirectoryLoader('./documents/', glob="**/*.txt")
documents = loader.load()

# Split documents
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Create embeddings
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY")
)

# Create vector store
vectorstore = FAISS.from_documents(texts, embeddings)

# Query
query = "What are the security best practices?"
docs = vectorstore.similarity_search(query, k=3)
        ''', language="python")
        
        st.markdown("### Security Implementation Example")
        st.code('''
import re
from typing import List

class RAGSecurityFilter:
    def __init__(self):
        # Patterns to filter sensitive information
        self.pii_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b',  # Credit card
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email
        ]
    
    def filter_output(self, text: str) -> str:
        """Remove sensitive information from outputs"""
        filtered_text = text
        for pattern in self.pii_patterns:
            filtered_text = re.sub(pattern, '[REDACTED]', filtered_text)
        return filtered_text
    
    def validate_input(self, query: str) -> bool:
        """Validate input queries for malicious content"""
        malicious_patterns = [
            r'ignore\s+previous\s+instructions',
            r'system\s+prompt',
            r'jailbreak'
        ]
        
        for pattern in malicious_patterns:
            if re.search(pattern, query.lower()):
                return False
        return True

# Usage
security_filter = RAGSecurityFilter()
        ''', language="python")
    
    # Summary
    st.markdown("---")
    st.markdown("### 📊 Challenge 4 Summary")
    
    summary_cols = st.columns(3)
    
    with summary_cols[0]:
        st.metric("Security Vulnerabilities", "4", "Identified & Mitigated")
    
    with summary_cols[1]:
        st.metric("Azure Services", "5+", "For Production RAG")
    
    with summary_cols[2]:
        st.metric("Implementation", "Ready", "Code Examples Provided")
