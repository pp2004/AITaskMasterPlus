import streamlit as st

def render_ai_challenges():
    st.title("🤖 Week 4 - AI Challenges")
    st.markdown("Complete the following AI challenges using Azure OpenAI")
    
    # Challenge navigation
    challenge_tabs = st.tabs([
        "🎯 Challenge 1: Product Ideation",
        "🔧 Challenge 2: Azure OpenAI Integration", 
        "📝 Challenge 3: Advanced Prompt Engineering",
        "🛡️ Challenge 4: RAG & Security"
    ])
    
    with challenge_tabs[0]:
        from challenges.challenge1 import render_challenge1
        render_challenge1()
    
    with challenge_tabs[1]:
        from challenges.challenge2 import render_challenge2
        render_challenge2()
    
    with challenge_tabs[2]:
        from challenges.challenge3 import render_challenge3
        render_challenge3()
    
    with challenge_tabs[3]:
        from challenges.challenge4 import render_challenge4
        render_challenge4()
