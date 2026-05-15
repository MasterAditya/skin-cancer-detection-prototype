import os

project_structure = {
    "skin_ai_demo": {
        "app.py": "",
        "requirements.txt": "",
        "model": {
            "loader.py": "",
            "predictor.py": "",
        },
        "explainability": {
            "gradcam.py": "",
        },
        "decision": {
            "risk.py": "",
        },
        "utils": {
            "preprocessing.py": "",
            "constants.py": "",
        },
        "ui": {
            "components.py": "",
            "styling.py": "",
        },
    }
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


create_structure(".", project_structure)

print("✅ skin_ai_demo directory structure created successfully.")