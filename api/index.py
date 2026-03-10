from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Load Trained Model
model_path = os.path.join(os.path.dirname(__file__), '..', 'student_model.pkl')
model = pickle.load(open(model_path, "rb"))

# Skill Suggestion Function
def suggest_skills(study_hours,
                   distraction_level,
                   sleep_hours,
                   stress_level,
                   assignment_completion_rate,
                   class_participation_level,
                   daily_goal_planning):

    skills = []

    excellent_conditions = (
        study_hours >= 4 and
        distraction_level <= 4 and
        sleep_hours >= 7 and
        stress_level <= 5 and
        assignment_completion_rate >= 80 and
        class_participation_level >= 6 and
        daily_goal_planning == 1
    )

    if excellent_conditions:
        return ["Excellent Performance! No need to improve any skills 🎉"]

    if study_hours < 4:
        skills.append("Increase Daily Study Hours")

    if daily_goal_planning == 0:
        skills.append("Start Daily Goal Planning")

    if distraction_level > 4:
        skills.append("Reduce Distractions and Improve Focus")

    if sleep_hours < 7:
        skills.append("Maintain Better Sleep Routine")

    if stress_level > 5:
        skills.append("Practice Stress Management Techniques")

    if assignment_completion_rate < 80:
        skills.append("Increase Assignment Completion Consistency")

    if class_participation_level < 6:
        skills.append("Improve Class Participation")

    return skills[:3]

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Show Form Page (GET)
@app.route("/predict", methods=["GET"])
def show_form():
    return render_template("index.html")

@app.route('/form')
def form_page():
    return render_template('index.html')

# Handle Prediction (POST)
@app.route("/predict", methods=["POST"])
def predict():
    study_hours = float(request.form["study_hours"])
    distraction_level = float(request.form["distraction_level"])
    sleep_hours = float(request.form["sleep_hours"])
    stress_level = float(request.form["stress_level"])
    assignment_completion_rate = float(request.form["assignment_completion_rate"])
    class_participation_level = float(request.form["class_participation_level"])
    daily_goal_planning = int(request.form["daily_goal_planning"])

    features = np.array([[ 
        study_hours,
        distraction_level,
        sleep_hours,
        stress_level,
        assignment_completion_rate,
        class_participation_level,
        daily_goal_planning
    ]])

    prediction = model.predict(features)

    skills = suggest_skills(
        study_hours,
        distraction_level,
        sleep_hours,
        stress_level,
        assignment_completion_rate,
        class_participation_level,
        daily_goal_planning
    )

    return render_template(
        "result.html",
        prediction=round(prediction[0], 2),
        skills=skills
    )

# Vercel serverless handler
if __name__ == "__main__":
    app.run(debug=True)
else:
    # Export for Vercel
    def handler(event, context):
        return app(event, context)
