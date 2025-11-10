#!/usr/bin/env python3
"""
Autonomous Builder for First Contact E.I.S.
Uses Anthropic API to build remaining components autonomously
"""

import os
import anthropic
import json
from pathlib import Path

class AutonomousBuilder:
    def __init__(self, api_key: str, project_root: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.project_root = Path(project_root)
        self.conversation_history = []
        
    def read_project_context(self):
        """Read all documentation to understand the project"""
        docs_dir = self.project_root / "docs"
        context = []
        
        # Read key architecture documents
        key_docs = [
            "SYSTEM_ARCHITECTURE.md",
            "ARCHITECTURE_BLUEPRINT.md", 
            "PROJECT_VISION_AND_ARCHITECTURE.md",
            "SESSION_NOTES_NOV7.md"
        ]
        
        for doc in key_docs:
            doc_path = docs_dir / doc
            if doc_path.exists():
                with open(doc_path, 'r', encoding='utf-8') as f:
                    context.append(f"=== {doc} ===\n{f.read()}\n")
        
        return "\n".join(context)
    
    def read_codebase_structure(self):
        """Get overview of existing code structure"""
        structure = []
        
        # Backend structure
        backend = self.project_root / "backend" / "app"
        if backend.exists():
            structure.append("Backend structure:")
            for item in backend.rglob("*.py"):
                rel_path = item.relative_to(self.project_root)
                structure.append(f"  - {rel_path}")
        
        # Frontend structure  
        frontend = self.project_root / "frontend" / "caseworker" / "src"
        if frontend.exists():
            structure.append("\nFrontend structure:")
            for item in frontend.rglob("*.tsx"):
                rel_path = item.relative_to(self.project_root)
                structure.append(f"  - {rel_path}")
                
        return "\n".join(structure)
    
    def build_component(self, component_name: str, requirements: str):
        """Use Claude to build a specific component"""
        
        # Build comprehensive prompt
        context = self.read_project_context()
        structure = self.read_codebase_structure()
        
        prompt = f"""You are the CTO building First Contact E.I.S. - The Brain for Human Services.

PROJECT CONTEXT:
{context}

CURRENT CODEBASE STRUCTURE:
{structure}

YOUR TASK: Build {component_name}

REQUIREMENTS:
{requirements}

CRITICAL RULES:
1. Follow the architecture defined in the documentation
2. Use demo_mode=True for external APIs (we're building for Nov 15 demo)
3. Match existing code style and patterns
4. Provide complete, production-ready code
5. Include detailed comments explaining logic
6. Return code as complete files with file paths

OUTPUT FORMAT:
For each file, use this format:
```filepath
FILE_PATH_HERE
```
```code
COMPLETE_CODE_HERE
```

Start building now."""

        # Call Claude API
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    def parse_and_write_files(self, response: str):
        """Parse Claude's response and write files to disk"""
        lines = response.split('\n')
        current_filepath = None
        current_code = []
        in_code_block = False
        files_created = []
        
        for line in lines:
            if line.startswith('```filepath'):
                # Next line will be the file path
                continue
            elif line.startswith('```code'):
                in_code_block = True
                continue
            elif line.startswith('```') and in_code_block:
                # End of code block - write the file
                if current_filepath and current_code:
                    file_path = self.project_root / current_filepath.strip()
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(current_code))
                    
                    files_created.append(str(file_path))
                    print(f"✅ Created: {file_path}")
                
                # Reset
                current_filepath = None
                current_code = []
                in_code_block = False
            elif not in_code_block and current_filepath is None:
                # Look for file path
                if line.strip() and not line.startswith('#'):
                    current_filepath = line.strip()
            elif in_code_block:
                current_code.append(line)
        
        return files_created
    
    def build_all(self):
        """Build all remaining components"""
        
        components = [
            {
                "name": "Seed Data Script",
                "requirements": """
Create backend/scripts/seed_demo_data.py that:
1. Seeds PostgreSQL with demo data:
   - Client A (Maria): maria_demo_001
     * Scheduled doctor appointment: Tomorrow 2pm
     * Status: active
     * Documents: uploaded yesterday
   - Client B (Robert): robert_demo_001  
     * Scheduled doctor appointment: Next week 2pm
     * Urgency score: 8/10 (diabetes)
     * Documents: all uploaded, verified
     * Lives on transport route
   - Provider: Dr. Smith (provider_001)
     * Available slots
     * 2pm opening tomorrow
2. Creates mock transport routes
3. Provides function to trigger demo cancellation scenario
"""
            },
            {
                "name": "Frontend Recommendations Feed",
                "requirements": """
Create frontend/caseworker/src/components/RecommendationsFeed.tsx that:
1. Polls GET /api/v1/orchestration/recommendations every 5 seconds
2. Displays recommendations with:
   - Summary (e.g., "Bump Client B to today's 2pm?")
   - Reasoning bullets (urgency, docs ready, transport OK)
   - Impact metrics (cost savings, confidence %)
   - APPROVE button (calls approve endpoint)
   - REJECT button
3. Shows execution status (pending → executing → completed)
4. Uses Tailwind CSS for enterprise styling
5. Includes "Trigger Demo Event" button for testing
"""
            },
            {
                "name": "API Integration Hook",
                "requirements": """
Create frontend/caseworker/src/hooks/useOrchestration.ts that:
1. useRecommendations() - polls recommendations endpoint
2. useApproveRecommendation() - calls approve with mutation
3. useTriggerDemoEvent() - triggers demo scenario
4. Uses React Query for caching and auto-refetch
5. Handles loading/error states
"""
            },
            {
                "name": "Wire Orchestration to Main",
                "requirements": """
Update backend/app/main.py to:
1. Import orchestration router
2. Include router with prefix /api/v1/orchestration
3. Initialize orchestration services on startup
4. Add health check that verifies orchestration is ready
"""
            },
            {
                "name": "Demo Trigger Endpoint",
                "requirements": """
Update backend/app/routes/orchestration.py to ensure:
1. POST /trigger-event endpoint works
2. Stores recommendations in-memory dict (for demo)
3. GET /recommendations endpoint returns stored recommendations
4. POST /recommendations/{id}/approve triggers executor
5. All endpoints have proper error handling
"""
            }
        ]
        
        print("🚀 Starting autonomous build...")
        print(f"📁 Project root: {self.project_root}")
        print(f"🎯 Components to build: {len(components)}\n")
        
        all_files_created = []
        
        for i, component in enumerate(components, 1):
            print(f"\n{'='*60}")
            print(f"Building {i}/{len(components)}: {component['name']}")
            print(f"{'='*60}")
            
            response = self.build_component(
                component['name'],
                component['requirements']
            )
            
            files = self.parse_and_write_files(response)
            all_files_created.extend(files)
            
            print(f"\n✅ {component['name']} complete!")
            print(f"   Created {len(files)} file(s)")
        
        print(f"\n{'='*60}")
        print(f"🎉 BUILD COMPLETE!")
        print(f"{'='*60}")
        print(f"\nTotal files created: {len(all_files_created)}")
        print("\nFiles:")
        for f in all_files_created:
            print(f"  - {f}")
        
        return all_files_created


def main():
    """Main execution"""
    import sys
    
    # Get API key from environment or argument
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key and len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    if not api_key:
        print("❌ ERROR: No API key provided")
        print("\nUsage:")
        print("  python autonomous_builder.py YOUR_API_KEY")
        print("  OR")
        print("  set ANTHROPIC_API_KEY=your_key && python autonomous_builder.py")
        sys.exit(1)
    
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Build
    builder = AutonomousBuilder(api_key, project_root)
    builder.build_all()
    
    print("\n✅ All components built successfully!")
    print("\n🎯 Next steps:")
    print("1. Review the generated files")
    print("2. Test the demo flow: python scripts/test_demo.py")
    print("3. Commit to git: git add . && git commit -m 'feat: Complete demo build'")


if __name__ == "__main__":
    main()
