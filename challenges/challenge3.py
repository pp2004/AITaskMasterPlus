import streamlit as st
import tiktoken
from utils.ai_client import AzureOpenAIClient
from utils.prompt_templates import ZERO_SHOT_EXAMPLE, FEW_SHOT_EXAMPLES, COT_PROMPT_TEMPLATE

def render_challenge3():
    st.header("📝 Challenge 3: Advanced Prompt Engineering")
    st.markdown("Master prompting techniques and token optimization")
    
    ai_client = AzureOpenAIClient()
    
    # Initialize tiktoken encoder
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
    except:
        st.warning("Tiktoken not available for token counting")
        encoding = None
    
    def count_tokens(text):
        if encoding:
            return len(encoding.encode(text))
        else:
            return len(text.split()) * 1.3  # Rough estimation
    
    # Exercise 1: Zero-Shot vs Few-Shot
    st.subheader("1. Zero-Shot vs Few-Shot Comparison")
    
    query_topic = st.text_input("Enter a topic to explain:", 
                               value="quantum computing",
                               key="zeroshot_topic")
    
    if st.button("🔬 Compare Zero-Shot vs Few-Shot", key="zero_few_shot"):
        if query_topic.strip():
            col1, col2 = st.columns(2)
            
            # Zero-Shot
            with col1:
                st.markdown("#### 🎯 Zero-Shot Approach")
                st.markdown("*Direct explanation without examples*")
                
                with st.spinner("Generating zero-shot response..."):
                    zero_shot_messages = [
                        {"role": "system", "content": "You are a helpful assistant that explains complex topics clearly."},
                        {"role": "user", "content": f"Explain {query_topic}"}
                    ]
                    
                    zero_shot_response = ai_client.get_completion(zero_shot_messages, max_completion_tokens=400)
                    
                    if zero_shot_response:
                        st.markdown("**Response:**")
                        st.markdown(zero_shot_response)
                        
                        # Token count
                        total_tokens = count_tokens(" ".join([msg["content"] for msg in zero_shot_messages]) + zero_shot_response)
                        st.markdown(f"**Estimated Tokens:** {total_tokens:.0f}")
            
            # Few-Shot
            with col2:
                st.markdown("#### 📚 Few-Shot Approach")
                st.markdown("*With examples for context*")
                
                with st.spinner("Generating few-shot response..."):
                    # Build few-shot prompt with examples
                    few_shot_content = "Here are some examples of clear explanations:\n\n"
                    for example in FEW_SHOT_EXAMPLES:
                        few_shot_content += f"**{example['concept']}:** {example['explanation']}\n\n"
                    few_shot_content += f"Now explain {query_topic} in a similar clear, accessible way:"
                    
                    few_shot_messages = [
                        {"role": "system", "content": "You are a helpful assistant that explains complex topics clearly using analogies and examples."},
                        {"role": "user", "content": few_shot_content}
                    ]
                    
                    few_shot_response = ai_client.get_completion(few_shot_messages, max_completion_tokens=400)
                    
                    if few_shot_response:
                        st.markdown("**Response:**")
                        st.markdown(few_shot_response)
                        
                        # Token count
                        total_tokens = count_tokens(" ".join([msg["content"] for msg in few_shot_messages]) + few_shot_response)
                        st.markdown(f"**Estimated Tokens:** {total_tokens:.0f}")
            
            # Analysis
            st.markdown("---")
            st.markdown("### 📊 Comparison Analysis")
            
            if zero_shot_response and few_shot_response:
                analysis_prompt = f"""
                Compare these two explanations of "{query_topic}":
                
                Zero-Shot Response:
                {zero_shot_response}
                
                Few-Shot Response: 
                {few_shot_response}
                
                Analyze:
                1. Clarity and accessibility
                2. Use of analogies/examples
                3. Depth of explanation
                4. Which approach worked better for this topic and why
                """
                
                with st.spinner("Analyzing approaches..."):
                    analysis_messages = [
                        {"role": "system", "content": "You are an expert in prompt engineering and educational content analysis."},
                        {"role": "user", "content": analysis_prompt}
                    ]
                    
                    analysis = ai_client.get_completion(analysis_messages, max_completion_tokens=500)
                    if analysis:
                        st.markdown(analysis)
    
    st.markdown("---")
    
    # Exercise 2: Chain-of-Thought (CoT)
    st.subheader("2. Chain-of-Thought (CoT) Prompting")
    
    # Math problem example
    st.markdown("**Example: Step-by-step reasoning**")
    math_problem = st.text_input("Enter a math word problem:", 
                                value="A store has 12 apples. They sold 5, then bought 8 more. How many apples do they have now?",
                                key="math_problem")
    
    if st.button("🧠 Apply Chain-of-Thought", key="cot_reasoning"):
        if math_problem.strip():
            with st.spinner("Thinking step by step..."):
                cot_prompt = COT_PROMPT_TEMPLATE.format(user_question=math_problem)
                
                messages = [
                    {"role": "system", "content": "You are a mathematics tutor who always shows step-by-step reasoning."},
                    {"role": "user", "content": cot_prompt}
                ]
                
                cot_response = ai_client.get_completion(messages, max_completion_tokens=500)
                
                if cot_response:
                    st.success("Step-by-Step Solution:")
                    st.markdown(cot_response)
    
    # Custom CoT example
    st.markdown("**Custom Chain-of-Thought Example:**")
    custom_problem = st.text_area("Enter a complex problem that requires reasoning:",
                                 placeholder="e.g., How would you design a secure authentication system for a banking app?",
                                 key="custom_cot")
    
    if st.button("🔗 Generate CoT Response", key="custom_cot_btn") and custom_problem.strip():
        with st.spinner("Breaking down the problem..."):
            cot_prompt = f"""
            Let's approach this step by step:
            
            1. First, I'll identify the key components of the problem
            2. Then, I'll consider the constraints and requirements
            3. Next, I'll evaluate different approaches
            4. Finally, I'll provide a structured solution with reasoning
            
            Problem: {custom_problem}
            """
            
            messages = [
                {"role": "system", "content": "You are an expert problem solver who uses systematic, step-by-step reasoning."},
                {"role": "user", "content": cot_prompt}
            ]
            
            response = ai_client.get_completion(messages, max_completion_tokens=600)
            if response:
                st.markdown("### 🎯 Chain-of-Thought Analysis:")
                st.markdown(response)
    
    st.markdown("---")
    
    # Exercise 3: Token Efficiency
    st.subheader("3. Token Efficiency Optimization")
    
    # Original vs Optimized comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Original Prompt")
        original_prompt = st.text_area(
            "Verbose prompt:",
            value="In light of recent developments in the field of artificial intelligence and considering the ever-evolving landscape of cybersecurity threats, could you please elucidate the various methodologies and best practices...",
            height=100,
            key="original_prompt"
        )
        
        if original_prompt:
            original_tokens = count_tokens(original_prompt)
            st.markdown(f"**Estimated Tokens:** {original_tokens:.0f}")
        else:
            original_tokens = 0
    
    with col2:
        st.markdown("#### ⚡ Optimized Prompt")
        optimized_prompt = st.text_area(
            "Concise prompt:",
            value="Explain recent AI security trends and best practices",
            height=100,
            key="optimized_prompt"
        )
        
        if optimized_prompt:
            optimized_tokens = count_tokens(optimized_prompt)
            st.markdown(f"**Estimated Tokens:** {optimized_tokens:.0f}")
            
            if original_prompt and original_tokens > 0:
                savings = ((original_tokens - optimized_tokens) / original_tokens) * 100
                st.success(f"**Token Savings:** {savings:.1f}%")
    
    if st.button("🔄 Compare Responses", key="compare_efficiency"):
        if original_prompt.strip() and optimized_prompt.strip():
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Response to Original")
                with st.spinner("Generating response to original prompt..."):
                    orig_messages = [
                        {"role": "user", "content": original_prompt}
                    ]
                    orig_response = ai_client.get_completion(orig_messages, max_completion_tokens=800)
                    if orig_response:
                        st.markdown(orig_response)
            
            with col2:
                st.markdown("#### Response to Optimized")
                with st.spinner("Generating response to optimized prompt..."):
                    opt_messages = [
                        {"role": "user", "content": optimized_prompt}
                    ]
                    opt_response = ai_client.get_completion(opt_messages, max_completion_tokens=800)
                    if opt_response:
                        st.markdown(opt_response)
    
    # Token optimization tips
    with st.expander("💡 Token Optimization Tips"):
        st.markdown("""
        ### Best Practices for Token Efficiency:
        
        1. **Remove unnecessary words**: "please", "could you", "I would like"
        2. **Use bullet points** instead of paragraphs for lists
        3. **Avoid repetition** of concepts
        4. **Use abbreviations** where appropriate
        5. **Be specific** rather than verbose
        6. **Remove filler words**: "very", "really", "quite"
        7. **Use active voice** instead of passive
        8. **Combine related requests** into single prompts
        
        ### Example Transformations:
        - ❌ "Could you please provide me with a detailed explanation of..."
        - ✅ "Explain..."
        
        - ❌ "I would really appreciate it if you could help me understand..."
        - ✅ "How does..."
        
        - ❌ "In consideration of the aforementioned factors..."
        - ✅ "Given these factors..."
        """)
