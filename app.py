import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from google import genai

app = FastAPI(title="FitBuddy AI Fitness Plan Generator")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Warning: GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key) if api_key else None


def generate_ai_plan(name, age, weight, goal, intensity):

    prompt = f"""
You are FitBuddy, an AI fitness assistant.

Create a simple 7-day fitness plan for:

Name: {name}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

Give:
1. A 7-day workout plan
2. One simple nutrition tip
3. One recovery tip

Keep the answer beginner-friendly and easy to understand.
Do not give dangerous or extreme medical advice.
"""

    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Gemini error: {e}"

    return "Gemini API key is not available."


@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FitBuddy AI</title>

        <style>
            body {
                font-family: Arial;
                max-width: 700px;
                margin: 40px auto;
                padding: 20px;
                background: #f4f7f9;
            }

            .box {
                background: white;
                padding: 30px;
                border-radius: 15px;
            }

            input, select, button {
                width: 100%;
                padding: 12px;
                margin: 8px 0 15px;
                box-sizing: border-box;
            }

            button {
                background: #222;
                color: white;
                border: none;
                cursor: pointer;
                border-radius: 6px;
            }

            h1 {
                text-align: center;
            }
        </style>
    </head>

    <body>

        <div class="box">

            <h1>FitBuddy AI 🏋️</h1>

            <form action="/generate" method="post">

                <label>Name</label>
                <input type="text" name="name" required>

                <label>Age</label>
                <input type="number" name="age" required>

                <label>Weight (kg)</label>
                <input type="number" name="weight" required>

                <label>Fitness Goal</label>

                <select name="goal">
                    <option value="weight loss">Weight Loss</option>
                    <option value="muscle gain">Muscle Gain</option>
                    <option value="general wellness">General Wellness</option>
                </select>

                <label>Workout Intensity</label>

                <select name="intensity">
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                </select>

                <button type="submit">
                    Generate AI Fitness Plan
                </button>

            </form>

        </div>

    </body>
    </html>
    """


@app.post("/generate", response_class=HTMLResponse)
def generate(
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    result = generate_ai_plan(
        name,
        age,
        weight,
        goal,
        intensity
    )

    formatted_result = result.replace("\n", "<br>")

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>FitBuddy Result</title>

        <style>

            body {{
                font-family: Arial;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
                background: #f4f7f9;
            }}

            .box {{
                background: white;
                padding: 30px;
                border-radius: 15px;
            }}

            .result {{
                line-height: 1.7;
            }}

            a {{
                display: inline-block;
                margin-top: 20px;
            }}

        </style>

    </head>

    <body>

        <div class="box">

            <h1>FitBuddy AI Plan 🏋️</h1>

            <p><b>Name:</b> {name}</p>
            <p><b>Age:</b> {age}</p>
            <p><b>Weight:</b> {weight} kg</p>
            <p><b>Goal:</b> {goal}</p>
            <p><b>Intensity:</b> {intensity}</p>

            <hr>

            <h2>AI Generated Fitness Plan</h2>

            <div class="result">
                {formatted_result}
            </div>

            <a href="/">← Create another plan</a>

        </div>

    </body>

    </html>
    """