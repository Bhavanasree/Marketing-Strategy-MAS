from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

_llm = ChatBedrock(model="global.anthropic.claude-haiku-4-5-20251001-v1:0")

@tool
def generate_seo_keywords(business_name: str) -> str:
    """Generate SEO keywords, meta descriptions, and content topic ideas for a business.
    Use this tool when the user asks for SEO help, keyword research, search engine
    optimization, meta tags, or content strategy for organic search."""

    response =  _llm.invoke([
        HumanMessage(content=(
            f"Generate SEO content for the business below.\n\n"

            f"1. PRIMARY KEYWORDS (10 high-intent keywords)\n"
            f"2. LONG-TAIL KEYWORDS (10 specific search phrases)\n"
            f"3. LOCAL SEO KEYWORDS (5 location-based variations if applicable)\n\n"

            f"4. META TITLE (max 60 characters)\n"
            f"5. META DESCRIPTION (max 155 characters, compelling and click-worthy)\n\n"

            f"6. CONTENT IDEAS (5 blog/article topics optimized for SEO)\n\n"

            f"Guidelines:\n"
            f"- Focus on search intent (informational + transactional)\n"
            f"- Use clear, relevant, and realistic keywords\n"
            f"- Avoid generic terms\n"
            f"- Make meta description engaging with a call-to-action\n\n"

            f"Business Name: {business_name}\n"
            f"Generate Seo Keywords:"
        ))
    ])
    return response.content