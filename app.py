from flask import Flask, render_template, request, session
from recommendation import recommend_projects, generate_project_details


app = Flask(__name__)

app.secret_key = "ai-project-finder-secret-key"


# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# ABOUT PAGE
# =========================
@app.route("/about")
def about():
    return render_template("about.html")

# =========================
# CATEGORIES PAGE
# =========================
@app.route("/categories")
def categories():
    return render_template("categories.html")

# =========================
# HOW IT WORKS PAGE
# =========================
@app.route("/how-it-works")
def how_it_works():
    return render_template("how-it-works.html")

# =========================
# RECOMMEND PAGE
# =========================
@app.route("/recommend", methods=["GET", "POST"])
def recommend():

    # Normal page open
    if request.method == "GET":
        return render_template("recommend.html")

    # Form submit
    if request.method == "POST":

        preferences = {
            "domain": request.form.get("domain", ""),
            "technology": request.form.get("technology", ""),
            "experience": request.form.get("experience", ""),
            "difficulty": request.form.get("difficulty", ""),
            "interest": request.form.get("interest", ""),
            "type": request.form.get("project_type", "")
        }

        print("Generating AI recommendations...")
        print("Preferences:", preferences)

        recommendations = recommend_projects(preferences)

        if not recommendations:

            return render_template(
                "recommend.html",
                error="AI is temporarily unavailable. Please try again."
            )

        # Save AI projects in session
        session["ai_projects"] = recommendations
        session["ai_preferences"] = preferences

        # Show first 6 projects
        first_projects = recommendations[:6]

        print(
            f"AI generated {len(recommendations)} projects."
        )

        return render_template(
            "results.html",
            recommendations=first_projects,
            preferences=preferences,
            more_results=False
        )

# =========================
# AI RESULTS PAGE
# =========================
@app.route("/results")
def results():

    preferences = {
        "domain": request.args.get("domain", ""),
        "technology": request.args.get("technology", ""),
        "experience": request.args.get("experience", ""),
        "difficulty": request.args.get("difficulty", ""),
        "interest": request.args.get("interest", ""),
        "type": request.args.get("project_type", "")
    }

    print("Generating AI recommendations...")

    recommendations = recommend_projects(preferences)

    if not recommendations:

        print("AI could not generate projects.")

        return render_template(
            "results.html",
            recommendations=[],
            preferences=preferences,
            error="AI is temporarily unavailable. Please try again."
        )

    # Save all AI projects
    session["ai_projects"] = recommendations
    session["ai_preferences"] = preferences

    # First 6 projects
    first_projects = recommendations[:6]

    print(
        f"AI generated {len(recommendations)} projects."
    )

    return render_template(
        "results.html",
        recommendations=first_projects,
        preferences=preferences,
        more_results=False
    )


# =========================
# MORE AI PROJECTS
# =========================
@app.route("/more-projects")
def more_projects():

    preferences = {
        "domain": request.args.get("domain", ""),
        "technology": request.args.get("technology", ""),
        "experience": request.args.get("experience", ""),
        "difficulty": request.args.get("difficulty", ""),
        "interest": request.args.get("interest", ""),
        "type": request.args.get("project_type", "")
    }

    print("Generating more AI projects...")

    recommendations = recommend_projects(preferences)

    if not recommendations:

        print("More AI projects could not be generated.")

        return render_template(
            "results.html",
            recommendations=[],
            preferences=preferences,
            more_results=True,
            error="AI is temporarily unavailable. Please try again."
        )

    print(
        f"More AI projects generated: "
        f"{len(recommendations)}"
    )

    return render_template(
        "results.html",
        recommendations=recommendations,
        preferences=preferences,
        more_results=True
    )

# =========================
# DYNAMIC PROJECT DETAILS
# =========================
@app.route("/details")
def details():

    title = request.args.get(
        "title",
        ""
    )

    # Get saved projects
    all_projects = session.get(
        "ai_projects",
        []
    )

    selected_project = None

    # Find selected project
    for project in all_projects:

        if project.get("title") == title:

            selected_project = project

            break


    # If project was found
    if selected_project:

        print(
            f"Generating AI details for: {title}"
        )

        ai_details = generate_project_details(
            selected_project
        )

        return render_template(
            "details.html",

            title=selected_project.get(
                "title",
                ""
            ),

            domain=selected_project.get(
                "domain",
                ""
            ),

            technology=selected_project.get(
                "technology",
                ""
            ),

            difficulty=selected_project.get(
                "difficulty",
                ""
            ),

            experience=selected_project.get(
                "experience",
                ""
            ),

            description=selected_project.get(
                "description",
                ""
            ),

            technologies=selected_project.get(
                "technologies",
                []
            ),

            details=ai_details
        )


    # Fallback if project is not found
    return render_template(
        "details.html",

        title=title,

        domain=request.args.get(
            "domain",
            ""
        ),

        technology=request.args.get(
            "technology",
            ""
        ),

        difficulty=request.args.get(
            "difficulty",
            ""
        ),

        experience=request.args.get(
            "experience",
            ""
        ),

        description=request.args.get(
            "description",
            ""
        ),

        technologies=[],

        details={
            "overview": request.args.get(
                "description",
                ""
            ),
            "objectives": [],
            "features": [],
            "modules": [],
            "development_steps": [],
            "future_scope": ""
        }
    )


# =========================
# CONTACT PAGE
# =========================
@app.route(
    "/contact",
    methods=["GET", "POST"]
)
def contact():

    if request.method == "POST":

        name = request.form.get(
            "name"
        )

        email = request.form.get(
            "email"
        )

        subject = request.form.get(
            "subject"
        )

        message = request.form.get(
            "message"
        )

        print(
            "\n========== CONTACT MESSAGE =========="
        )

        print(
            "Name:",
            name
        )

        print(
            "Email:",
            email
        )

        print(
            "Subject:",
            subject
        )

        print(
            "Message:",
            message
        )

        print(
            "=====================================\n"
        )

        return render_template(
            "contact.html",
            success=True
        )

    return render_template(
        "contact.html"
    )


# =========================
# START FLASK
# =========================
if __name__ == "__main__":

    app.run(
        debug=True
    )