from typing import TypedDict
import re

from langgraph.graph import StateGraph, END


# ---------------- STATE ---------------- #

class AgentState(TypedDict):
    user_input: str
    intent: str
    response: str

    name: str
    email: str
    platform: str

    collecting_lead: bool
    lead_capture_complete: bool
    current_lead_field: str


# ---------------- UTIL ---------------- #

def is_valid_email(email):
    pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return re.match(pattern, email) is not None


def mock_lead_capture(name, email, platform):
    print(f"\nLead captured successfully: {name}, {email}, {platform}\n")


# ---------------- NODES ---------------- #

def detect_intent_node(state: AgentState):
    text = state["user_input"].lower()

    if any(x in text for x in ["hi", "hello", "hey"]):
        state["intent"] = "greeting"

    elif any(x in text for x in ["buy", "sign up", "signup", "subscribe", "demo", "get started", "purchase"]):
        state["intent"] = "high_intent_lead"

    elif any(x in text for x in ["price", "pricing", "plan", "plans", "feature", "features", "refund", "support"]):
        state["intent"] = "product_inquiry"

    else:
        state["intent"] = "unknown"

    return state


def greeting_node(state: AgentState):
    state["response"] = "Hello! I am the AutoStream assistant. How can I help you today?"
    return state


def product_node(state: AgentState):
    text = state["user_input"].lower()

    if "basic" in text:
        state["response"] = "Basic Plan: $29/month, 10 videos/month, 720p."
    elif "pro" in text:
        state["response"] = "Pro Plan: $79/month, unlimited videos, 4K, AI captions."
    elif "price" in text or "pricing" in text or "plan" in text or "plans" in text:
        state["response"] = (
            "AutoStream has two plans:\n"
            "- Basic Plan: $29/month, 10 videos/month, 720p\n"
            "- Pro Plan: $79/month, unlimited videos, 4K, AI captions"
        )
    elif "refund" in text:
        state["response"] = "Policy: No refunds after 7 days of purchase."
    elif "support" in text:
        state["response"] = "24/7 support is available only for Pro Plan users."
    elif "feature" in text or "features" in text:
        state["response"] = (
            "Known features from the knowledge base:\n"
            "- Basic Plan: 10 videos/month, 720p\n"
            "- Pro Plan: unlimited videos, 4K, AI captions"
        )
    else:
        state["response"] = "I could not find that in the knowledge base."

    return state


def lead_node(state: AgentState):
    if state["lead_capture_complete"]:
        state["response"] = (
            "Your lead information has already been captured. "
            "I can still help with plans, pricing, support, or refund policy."
        )
        return state

    state["collecting_lead"] = True

    if not state["name"]:
        state["current_lead_field"] = "name"
        state["response"] = "May I have your name?"
        return state

    if not state["email"]:
        state["current_lead_field"] = "email"
        state["response"] = "Please share your email."
        return state

    if not state["platform"]:
        state["current_lead_field"] = "platform"
        state["response"] = "Which creator platform do you use?"
        return state

    state["response"] = "I already have your details."
    return state


def lead_collection_node(state: AgentState):
    text = state["user_input"].strip()

    if state["current_lead_field"] == "name":
        if not text:
            state["response"] = "Please enter your name."
            return state

        state["name"] = text
        state["current_lead_field"] = "email"
        state["response"] = "Thanks. Your email?"
        return state

    elif state["current_lead_field"] == "email":
        if not is_valid_email(text):
            state["response"] = "That does not look like a valid email address. Please enter a valid email."
            return state

        state["email"] = text
        state["current_lead_field"] = "platform"
        state["response"] = "Which creator platform do you use?"
        return state

    elif state["current_lead_field"] == "platform":
        if not text:
            state["response"] = "Please tell me which creator platform you use."
            return state

        state["platform"] = text

        mock_lead_capture(state["name"], state["email"], state["platform"])

        state["lead_capture_complete"] = True
        state["collecting_lead"] = False
        state["current_lead_field"] = None
        state["response"] = "Lead captured successfully!"
        return state

    state["response"] = "I was not expecting that input right now."
    return state


# ---------------- ROUTER ---------------- #

def router(state: AgentState):
    if state["collecting_lead"]:
        return "lead_collection"

    if state["intent"] == "greeting":
        return "greeting"

    if state["intent"] == "product_inquiry":
        return "product"

    if state["intent"] == "high_intent_lead":
        return "lead"

    return END


# ---------------- GRAPH ---------------- #

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("intent", detect_intent_node)
    graph.add_node("greeting", greeting_node)
    graph.add_node("product", product_node)
    graph.add_node("lead", lead_node)
    graph.add_node("lead_collection", lead_collection_node)

    graph.set_entry_point("intent")
    graph.add_conditional_edges("intent", router)

    graph.add_edge("greeting", END)
    graph.add_edge("product", END)
    graph.add_edge("lead", END)
    graph.add_edge("lead_collection", END)

    return graph.compile()


# ---------------- MAIN ---------------- #

def main():
    graph = build_graph()

    state = {
        "user_input": "",
        "intent": "",
        "response": "",
        "name": None,
        "email": None,
        "platform": None,
        "collecting_lead": False,
        "lead_capture_complete": False,
        "current_lead_field": None,
    }

    print("AutoStream LangGraph Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break

        if not user_input:
            print("Bot: Please enter a message.")
            continue

        state["user_input"] = user_input
        state = graph.invoke(state)

        print(f"Bot: {state['response']}")


if __name__ == "__main__":
    main()