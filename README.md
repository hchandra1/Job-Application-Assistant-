# Job Application Assistant 💼🤖

A Python-based script to help users generate tailored resumes and cover letters based on a user's profile and a specific job description. The script leverages OpenAI's GPT models to customize the documents according to the user's input, following specific formatting guidelines.

---

## ✨ Features

- **User Profile Management**: Create or load a user profile containing personal and professional details.
- **Job Description Input**: Provide or load job descriptions to tailor the application.
- **Tailored Resume Generation**: Generate a resume following "Jake's Resume Format," emphasizing relevant skills and experiences for the specific job.
- **Custom Cover Letter Creation**: Generate a cover letter in "Dedy's Cover Letter Format," highlighting the user's interest and qualifications.
- **File Saving**: Automatically saves the generated resume and cover letter with timestamped filenames for easy organization.

---

## 🛠️ Requirements

- Python 3.7+
- Install dependencies:
  ```bash
  pip install openai
  ```
- Set up an OpenAI API key in your environment:
  ```bash
  export OPENAI_API_KEY="YOUR_API_KEY"
  ```

---

## 🚀 Usage

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/job-application-assistant.git
   cd job-application-assistant
   ```

2. **Run the Script**
   ```bash
   python job_application_assistant.py
   ```

3. **Follow the Prompts**
   - Create or load a user profile.
   - Create or load a job description.
   - The script will generate and save a tailored resume and cover letter.

---

## 📁 File Descriptions

- `job_application_assistant.py`: Main script to generate resumes and cover letters.
- `user_profile.json`: Stores user profile data (auto-generated).
- `job_description.json`: Stores job description data (auto-generated).
- `README.md`: Documentation for the project.

---

## 📝 Input Format

### User Profile
The user profile includes:
- Full Name
- Contact Email
- Phone Number
- Professional Summary
- Skills
- Work Experiences (Company, Role, Duration, Responsibilities)
- Education (Institution, Degree, Graduation Year)

### Job Description
The job description includes:
- Company Name
- Position Title
- Responsibilities
- Required Skills
- Job Location
- Job Summary
- Additional Notes (optional)

---

## 📄 Output

### Tailored Resume
The resume is formatted according to "Jake's Resume Format":
1. Header with candidate's name.
2. Contact details.
3. Professional summary.
4. Skills in bullet points.
5. Work experience (most recent first).
6. Education.

### Custom Cover Letter
The cover letter follows "Dedy's Cover Letter Format":
1. Polite salutation.
2. Introduction referencing the job title and interest.
3. Key skills and relevant experience.
4. Closing paragraph with a call to action.
5. Formal sign-off.

---

## 🛠️ Example Workflow

1. **Step 1: Load/Create User Profile**
   - Input details like name, email, phone, skills, etc.
   - Optionally, load an existing profile from `user_profile.json`.

2. **Step 2: Load/Create Job Description**
   - Input job details like company name, role, responsibilities, and required skills.
   - Optionally, load an existing description from `job_description.json`.

3. **Step 3: Generate Documents**
   - Tailored resume and cover letter are generated and saved with filenames like:
     - `job_app_resume_YYYYMMDD_HHMMSS.txt`
     - `job_app_cover_letter_YYYYMMDD_HHMMSS.txt`

---

## 🤝 Contribution
Feel free to fork this repository and make contributions. Open a pull request for any enhancements or bug fixes.

---

## 📜 License
This project is licensed under the MIT License.

---

## 🙌 Acknowledgments
Special thanks to OpenAI for the GPT models and to "Jake" and "Dedy" for the inspiration behind the formats. 🎉
