import os
import time
from openai import AzureOpenAI
import streamlit as st

class AzureOpenAIClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("OPENAI_API_BASE")
        )
        self.deployment = os.getenv("OPENAI_DEPLOYMENT")
    
    def get_completion(self, messages, max_completion_tokens=1000, max_retries=3):
        """Get completion from Azure OpenAI with retry mechanism"""
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.deployment,
                    messages=messages,
                    max_completion_tokens=max_completion_tokens
                )
                content = response.choices[0].message.content
                if content and content.strip() != "":
                    return content
                
                # Empty response - retry
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                    st.warning(f"Empty response received. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    st.error("Received empty response after all retry attempts")
                    return None
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt)
                    st.warning(f"API error occurred. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    st.error(f"Error calling Azure OpenAI after all retries: {str(e)}")
                    return None
        
        return None
    
    def get_completion_with_tokens(self, messages, max_completion_tokens=1000, max_retries=3):
        """Get completion with token usage information and retry mechanism"""
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.deployment,
                    messages=messages,
                    max_completion_tokens=max_completion_tokens
                )
                content = response.choices[0].message.content
                usage = response.usage if hasattr(response, 'usage') else None
                
                if content and content.strip() != "":
                    return {
                        "content": content,
                        "usage": usage
                    }
                
                # Empty response - retry
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt)
                    st.warning(f"Empty response received. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    st.error("Received empty response after all retry attempts")
                    return {
                        "content": None,
                        "usage": usage
                    }
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt)
                    st.warning(f"API error occurred. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    st.error(f"Error calling Azure OpenAI after all retries: {str(e)}")
                    return None
        
        return None
