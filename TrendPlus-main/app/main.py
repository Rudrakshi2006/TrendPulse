import sys
from rich.console import Console

from app.config import load_and_validate_env
from app.utils.terminal_ui import display_welcome, display_error, prompt_user_input, display_report, save_report_to_markdown
from app.utils.validators import validate_user_input
from app.services.tavily_service import TavilyService
from app.services.groq_service import GroqService

def main():
    console = Console()
    try:
        display_welcome()
        
        # Load environment
        config = load_and_validate_env()
        
        # Initialize services
        tavily_service = TavilyService(
            api_key=config['tavily_api_key'], 
            max_results=config['tavily_max_results']
        )
        groq_service = GroqService(
            api_key=config['groq_api_key'],
            model_name=config['groq_model']
        )
        
        # Get and validate user input
        raw_input = prompt_user_input()
        user_input = validate_user_input(raw_input)
        
        if not user_input:
            display_error("Invalid input provided. Please ensure all fields are properly filled.")
            sys.exit(1)
            
        # Research Phase
        with console.status("[bold cyan]Gathering live intelligence...", spinner="dots"):
            search_results = tavily_service.perform_research(user_input)
            
        if not search_results:
            display_error("No relevant search results found. Please try broadening your target or tech stack.")
            sys.exit(1)
            
        # Analysis Phase
        with console.status("[bold magenta]Analyzing trends and generating strategy...", spinner="dots"):
            try:
                report = groq_service.generate_report(user_input, search_results)
            except Exception as e:
                display_error(f"Failed to generate analysis: {e}")
                sys.exit(1)
                
        # Display Results
        display_report(report)
        
        # Save Report
        try:
            filename = save_report_to_markdown(report, raw_input)
            console.print(f"\n[bold green]Success![/bold green] Report saved to [cyan]{filename}[/cyan]")
        except Exception as e:
            display_error(f"Failed to save Markdown report: {e}")
            
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Process interrupted by user. Exiting...[/bold yellow]")
        sys.exit(0)
    except Exception as e:
        display_error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
