from browser_use import Agent, ChatGoogle
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import os
import json

load_dotenv()


def format_duration(seconds):
    """Format duration in a human-readable way"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def create_table_of_contents(sections):
    """Generate a beautiful table of contents"""
    toc = "## 📚 Table of Contents\n\n"
    for section in sections:
        toc += f"- [{section['emoji']} {section['title']}](#{section['anchor']})\n"
    return toc + "\n"


def format_metadata_table(task, history, timestamp):
    """Create a beautiful metadata table"""
    status_emoji = "✅" if history.is_done() else "❌"
    success_emoji = "🎯" if history.is_successful() else "⚠️"
    
    table = "| Attribute | Value |\n"
    table += "|-----------|-------|\n"
    table += f"| 📅 **Generated** | {datetime.now().strftime('%B %d, %Y at %I:%M %p')} |\n"
    table += f"| 🎯 **Task** | {task} |\n"
    table += f"| {status_emoji} **Status** | {'Completed Successfully' if history.is_done() else 'Incomplete'} |\n"
    table += f"| {success_emoji} **Success** | {'Yes' if history.is_successful() else 'No' if history.is_successful() is False else 'Unknown'} |\n"
    table += f"| ⏱️ **Duration** | {format_duration(history.total_duration_seconds())} |\n"
    table += f"| 🔢 **Steps** | {history.number_of_steps()} |\n"
    table += f"| 🌐 **URLs Visited** | {len(history.urls())} |\n"
    table += f"| ⚡ **Actions** | {len(history.action_names())} |\n"
    table += f"| 🚨 **Errors** | {len([e for e in history.errors() if e is not None])} |\n"
    
    return table + "\n"


async def main():
    llm = ChatGoogle(model="gemini-flash-latest")
    task = "summarize latest 3 hackernews articles"
    agent = Agent(task=task, llm=llm)
    
    print("🚀 Starting Hacker News analysis...")
    start_time = datetime.now()
    
    # Run the agent and capture the history
    history = await agent.run()
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/hn_analysis_{timestamp}.md"
    
    # Define sections for TOC
    sections = [
        {"title": "Executive Summary", "emoji": "📋", "anchor": "executive-summary"},
        {"title": "Analysis Results", "emoji": "🎯", "anchor": "analysis-results"},
        {"title": "Browsing Journey", "emoji": "🗺️", "anchor": "browsing-journey"},
        {"title": "Actions Timeline", "emoji": "⚡", "anchor": "actions-timeline"},
        {"title": "Content Discovery", "emoji": "📄", "anchor": "content-discovery"},
        {"title": "Agent Intelligence", "emoji": "🧠", "anchor": "agent-intelligence"},
        {"title": "Technical Details", "emoji": "🔧", "anchor": "technical-details"}
    ]
    
    # Save comprehensive analysis to markdown file
    with open(filename, "w", encoding="utf-8") as f:
        # Beautiful Header with ASCII art
        f.write("```\n")
        f.write("██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗     ███╗   ██╗███████╗██╗    ██╗███████╗\n")
        f.write("██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗    ████╗  ██║██╔════╝██║    ██║██╔════╝\n")
        f.write("███████║███████║██║     █████╔╝ █████╗  ██████╔╝    ██╔██╗ ██║█████╗  ██║ █╗ ██║███████╗\n")
        f.write("██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗    ██║╚██╗██║██╔══╝  ██║███╗██║╚════██║\n")
        f.write("██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║    ██║ ╚████║███████╗╚███╔███╔╝███████║\n")
        f.write("╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝ ╚══════╝\n")
        f.write("```\n\n")
        
        f.write("# 🔥 Hacker News AI Analysis Report\n\n")
        f.write("> *Powered by Google Gemini Flash & Browser Automation*\n\n")
        
        # Table of Contents
        f.write(create_table_of_contents(sections))
        
        # Metadata Table
        f.write("## 📊 Report Overview\n\n")
        f.write(format_metadata_table(task, history, timestamp))
        
        # Executive Summary
        f.write("## 📋 Executive Summary {#executive-summary}\n\n")
        final_result = history.final_result()
        if final_result:
            f.write(f"> **Key Findings:** {final_result}\n\n")
        else:
            f.write("> ⚠️ **No final result available** - The analysis may have been interrupted or incomplete.\n\n")
        
        # Analysis Results (Main Content)
        f.write("## 🎯 Analysis Results {#analysis-results}\n\n")
        if final_result:
            # Try to format the result nicely
            lines = str(final_result).split('\n')
            for line in lines:
                if line.strip():
                    if line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                        f.write(f"### {line}\n\n")
                    else:
                        f.write(f"{line}\n\n")
        else:
            f.write("*Analysis results not available.*\n\n")
        
        # Browsing Journey
        urls = history.urls()
        if urls:
            f.write("## 🗺️ Browsing Journey {#browsing-journey}\n\n")
            f.write("The AI agent visited the following websites during its analysis:\n\n")
            for i, url in enumerate(urls, 1):
                f.write(f"**{i}.** [{url}]({url})\n")
            f.write("\n")
        
        # Actions Timeline
        actions = history.action_names()
        if actions:
            f.write("## ⚡ Actions Timeline {#actions-timeline}\n\n")
            f.write("| Step | Action | Description |\n")
            f.write("|------|--------|-------------|\n")
            for i, action in enumerate(actions, 1):
                f.write(f"| {i} | `{action}` | Automated browser action |\n")
            f.write("\n")
        
        # Content Discovery
        content = history.extracted_content()
        if content and any(item for item in content if item):
            f.write("## 📄 Content Discovery {#content-discovery}\n\n")
            f.write("Raw content extracted during the browsing session:\n\n")
            for i, item in enumerate(content, 1):
                if item and str(item).strip():
                    f.write(f"### 📝 Extract {i}\n\n")
                    f.write("```text\n")
                    f.write(str(item)[:1000])  # Limit to first 1000 chars
                    if len(str(item)) > 1000:
                        f.write("\n... [truncated for readability]")
                    f.write("\n```\n\n")
        
        # Agent Intelligence (Reasoning)
        thoughts = history.model_thoughts()
        if thoughts:
            f.write("## 🧠 Agent Intelligence {#agent-intelligence}\n\n")
            f.write("The AI's reasoning process and decision-making:\n\n")
            for i, thought in enumerate(thoughts, 1):
                f.write(f"### 💭 Thought Process {i}\n\n")
                f.write("```markdown\n")
                f.write(str(thought)[:800])  # Limit reasoning length
                if len(str(thought)) > 800:
                    f.write("\n... [truncated]")
                f.write("\n```\n\n")
        
        # Technical Details
        f.write("## 🔧 Technical Details {#technical-details}\n\n")
        
        # Errors section
        errors = history.errors()
        error_count = len([e for e in errors if e is not None])
        if error_count > 0:
            f.write("### 🚨 Errors Encountered\n\n")
            f.write(f"**Total Errors:** {error_count}\n\n")
            for i, error in enumerate(errors, 1):
                if error:
                    f.write(f"**Error {i}:**\n```\n{error}\n```\n\n")
        else:
            f.write("### ✅ Error Status\n\n")
            f.write("🎉 **No errors encountered!** The analysis completed successfully.\n\n")
        
        # Performance metrics
        f.write("### 📈 Performance Metrics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Total Execution Time | {format_duration(history.total_duration_seconds())} |\n")
        f.write(f"| Average Time per Step | {format_duration(history.total_duration_seconds() / max(history.number_of_steps(), 1))} |\n")
        f.write(f"| Success Rate | {('100%' if history.is_successful() else '0%' if history.is_successful() is False else 'Unknown')} |\n")
        f.write(f"| Content Extraction Rate | {len([c for c in content if c]) if content else 0}/{len(content) if content else 0} |\n\n")
        
        # Footer
        f.write("---\n\n")
        f.write("*Report generated by Gemini Computer Use Agent*  \n")
        f.write(f"*Timestamp: {datetime.now().isoformat()}*  \n")
        f.write("*🤖 Powered by AI automation*\n")
    
    # Beautiful console output
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "="*60)
    print("🎉 ANALYSIS COMPLETE!")
    print("="*60)
    print(f"📁 Report saved: {filename}")
    print(f"⏱️  Total time: {format_duration(duration)}")
    print(f"📊 Agent steps: {history.number_of_steps()}")
    print(f"🌐 URLs visited: {len(history.urls())}")
    print(f"✅ Status: {'Success' if history.is_successful() else 'Completed with issues'}")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())