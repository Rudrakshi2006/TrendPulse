from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown
from app.models.analysis_models import PlacementReport

console = Console()

def display_welcome():
    welcome_text = "[bold cyan]TREND PULSE[/bold cyan]\n[italic]Live Placement Intelligence[/italic]"
    console.print(Panel(welcome_text, expand=False, border_style="cyan"))

def display_error(msg: str):
    console.print(Panel(f"[bold red]Error:[/bold red] {msg}", border_style="red"))

def prompt_user_input():
    company = Prompt.ask("[bold yellow]Target company or domain[/bold yellow]")
    role = Prompt.ask("[bold yellow]Target role[/bold yellow]")
    tech_stack = Prompt.ask("[bold yellow]Tech stack[/bold yellow]")
    
    # We remove show_default and show_choices to make the prompt as clean as possible
    level = Prompt.ask(
        "[bold yellow]Current level (beginner / intermediate / advanced)[/bold yellow]", 
        choices=["beginner", "intermediate", "advanced"],
        show_default=False,
        show_choices=False
    )
    
    duration = IntPrompt.ask(
        "[bold yellow]Preparation duration in days (7 / 15 / 30 / 45 / 60 / 90 / 120 / 150 / 180)[/bold yellow]", 
        choices=["7", "15", "30", "45", "60", "90", "120", "150", "180"],
        show_default=False,
        show_choices=False
    )
    
    return {
        "company": company,
        "role": role,
        "tech_stack": tech_stack,
        "level": level,
        "duration": int(duration)
    }

def display_report(report: PlacementReport):
    # Target Summary
    console.print(Panel(f"{report.target_summary}\n\n[italic gray]{report.confidence_note}[/italic gray]", title="Target Summary", border_style="blue"))
    
    # Feasibility Assessment
    console.print(Panel(report.feasibility_assessment, title="Feasibility Assessment", border_style="yellow"))
    
    # Tech Stack Gaps
    if report.tech_stack_gaps:
        gaps_content = "\n".join([f"- {gap}" for gap in report.tech_stack_gaps])
        console.print(Panel(gaps_content, title="Tech Stack Gaps & Recommendations", border_style="red"))
    
    # Live Intel
    intel_table = Table(title="Live Intel", show_header=True, header_style="bold magenta")
    intel_table.add_column("Importance", style="dim", width=10)
    intel_table.add_column("Title", style="bold")
    intel_table.add_column("Description")
    
    for item in report.live_intel:
        color = "red" if item.importance == "High" else "yellow" if item.importance == "Medium" else "green"
        intel_table.add_row(f"[{color}]{item.importance}[/{color}]", item.title, item.description)
    console.print(intel_table)
    
    # Recently Reported Questions
    q_table = Table(title="Recently Reported Questions", show_header=True, header_style="bold green")
    q_table.add_column("Category")
    q_table.add_column("Difficulty")
    q_table.add_column("Question")
    q_table.add_column("Approach")
    
    for q in report.recent_questions:
        diff_color = "red" if q.difficulty == "Hard" else "yellow" if q.difficulty == "Medium" else "green"
        q_table.add_row(q.category, f"[{diff_color}]{q.difficulty}[/{diff_color}]", q.question, q.answer_approach)
    console.print(q_table)
    
    # Preparation Sprint
    console.print("\n[bold cyan]Preparation Sprint[/bold cyan]")
    for step in report.sprint_plan:
        content = f"[bold]Focus:[/bold] {step.focus}\n"
        content += f"[bold]Learn:[/bold] {', '.join(step.learn)}\n"
        content += f"[bold]Practice:[/bold] {', '.join(step.practice)}\n"
        content += f"[bold]Deliverable:[/bold] {step.deliverable}"
        console.print(Panel(content, title=f"{step.unit} {step.number}", border_style="cyan"))
        
    # Final Strategy
    strategy_content = "\n".join([f"- {s}" for s in report.final_strategy])
    console.print(Panel(strategy_content, title="Final Strategy", border_style="yellow"))
    
    # Sources
    console.print("\n[bold]Sources:[/bold]")
    for s in report.sources:
        console.print(f"- [link={s.url}]{s.title}[/link] ({s.published_date or 'No date'})")
        
def save_report_to_markdown(report: PlacementReport, user_input: dict) -> str:
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_company = "".join(c if c.isalnum() else "_" for c in user_input['company']).lower()
    safe_role = "".join(c if c.isalnum() else "_" for c in user_input['role']).lower()
    filename = f"outputs/{safe_company}_{safe_role}_{user_input['duration']}_day_report.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# TrendPulse Report\n")
        f.write(f"Generated date: {date_str}\n\n")
        f.write(f"**Target Company:** {user_input['company']}\n")
        f.write(f"**Target Role:** {user_input['role']}\n")
        f.write(f"**Tech stack:** {user_input['tech_stack']}\n")
        f.write(f"**Level:** {user_input['level']}\n")
        f.write(f"**Duration:** {user_input['duration']} days\n\n")
        
        f.write("## Target Summary\n")
        f.write(f"{report.target_summary}\n\n")
        f.write(f"_{report.confidence_note}_\n\n")
        
        f.write("## Feasibility Assessment\n")
        f.write(f"{report.feasibility_assessment}\n\n")
        
        f.write("## Tech Stack Gaps & Recommendations\n")
        for gap in report.tech_stack_gaps:
            f.write(f"- {gap}\n")
        f.write("\n")
        
        f.write("## Live Intel\n")
        for item in report.live_intel:
            f.write(f"- **[{item.importance}] {item.title}:** {item.description}\n")
        f.write("\n")
        
        f.write("## Recently Reported Questions\n")
        for q in report.recent_questions:
            f.write(f"### {q.question}\n")
            f.write(f"- Category: {q.category}\n")
            f.write(f"- Difficulty: {q.difficulty}\n")
            f.write(f"- Approach: {q.answer_approach}\n\n")
            
        f.write("## Preparation Sprint\n")
        for step in report.sprint_plan:
            f.write(f"### {step.unit} {step.number}: {step.focus}\n")
            f.write(f"- **Learn:** {', '.join(step.learn)}\n")
            f.write(f"- **Practice:** {', '.join(step.practice)}\n")
            f.write(f"- **Deliverable:** {step.deliverable}\n\n")
            
        f.write("## Final Strategy\n")
        for s in report.final_strategy:
            f.write(f"- {s}\n")
        f.write("\n")
            
        f.write("## Sources\n")
        for s in report.sources:
            f.write(f"- [{s.title}]({s.url})\n")
        f.write("\n")
        
        f.write("## Disclaimer\n")
        f.write("The report is generated from publicly available web results. Interview processes and questions may change. Reported questions should be treated as preparation indicators, not guaranteed assessment content.\n")
        
    return filename
