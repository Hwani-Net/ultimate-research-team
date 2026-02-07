
import json
import os

def get_content(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

app_py = get_content('app.py')
agents_py = get_content('agents.py')
tasks_py = get_content('tasks.py')
dot_env = get_content('.env')

# Prepare the index.html content
index_html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>Ultimate Research Team - Antigravity v11.2</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.57.0/build/stlite.css" />
    <style>
      #root {{ height: 100vh; }}
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.57.0/build/stlite.js"></script>
    <script>
      stlite.mount({{
        requirements: ["crewai", "crewai-tools", "langchain-google-genai", "python-dotenv", "pydantic==2.10.6"],
        entrypoint: "app.py",
        files: {{
          "app.py": {json.dumps(app_py)},
          "agents.py": {json.dumps(agents_py)},
          "tasks.py": {json.dumps(tasks_py)},
          ".env": {json.dumps(dot_env)}
        }},
        stliteConfig: {{
          platform: "browser"
        }}
      }}, document.getElementById("root"));
    </script>
  </body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("Successfully generated index.html for stlite deployment.")
