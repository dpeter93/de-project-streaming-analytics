from flask import Flask
from flask import request
import os
import subprocess

# Create a Flask application instance
app = Flask(__name__)

# Defines the route for the Flask application, when a POST request is made to the endpoint the run() function will run
@app.route("/dbt", methods=["POST"])
def run():

    # Define command and arguments list
    command = ["dbt"]
    arguments = []

    # Parse the request data
    request_data = request.get_json()

    # Checks the JSON data exists and the parameters of the request data, split the parameters and extends the command with those
    if request_data:
        if "cli" in request_data.get("params", {}):
            arguments = request_data["params"]["cli"].split(" ")
            command.extend(arguments)

    # Add an argument for the project dir if not specified from the environment variable and extends the command
    if not any("--project-dir" in c for c in command):
        project_dir = os.environ.get("DBT_PROJECT_DIR", None)
        if project_dir:
            command.extend(["--project-dir", project_dir])

    # Execute the dbt command and captures the output as a text
    result = subprocess.run(command,
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)

    # Format the response
    response = {
        "result": {
            "status": "ok" if result.returncode == 0 else "error",
            "args": result.args,
            "return_code": result.returncode,
            "command_output": result.stdout,
        }
    }

    return response, 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))