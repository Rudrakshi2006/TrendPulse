import json
import logging
from typing import List, Dict, Any
from tavily import TavilyClient

from app.models.analysis_models import SearchResult, UserInput

class TavilyService:
    def __init__(self, api_key: str, max_results: int = 5):
        self.client = TavilyClient(api_key=api_key)
        self.max_results = max_results
        
    def _generate_queries(self, user_input: UserInput) -> List[str]:
        """Generate search queries based on user target company, role, and stack."""
        company = user_input.company
        role = user_input.role
        stack = user_input.tech_stack
        return [
            f"{company} {role} interview experience 2026",
            f"{company} campus placement technical questions 2026",
            f"{company} {role} coding assessment skills recent",
            f"{company} {role} {stack} interview questions",
            f"{company} campus recruitment process {role}"
        ]

    def perform_research(self, user_input: UserInput) -> List[SearchResult]:
        """Perform multiple searches and combine unique results."""
        queries = self._generate_queries(user_input)
        all_results = []
        seen_urls = set()

        for query in queries:
            try:
                response = self.client.search(
                    query=query, 
                    search_depth="basic",
                    max_results=self.max_results
                )
                
                for res in response.get("results", []):
                    url = res.get("url")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        all_results.append(
                            SearchResult(
                                title=res.get("title", "Unknown Title"),
                                url=url,
                                content=res.get("content", ""),
                                published_date=res.get("published_date", "")
                            )
                        )
            except Exception as e:
                logging.debug(f"Tavily search failed for query '{query}': {e}")
                pass
                
        return all_results
