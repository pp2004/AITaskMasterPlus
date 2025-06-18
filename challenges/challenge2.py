import streamlit as st
import os
from utils.ai_client import AzureOpenAIClient
from utils.prompt_templates import CYBERSECURITY_SYSTEM_PROMPT

def render_challenge2():
    st.header("🔧 Challenge 2: Azure OpenAI Integration")
    st.markdown("Programmatically interact with LLMs using Python and Azure OpenAI SDK")
    
    ai_client = AzureOpenAIClient()
    
    # Environment Setup Display
    st.subheader("1. Environment Configuration")
    
    with st.expander("🔧 View Current Configuration"):
        st.markdown("**Current Azure OpenAI Configuration:**")
        st.code(f"""
OPENAI_API_KEY: {'*' * 10 + os.getenv('OPENAI_API_KEY', 'Not Set')[-4:] if os.getenv('OPENAI_API_KEY') else 'Not Set'}
OPENAI_API_BASE: {os.getenv('OPENAI_API_BASE', 'Not Set')}
OPENAI_API_VERSION: {os.getenv('OPENAI_API_VERSION', 'Not Set')}
OPENAI_DEPLOYMENT: {os.getenv('OPENAI_DEPLOYMENT', 'Not Set')}
        """)
        
        st.markdown("**Required .env format:**")
        st.code("""
OPENAI_API_KEY=your_key
OPENAI_API_BASE=your_endpoint
OPENAI_API_VERSION=2024-12-01-preview
OPENAI_DEPLOYMENT=o3-mini
        """)
    
    st.markdown("---")
    
    # Cybersecurity Query Section
    st.subheader("2. Cybersecurity Expert Queries")
    
    topics = {
        "DNS Security": "How does DNS work and what are the main security risks associated with DNS infrastructure?",
        "Encryption": "Explain how modern encryption works and what are the best practices for implementing encryption in web applications?", 
        "2FA (Two-Factor Authentication)": "How does 2FA work and what are the different types of 2FA methods available?"
    }
    
    selected_topic = st.selectbox("Select a cybersecurity topic:", list(topics.keys()))
    custom_query = st.text_area("Or enter your custom cybersecurity question:", 
                                placeholder="e.g., Explain zero-trust security architecture")
    
    query = custom_query if custom_query.strip() else topics[selected_topic]
    
    if st.button("🔍 Query Cybersecurity Expert", key="cyber_query"):
        with st.spinner("Consulting cybersecurity expert..."):
            messages = [
                {"role": "system", "content": CYBERSECURITY_SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ]
            
            response = ai_client.get_completion(messages, max_completion_tokens=800)
            if response:
                st.success("Expert Analysis Complete!")
                st.markdown("### 🛡️ Cybersecurity Expert Response:")
                st.markdown(response)
    
    st.markdown("---")
    
    # Parameter Tuning Experiment
    st.subheader("3. Parameter Tuning Experiment")
    st.markdown("Compare outputs with different temperature and max_tokens settings")
    
    experiment_query = st.text_input("Enter query for parameter experiment:", 
                                     value="Explain the fundamentals of network security",
                                     key="param_query")
    
    if st.button("🧪 Run Parameter Experiment", key="param_experiment"):
        if experiment_query.strip():
            st.markdown("### 📊 Parameter Tuning Results")
            
            # Create columns for side-by-side comparison
            col1, col2 = st.columns(2)
            
            # Conservative settings (fewer tokens)
            with col1:
                st.markdown("#### 🎯 Conservative Settings")
                st.markdown("**Max Completion Tokens: 300**")
                
                with st.spinner("Generating conservative response..."):
                    messages = [
                        {"role": "system", "content": CYBERSECURITY_SYSTEM_PROMPT},
                        {"role": "user", "content": experiment_query}
                    ]
                    
                    conservative_response = ai_client.get_completion_with_tokens(
                        messages, max_completion_tokens=300
                    )
                    
                    if conservative_response:
                        st.markdown("**Response:**")
                        if conservative_response.get("content"):
                            st.markdown(conservative_response["content"])
                        else:
                            st.error("No response content received")
                        st.markdown("**Token Usage:**")
                        if conservative_response.get("usage"):
                            usage = conservative_response["usage"]
                            st.markdown(f"- Prompt tokens: {usage.prompt_tokens}")
                            st.markdown(f"- Completion tokens: {usage.completion_tokens}")
                            st.markdown(f"- Total tokens: {usage.total_tokens}")
                        else:
                            st.error("No token usage information available")
                    else:
                        st.error("Failed to get response from Azure OpenAI")
            
            # Extended settings (more tokens)
            with col2:
                st.markdown("#### 🎨 Extended Settings")
                st.markdown("**Max Completion Tokens: 700**")
                
                with st.spinner("Generating extended response..."):
                    messages = [
                        {"role": "system", "content": CYBERSECURITY_SYSTEM_PROMPT},
                        {"role": "user", "content": experiment_query}
                    ]
                    
                    creative_response = ai_client.get_completion_with_tokens(
                        messages, max_completion_tokens=700
                    )
                    
                    if creative_response:
                        st.markdown("**Response:**")
                        if creative_response.get("content"):
                            st.markdown(creative_response["content"])
                        else:
                            st.error("No response content received")
                        st.markdown("**Token Usage:**")
                        if creative_response.get("usage"):
                            usage = creative_response["usage"]
                            st.markdown(f"- Prompt tokens: {usage.prompt_tokens}")
                            st.markdown(f"- Completion tokens: {usage.completion_tokens}")
                            st.markdown(f"- Total tokens: {usage.total_tokens}")
                        else:
                            st.error("No token usage information available")
                    else:
                        st.error("Failed to get response from Azure OpenAI")
            
            # Analysis
            st.markdown("---")
            st.markdown("### 📈 Analysis")
            
            analysis_prompt = f"""
            Compare these two responses to the query "{experiment_query}":
            
            Conservative Response (max_completion_tokens=200):
            {conservative_response['content'] if conservative_response else 'Failed to generate'}
            
            Extended Response (max_completion_tokens=500):
            {creative_response['content'] if creative_response else 'Failed to generate'}
            
            Analyze the differences in:
            1. Response length and detail
            2. Technical depth and coverage
            3. Token efficiency
            4. Practical recommendations for when to use each setting
            """
            
            with st.spinner("Analyzing parameter differences..."):
                analysis_messages = [
                    {"role": "system", "content": "You are an AI researcher analyzing model parameter effects."},
                    {"role": "user", "content": analysis_prompt}
                ]
                
                analysis = ai_client.get_completion(analysis_messages, max_completion_tokens=600)
                if analysis:
                    st.markdown(analysis)
    
    # Code Example
    with st.expander("💻 View Implementation Code"):
        st.markdown("### Python Implementation Example")
        st.code('''
from openai import AzureOpenAI
import os

# Initialize client
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_API_BASE")
)

# Cybersecurity expert prompt
messages = [
    {
        "role": "system", 
        "content": "You are a cybersecurity expert with extensive knowledge..."
    },
    {
        "role": "user", 
        "content": "Explain DNS security risks"
    }
]

# Get response
response = client.chat.completions.create(
    model=os.getenv("OPENAI_DEPLOYMENT"),
    messages=messages,
    temperature=0.2,
    max_tokens=200
)

print(response.choices[0].message.content)
        ''', language="python")
