from langchain.tools import tool
from app.rag.retriever import get_retriever

@tool
def get_price_estimate(make_model: str) -> str:
    """Returns price range for given car make/model using market data"""
    # Implement your pricing logic here
    return "₹5-7 lakhs (based on 2024 market data)"

@tool
def fetch_technical_specs(query: str) -> str:
    """Retrieves technical specifications from vehicle database"""
    retriever = get_retriever().as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    return "\n\n".join([d.page_content for d in docs])