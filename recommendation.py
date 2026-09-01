import json
import re
import os

from dotenv import load_dotenv
from groq import Groq


# =========================
# LOAD ENVIRONMENT
# =========================

load_dotenv(dotenv_path=".env")


# =========================
# GROQ API KEY
# =========================

api_key = os.getenv("GROQ_API_KEY")

print("Groq API key loaded:", bool(api_key))


# =========================
# GROQ CLIENT
# =========================

client = Groq(
    api_key=api_key
)


# =========================
# CLEAN JSON RESPONSE
# =========================

def clean_json(text):

    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


# =========================
# AI PROJECT RECOMMENDATIONS
# =========================

def recommend_projects(user_preferences):

    prompt = f"""
You are an expert AI project recommendation system.

Generate exactly 6 unique and practical college project ideas.

Student preferences:

Domain: {user_preferences["domain"]}
Technology: {user_preferences["technology"]}
Experience: {user_preferences["experience"]}
Difficulty: {user_preferences["difficulty"]}
Interest: {user_preferences["interest"]}
Project Type: {user_preferences["type"]}

Rules:

1. Generate exactly 6 projects.
2. All projects must be different.
3. Match the selected difficulty.
4. Prefer the selected domain.
5. Prefer the selected technology.
6. Consider experience level.
7. Consider interest.
8. Consider project type.
9. Keep descriptions short and meaningful.
10. Give a match score from 0 to 100.
11. Give exactly 3 short reasons.
12. Return ONLY valid JSON.
13. Do not use Markdown.
14. Do not add explanations.

Return this JSON structure:

{{
    "projects": [
        {{
            "title": "Project Name",
            "domain": "Project Domain",
            "technology": "Main Technology",
            "experience": "Experience Level",
            "difficulty": "Difficulty",
            "interest": "Interest",
            "type": "Project Type",
            "description": "Short project description",
            "technologies": [
                "Technology 1",
                "Technology 2",
                "Technology 3"
            ],
            "score": 95,
            "reasons": [
                "Domain matches",
                "Technology matches",
                "Interest matches"
            ]
        }}
    ]
}}
"""

    try:

        print("Groq AI request started...")

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "system",
                    "content":
                    "You are an expert college project recommendation AI. Return only valid JSON."
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,

            max_tokens=3000,

            response_format={
                "type": "json_object"
            }
        )

        print("Groq AI response received.")

        text = response.choices[0].message.content

        text = clean_json(text)

        data = json.loads(text)


        # =========================
        # GET PROJECT LIST
        # =========================

        if isinstance(data, dict):

            if "projects" in data:

                recommendations = data["projects"]

            elif "recommendations" in data:

                recommendations = data["recommendations"]

            else:

                recommendations = []

        elif isinstance(data, list):

            recommendations = data

        else:

            recommendations = []


        # =========================
        # VALIDATE PROJECTS
        # =========================

        if not isinstance(
            recommendations,
            list
        ):

            raise ValueError(
                "Invalid AI response format."
            )


        recommendations = [

            project

            for project in recommendations

            if isinstance(project, dict)
            and project.get("title")

        ]


        # =========================
        # SORT BY MATCH SCORE
        # =========================

        recommendations.sort(

            key=lambda project:
            project.get("score", 0),

            reverse=True

        )


        print(
            f"Successfully generated "
            f"{len(recommendations)} projects."
        )


        return recommendations[:6]


    except Exception as e:

        print("Groq API Error:")

        print(e)

        return []


# =========================
# AI PROJECT DETAILS
# =========================

def generate_project_details(project):

    prompt = f"""
You are an expert college project documentation AI.

Create detailed, practical and project-specific documentation
for the following college project.

Project Title:
{project.get("title", "")}

Domain:
{project.get("domain", "")}

Main Technology:
{project.get("technology", "")}

Experience Level:
{project.get("experience", "")}

Difficulty:
{project.get("difficulty", "")}

Project Description:
{project.get("description", "")}

Technologies:
{", ".join(project.get("technologies", []))}

IMPORTANT RULES:

1. All content must be specifically related to this project.
2. Do NOT give generic features.
3. Features must describe actual functionality of the project.
4. Objectives must explain what the project is designed to achieve.
5. Modules must represent actual parts of this project.
6. Development steps must be practical and follow a logical order.
7. Keep the language simple and suitable for a college project.
8. Do not repeat the project description unnecessarily.
9. Generate exactly 5 features.
10. Generate exactly 4 objectives.
11. Generate exactly 4 modules.
12. Generate exactly 6 development steps.
13. Future scope should be realistic.
14. Return ONLY valid JSON.
15. Do not use Markdown.
16. Do not add explanations outside JSON.

Return ONLY this JSON structure:

{{
    "overview": "Write 2 to 3 clear sentences explaining this specific project.",

    "objectives": [
        "Specific objective 1",
        "Specific objective 2",
        "Specific objective 3",
        "Specific objective 4"
    ],

    "features": [
        "Specific project feature 1",
        "Specific project feature 2",
        "Specific project feature 3",
        "Specific project feature 4",
        "Specific project feature 5"
    ],

    "modules": [
        "Specific project module 1",
        "Specific project module 2",
        "Specific project module 3",
        "Specific project module 4"
    ],

    "development_steps": [
        "Practical development step 1",
        "Practical development step 2",
        "Practical development step 3",
        "Practical development step 4",
        "Practical development step 5",
        "Practical development step 6"
    ],

    "future_scope": "Write one realistic sentence describing how this project can be improved or expanded in the future."
}}
"""

    try:

        print(
            "Generating project-specific details with Groq..."
        )


        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an expert college project documentation AI. Generate project-specific content and return only valid JSON."
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.6,

            max_tokens=1800,

            response_format={
                "type": "json_object"
            }

        )


        print(
            "Project details AI response received."
        )


        text = response.choices[0].message.content

        text = clean_json(text)

        details = json.loads(text)


        # =========================
        # VALIDATE DETAILS
        # =========================

        if not isinstance(details, dict):

            raise ValueError(
                "Invalid project details format."
            )


        # Make sure all required fields exist

        details.setdefault(
            "overview",
            project.get("description", "")
        )

        details.setdefault(
            "objectives",
            []
        )

        details.setdefault(
            "features",
            []
        )

        details.setdefault(
            "modules",
            []
        )

        details.setdefault(
            "development_steps",
            []
        )

        details.setdefault(
            "future_scope",
            ""
        )


        print(
            "Project-specific details generated successfully."
        )


        return details


    except Exception as e:

        print(
            "Project details error:"
        )

        print(e)


        # =========================
        # FALLBACK DETAILS
        # =========================

        return {

            "overview":
            project.get(
                "description",
                ""
            ),

            "objectives": [],

            "features": [],

            "modules": [],

            "development_steps": [],

            "future_scope": ""

        }