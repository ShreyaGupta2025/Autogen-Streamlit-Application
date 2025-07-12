# Autogen Streamlit Report Generation

This project is a Streamlit-based application for generating personalized lesson plan reports using AI agents. It leverages OpenAI's GPT models to automate report creation and provides an interactive web interface for users.

## Features
- Generate personalized lesson plan reports
- Interactive web UI with Streamlit
- Modular agent design for extensibility
- Support for multiple report templates

## Project Structure
```
├── home.py                        # Main Streamlit app entry point
├── requirements.txt              # Python dependencies
├── pages/                        # Additional Streamlit pages
│   ├── 1_Agent_Designer.py
│   ├── 4_AgenticSquad.py
├── src/                          # Source code modules
│   └── logo_title.py
├── images/                       # Image assets (e.g., logos)
├── work_dir/                     # Working directory for generated files
├── Personalised-lesson-plan-Report.docx  # Sample report template
├── Land-enroachement-Report.docx         # Example generated report
```

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App
Start the Streamlit app:
```bash
streamlit run home.py
```

The app will open in your default web browser. Use the sidebar to navigate between different agent modules and generate reports.