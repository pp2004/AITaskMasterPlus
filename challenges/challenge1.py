import streamlit as st
from utils.ai_client import AzureOpenAIClient
from utils.prompt_templates import PRODUCT_MANAGER_SYSTEM_PROMPT

def render_challenge1():
    st.header("🎯 Challenge 1: Product Ideation & Roadmap Development")
    st.markdown("Simulate a Product Manager's workflow using AI for ideation, prioritization, and planning.")
    
    ai_client = AzureOpenAIClient()
    
    # Initialize session state for product concepts
    if "product_concepts" not in st.session_state:
        st.session_state.product_concepts = []
    if "selected_concept" not in st.session_state:
        st.session_state.selected_concept = None
    
    # Task 1: Product Concept
    st.subheader("1. Product Concept Generation")
    
    # Product concept dropdown for existing concepts
    if st.session_state.product_concepts:
        selected_concept_index = st.selectbox(
            "Select an existing product concept or generate a new one:",
            range(len(st.session_state.product_concepts) + 1),
            format_func=lambda x: f"Concept {x+1}" if x < len(st.session_state.product_concepts) else "Generate New Concept",
            key="concept_selector"
        )
        
        if selected_concept_index < len(st.session_state.product_concepts):
            st.session_state.selected_concept = st.session_state.product_concepts[selected_concept_index]
            st.markdown("**Selected Product Concept:**")
            st.markdown(st.session_state.selected_concept)
    
    if st.button("Generate New Product Idea", key="product_concept"):
        with st.spinner("Generating product concept..."):
            messages = [
                {"role": "system", "content": PRODUCT_MANAGER_SYSTEM_PROMPT},
                {"role": "user", "content": """Generate a product idea for "AI-Powered Fraud Detection for E-Commerce". 
                Define:
                - Target audience
                - Unique Selling Proposition (USP)
                - 3 core features
                
                Format: 1-paragraph summary + bulleted list"""}
            ]
            
            response = ai_client.get_completion(messages, max_completion_tokens=600)
            if response:
                st.success("Product Concept Generated!")
                st.markdown(response)
                # Store the concept for future use
                st.session_state.product_concepts.append(response)
                st.session_state.selected_concept = response
    
    st.markdown("---")
    
    # Task 2: Feature Prioritization
    st.subheader("2. Feature Prioritization using MoSCoW Method")
    
    if st.button("Brainstorm & Prioritize Features", key="feature_prioritization"):
        if not st.session_state.selected_concept:
            st.warning("Please generate or select a product concept first!")
        else:
            with st.spinner("Analyzing features using Chain of Thought..."):
                context_prompt = f"""
                Based on this product concept:
                {st.session_state.selected_concept}
                
                Using Chain of Thought prompting, brainstorm 5 additional features for this product.
                Then prioritize ALL features (including the 3 core ones from the concept) using MoSCoW method:
                - Must-have: Critical for MVP
                - Should-have: Important but not critical
                - Could-have: Nice to have
                - Won't-have: Out of scope for now
                
                Think step by step:
                1. First, extract the 3 core features from the product concept
                2. Brainstorm 5 additional features that complement the concept
                3. List all 8 features (3 core + 5 additional)
                4. Apply MoSCoW prioritization with reasoning
                5. Output as a table with columns: Feature | Priority | Reasoning
                """
                
                messages = [
                    {"role": "system", "content": PRODUCT_MANAGER_SYSTEM_PROMPT},
                    {"role": "user", "content": context_prompt}
                ]
                
                response = ai_client.get_completion(messages, max_completion_tokens=1200)
                if response:
                    st.success("Feature Prioritization Complete!")
                    st.markdown(response)
    
    st.markdown("---")
    
    # Task 3: Roadmap Creation
    st.subheader("3. 4-Quarter Roadmap Creation")
    
    if st.button("Create Product Roadmap", key="roadmap_creation"):
        if not st.session_state.selected_concept:
            st.warning("Please generate or select a product concept first!")
        else:
            with st.spinner("Creating roadmap with milestones..."):
                roadmap_prompt = f"""
                Based on this product concept:
                {st.session_state.selected_concept}
                
                Create a 4-quarter roadmap for this product.
                
                Format as a table:
                | Q1 2025 | Q2 2025 | Q3 2025 | Q4 2025 |
                |---------|---------|---------|---------|
                | [Feature A] | [Feature B] | [Feature C] | [Feature D] |
                
                Include:
                - Key features to be delivered each quarter based on the product concept
                - Major milestones aligned with the product's core features
                - Dependencies between quarters
                - Risk mitigation strategies specific to this product
                """
                
                messages = [
                    {"role": "system", "content": PRODUCT_MANAGER_SYSTEM_PROMPT},
                    {"role": "user", "content": roadmap_prompt}
                ]
                
                response = ai_client.get_completion(messages, max_completion_tokens=1000)
                if response:
                    st.success("Roadmap Created!")
                    st.markdown(response)
    
    st.markdown("---")
    
    # Task 4: User Story Creation
    st.subheader("4. GitLab-style User Story")
    
    feature_input = st.text_input("Enter a feature to create user story for:", 
                                  placeholder="e.g., Real-time transaction monitoring")
    
    if st.button("Generate User Story", key="user_story") and feature_input:
        if not st.session_state.selected_concept:
            st.warning("Please generate or select a product concept first!")
        else:
            with st.spinner("Creating user story..."):
                user_story_prompt = f"""
                Based on this product concept:
                {st.session_state.selected_concept}
                
                Write a GitLab-style user story for the feature: "{feature_input}"
                
                Ensure the user story aligns with the product concept's target audience and use cases.
                
                Format:
                **User Story:**
                As a [user type], I want [action] so that [benefit].
                
                **Acceptance Criteria:**
                - [Detailed list of acceptance criteria]
                - [Include both functional and non-functional requirements]
                
                **Definition of Done:**
                - [List of completion criteria]
                """
                
                messages = [
                    {"role": "system", "content": PRODUCT_MANAGER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_story_prompt}
                ]
                
                response = ai_client.get_completion(messages, max_completion_tokens=1100)
                if response:
                    st.success("User Story Generated!")
                    st.markdown(response)
    
    # Display example data structure
    with st.expander("📊 View Sample Data Structures"):
        st.markdown("### Sample Hosts Data")
        st.code('''
{
  "hosts": [
    {
      "gpn": "43746091",
      "name": "MUHAMMAD AZLAN BIN HASSAN"
    },
    {
      "gpn": "43746115", 
      "name": "CHEW SHI DA, ERIC"
    }
  ]
}''', language="json")
        
        st.markdown("### Sample Events Data")
        st.code('''
{
  "events": [
    {
      "id": 1,
      "eventDate": "11/07/22",
      "status": 2,
      "rsvpBy": "01/07/22", 
      "eventTitle": "TFIP Lunch",
      "eventHost": "Xinying Tan",
      "eventLocation": "9 Penang Road, Cafeteria",
      "pax": "5"
    }
  ]
}''', language="json")
