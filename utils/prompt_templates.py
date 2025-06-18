CYBERSECURITY_SYSTEM_PROMPT = """You are a cybersecurity expert analyst with extensive knowledge in:
- Network security and infrastructure protection
- Threat detection and incident response
- Security frameworks and compliance
- Vulnerability assessment and penetration testing
- Cryptography and data protection
- Identity and access management

Provide detailed, technical explanations while being accessible to various skill levels. 
Include practical examples and real-world scenarios when relevant."""

PRODUCT_MANAGER_SYSTEM_PROMPT = """You are an experienced Product Manager with expertise in:
- Product strategy and roadmap development
- Feature prioritization using frameworks like MoSCoW
- User story creation and acceptance criteria
- Market analysis and competitive intelligence
- Agile methodologies and stakeholder management

Provide structured, actionable insights with clear reasoning and business justification."""

ZERO_SHOT_EXAMPLE = {
    "prompt": "Explain quantum computing",
    "context": "Direct explanation without examples"
}

FEW_SHOT_EXAMPLES = [
    {
        "concept": "Machine Learning",
        "explanation": "Machine learning is like teaching a computer to recognize patterns, similar to how you learn to recognize faces - the more examples you see, the better you become at identifying new ones."
    },
    {
        "concept": "Blockchain",
        "explanation": "Blockchain is like a digital ledger that's copied across many computers, where each page (block) is linked to the previous one, making it nearly impossible to change past entries without everyone noticing."
    }
]

COT_PROMPT_TEMPLATE = """
Let's think step by step:

1. First, let me understand what you're asking about
2. Then, I'll break down the key components
3. Next, I'll explain how these components work together
4. Finally, I'll provide practical implications

{user_question}
"""

SECURITY_VULNERABILITIES = {
    "Training Data Poisoning": {
        "description": "Malicious actors inject harmful data into training datasets",
        "mitigation": "Implement data validation pipelines, source verification, and anomaly detection"
    },
    "Model Extraction": {
        "description": "Attackers query models to reverse-engineer their functionality",
        "mitigation": "API rate limiting, query obfuscation, and differential privacy"
    },
    "Data Leakage": {
        "description": "Sensitive training data can be extracted from model outputs",
        "mitigation": "Output filtering using regex patterns, data anonymization, and access controls"
    },
    "Supply Chain Attacks": {
        "description": "Compromised dependencies or model artifacts introduce vulnerabilities",
        "mitigation": "Signed model artifacts, dependency scanning, and secure deployment pipelines"
    }
}
