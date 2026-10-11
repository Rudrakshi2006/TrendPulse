from app.models.analysis_models import UserInput, SearchResult
from typing import List

def generate_placement_prompt(user_input: UserInput, search_results: List[SearchResult]) -> str:
    """Generate the main prompt for Groq to analyze the placement data with the updated schema."""
    
    # Format the search results to be easily readable by the LLM
    search_context = ""
    for idx, res in enumerate(search_results, 1):
        search_context += f"Result {idx}:\n"
        search_context += f"Title: {res.title}\n"
        search_context += f"URL: {res.url}\n"
        search_context += f"Content: {res.content}\n"
        if res.published_date:
            search_context += f"Published: {res.published_date}\n"
        search_context += "-" * 40 + "\n"

    # Determine sprint steps format
    duration = user_input.duration
    if duration in [7, 15, 30]:
        unit = "Day"
        num_steps = duration
    else:
        unit = "Week"
        num_steps = duration // 7

    prompt = f"""
You are an expert AI campus placement advisor. Analyze the web research provided and generate a comprehensive placement preparation report.

USER PROFILE:
- Target Company: {user_input.company}
- Target Role: {user_input.role}
- Tech Stack Provided: {user_input.tech_stack}
- Current Skill Level: {user_input.level}
- Preparation Duration: {user_input.duration} days

WEB RESEARCH RESULTS (Live Intel):
{search_context}

INSTRUCTIONS:
1. **Target Summary:** Synthesize the research to write a summary of the hiring processes, typical interview formats, and expectations for the role at this company.
2. **Confidence Note:** Include a disclaimer indicating whether the analysis is highly company-specific or based on broader role/domain trends.
3. **Feasibility Assessment:** Write a realistic, constructive evaluation of whether the selected preparation duration ({user_input.duration} days) is realistic given the candidate's current skill level ({user_input.level}) and target. Do not say "impossible" bluntly, but explain the level of difficulty (e.g., extremely tough vs. highly feasible) and what extra focus is required to make it.
4. **Tech Stack Gaps:** Critically analyze the user's provided tech stack against what is typically expected for this role at the target company. For example, if they provided Python for a Java-centric role, or missed foundational topics like SQL, DSA, System Design, Git, or Docker. Identify exactly what is missing or what else they should consider. Be precise.
5. **Interview Questions:** Extract or construct 5 to 10 highly relevant recently reported or common questions for this specific combination of company, role, and stack.
6. **Sprint Plan:**
   - You MUST generate exactly {num_steps} entries in the `sprint_plan` list.
   - For this duration ({user_input.duration} days), the `unit` for each step must be "{unit}" (e.g. step 1, 2, ... {num_steps}).
   - Each step must have a clear Focus, Learn (array), Practice (array), and Deliverable (string).
7. Return your response strictly as a JSON object matching the schema below. DO NOT wrap it in markdown code blocks. DO NOT output any conversational text.

REQUIRED JSON SCHEMA:
{{
  "target_summary": "string",
  "confidence_note": "string",
  "feasibility_assessment": "string",
  "tech_stack_gaps": [
    "string"
  ],
  "live_intel": [
    {{
      "title": "string",
      "description": "string",
      "importance": "High | Medium | Low",
      "source_urls": ["string"]
    }}
  ],
  "recent_questions": [
    {{
      "question": "string",
      "category": "Coding | Technical | Aptitude | HR | System Design | Other",
      "difficulty": "Easy | Medium | Hard",
      "answer_approach": "string",
      "source_urls": ["string"]
    }}
  ],
  "sprint_plan": [
    {{
      "number": 1,
      "unit": "{unit}",
      "focus": "string",
      "learn": ["string"],
      "practice": ["string"],
      "deliverable": "string"
    }}
  ],
  "final_strategy": [
    "string"
  ],
  "sources": [
    {{
      "title": "string",
      "url": "string",
      "published_date": "string"
    }}
  ]
}}
"""
    return prompt
