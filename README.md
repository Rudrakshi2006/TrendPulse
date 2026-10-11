# TrendPulse: AI Campus Placement Intelligence CLI

## Description
TrendPulse is a zero-database, terminal-based placement preparation tool for university students. 
It leverages the Tavily API for live web research and the Groq API for generating a structured, AI-driven preparation plan based on the user's target company, tech stack, current skill level, and available preparation time.

## Features
- **Live Intelligence:** Fetches the most recent interview questions, trends, and assessment topics using Tavily.
- **AI-Powered Analysis:** Uses Groq to parse web results and generate structured JSON insights.
- **Custom Sprint Plans:** Generates day-by-day 7, 15, or 30-day preparation plans tailored to the user.
- **Terminal UI:** Beautiful, interactive terminal interface using `rich`.
- **Markdown Reports:** Automatically saves generated reports in the `outputs/` folder.
- **Zero-Database & Local:** Runs completely in the terminal without complex backends or databases.

## Architecture Flow
1. **User Input:** Captures target, tech stack, level, and duration.
2. **Research Phase:** Generates multiple optimized search queries and fetches live data via Tavily.
3. **Analysis Phase:** Sends combined intelligence and user inputs to Groq for structured JSON generation.
4. **Validation Phase:** Uses Pydantic to strictly validate the AI output.
5. **Display & Save Phase:** Presents the report in the terminal and saves it as Markdown.

## Folder Structure
```text
trendpulse/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── services/
│   │   ├── tavily_service.py
│   │   └── groq_service.py
│   ├── prompts/
│   │   └── placement_prompt.py
│   ├── models/
│   │   └── analysis_models.py
│   └── utils/
│       ├── terminal_ui.py
│       └── validators.py
├── outputs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Rudrakshi2006/TrendPluse.git
cd trendpulse
```

### 2. Create and activate virtual environment
For macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```
For Windows:
```bash
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. API Key Configuration
Create a `.env` file in the root directory (you can copy from `.env.example`) and add your API keys:
```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama3-70b-8192  # Or any supported groq model
TAVILY_MAX_RESULTS=5
REQUEST_TIMEOUT=30
```

### 5. Run the Application
```bash
python -m app.main
```

## Example Input
```text
Target: Deloitte
Tech stack: Python, SQL, DBMS and aptitude
Level: Intermediate
Duration: 15 days
```

## Example Output Sections
- **Target Summary:** An overview of the company/role and general hiring patterns.
- **Live Intel:** High/Medium/Low priority trends and skills.
- **Recently Reported Questions:** Real questions categorised by difficulty.
- **Preparation Sprint:** Daily actionable plan (Focus, Learn, Practice, Deliverable).
- **Final Strategy:** Concluding tips to ace the placement.
- **Sources:** References used to generate the report.

## Limitations
- Quality of insights depends on search engine results from Tavily and Groq's interpretation.
- Groq models may occasionally return improperly formatted JSON (handled with retry mechanism).
- API rate limits apply based on your Groq and Tavily accounts.

## Disclaimer
The report is generated from publicly available web results. Interview processes and questions may change. Reported questions should be treated as preparation indicators, not guaranteed assessment content.
