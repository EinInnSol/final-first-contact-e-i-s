"""
GCP-Native Build Script
Uses Vertex AI Claude 4.5 to generate all remaining components

Run this in Vertex AI Workbench or Cloud Shell
"""

from google.cloud import aiplatform
from pathlib import Path
import json

# Initialize Vertex AI
PROJECT_ID = "einharjer-valhalla"
REGION = "us-east5"
MODEL_ID = "claude-sonnet-4-5@20250929"

aiplatform.init(project=PROJECT_ID, location=REGION)

def generate_with_claude(prompt: str, max_tokens: int = 8000) -> str:
    """Generate code using Vertex AI Claude"""
    
    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/claude"
    )
    
    response = endpoint.predict(
        instances=[{
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }]
    )
    
    return response.predictions[0]

def read_project_context():
    """Read architecture docs for context"""
    docs_dir = Path("docs")
    context = []
    
    for doc in ["SYSTEM_ARCHITECTURE.md", "SESSION_NOTES_NOV7.md"]:
        doc_path = docs_dir / doc
        if doc_path.exists():
            with open(doc_path) as f:
                context.append(f.read())
    
    return "\n\n".join(context)

def build_all_components():
    """Build everything that's left"""
    
    context = read_project_context()
    
    components = [
        {
            "name": "Seed Data",
            "path": "backend/scripts/seed_demo_data.py",
            "prompt": f"""{context}

Create complete seed_demo_data.py script that:
1. Connects to Cloud SQL PostgreSQL
2. Seeds demo clients (Maria, Robert) with appointments
3. Creates provider data (Dr. Smith)
4. Includes function to trigger demo cancellation
5. Uses SQLAlchemy with existing models

Return ONLY executable Python code, no markdown."""
        },
        {
            "name": "Recommendations Feed",
            "path": "frontend/caseworker/src/components/RecommendationsFeed.tsx",
            "prompt": f"""{context}

Create RecommendationsFeed.tsx component:
1. Polls /api/v1/orchestration/recommendations every 5s
2. Displays recommendations with APPROVE/REJECT buttons
3. Shows execution status with real-time updates
4. Uses Tailwind CSS (enterprise theme)
5. Integrates with useOrchestration hook

Return ONLY executable TypeScript/React code."""
        },
        {
            "name": "Orchestration Hooks",
            "path": "frontend/caseworker/src/hooks/useOrchestration.ts",
            "prompt": f"""{context}

Create useOrchestration.ts with React Query hooks:
1. useRecommendations() - auto-polling
2. useApproveRecommendation() - mutation
3. useRejectRecommendation() - mutation
4. useTriggerDemoEvent() - demo trigger

Return ONLY executable TypeScript code."""
        },
        {
            "name": "Dashboard Integration",
            "path": "frontend/caseworker/src/app/page.tsx",
            "prompt": f"""{context}

Update caseworker dashboard page.tsx to:
1. Import and use RecommendationsFeed component
2. Add "AI Recommendations" tab
3. Include demo trigger button
4. Maintain existing layout

Return ONLY executable TypeScript/React code."""
        },
        {
            "name": "API Wiring",
            "path": "backend/app/main.py",
            "prompt": f"""{context}

Update main.py to:
1. Import orchestration router
2. Include router at /api/v1/orchestration
3. Initialize orchestration services on startup
4. Add health check for orchestration status

Return ONLY executable Python code."""
        }
    ]
    
    print("🚀 Starting GCP-native build with Vertex AI Claude...\n")
    
    for i, component in enumerate(components, 1):
        print(f"Building {i}/{len(components)}: {component['name']}")
        
        # Generate code
        code = generate_with_claude(component['prompt'])
        
        # Write to file
        file_path = Path(component['path'])
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(code)
        
        print(f"✅ Created: {file_path}\n")
    
    print("🎉 All components built!")
    print("\n📋 Next steps:")
    print("1. Review generated files")
    print("2. Test: npm run dev (frontend) & uvicorn main:app (backend)")
    print("3. Run seed data: python backend/scripts/seed_demo_data.py")
    print("4. Commit: git add . && git commit -m 'feat: Complete build'")

if __name__ == "__main__":
    build_all_components()
