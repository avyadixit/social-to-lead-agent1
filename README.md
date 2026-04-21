# Social-to-Lead Agentic Workflow

##  Overview
This project implements a conversational AI agent for a fictional SaaS product **AutoStream** (an automated video editing tool).

The agent is designed to:
- Answer product-related queries
- Detect high-intent users
- Capture leads through a structured multi-step workflow

---

##  Features
-  Intent Detection (Greeting, Product Inquiry, High-Intent Lead)
-  Local Knowledge Base (RAG-style responses)
-  Stateful Conversation Memory
-  Multi-step Lead Capture (Name → Email → Platform)
-  Email Validation using Regex
-  Tool Execution after complete data collection
-  LangGraph-based Agentic Workflow

---

##  Tech Stack
- Python 3.10+
- LangChain
- LangGraph

---

##  Knowledge Base
The chatbot uses a local file (`knowledge_base.md`) containing:

- **Basic Plan**: $29/month, 10 videos/month, 720p  
- **Pro Plan**: $79/month, unlimited videos, 4K, AI captions  
- **Refund Policy**: No refunds after 7 days  
- **Support**: 24/7 support only for Pro users  

---

##  How to Run

### 1. Clone the repository
```bash
git clone https://github.com/avyadixit/social-to-lead-agent1.git
cd social-to-lead-agent1
