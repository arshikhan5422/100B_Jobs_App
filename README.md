# 100B_Jobs_App
# 📊 100B Jobs App — Candidate Filtering & Ranking Dashboard

This Streamlit web application helps recruiters and hiring managers filter, rank, and select top candidates from a JSON file (`form-submissions.json`) containing candidate submission data. The app supports both manual filtering and optional LLM-powered (Gemini) candidate summaries.

---

## 🚀 Features

- 📂 Upload JSON file containing candidate data
- 🔍 Filter candidates by:
  - Minimum years of experience
  - Skills (e.g., Python, React)
- 🎯 Score & rank candidates based on experience and keyword relevance
- ✅ Select top 5 candidates for final review
- 🤖 (Optional): Use Gemini Pro to generate AI summaries of resumes

---

## 🧪 Technologies Used

- Python
- Streamlit
- Pandas
- Google Generative AI (Gemini)
- dotenv

---

## 📁 Input Format

Upload a `form-submissions.json` file containing structured candidate data.

Each entry should look like:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "location": "New York",
  "work_availability": ["full-time"],
  "annual_salary_expectation": {
    "full-time": "120000"
  },
  "work_experiences": [
    {
      "roleName": "Software Engineer",
      "company": "TechCorp"
    }
  ]
}
## ⚙️ Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/arshikhan5422/100B_Jobs_App.git
   cd 100B_Jobs_App
