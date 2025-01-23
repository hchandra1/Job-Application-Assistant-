#!/usr/bin/env python3
"""
======================================================
Job Application Assistant
======================================================
A Python script that helps users generate a customized
cover letter and tailor each resume according to the
inputted job description. The final resume follows
Jake's resume format, and the cover letter follows
Dedy's cover letter format.

Usage:
    1. Set your environment variable for OpenAI:
        export OPENAI_API_KEY="YOUR_API_KEY"
    2. Prepare a JSON file with your user profile data (if desired).
    3. Run the script: python job_application_assistant.py
    4. Follow prompts or use the direct function calls in code.

Requirements:
    - Python 3.7+
    - openai (pip install openai)

======================================================
"""

import os
import sys
import json
import openai
import datetime
from typing import List, Dict, Optional

# Set up your OpenAI API key (either from environment or direct assignment).
# openai.api_key = "YOUR_API_KEY"  # <-- Optionally set here
openai.api_key = os.environ.get("OPENAI_API_KEY", None)

# -------------------------
# Constants
# -------------------------
DEFAULT_USER_PROFILE_FILE = "user_profile.json"
DEFAULT_JOB_DESCRIPTION_FILE = "job_description.json"
MODEL_NAME = "gpt-3.5-turbo"  # or "gpt-4" if you have access
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# ------------------------------------------------------------------------
# Data Classes
# ------------------------------------------------------------------------
class UserProfile:
    """
    Represents a user's personal and professional details.
    """
    def __init__(
        self,
        full_name: str,
        contact_email: str,
        phone_number: str,
        professional_summary: str,
        skills: List[str],
        experiences: List[Dict[str, str]],
        education: List[Dict[str, str]],
    ) -> None:
        self.full_name = full_name
        self.contact_email = contact_email
        self.phone_number = phone_number
        self.professional_summary = professional_summary
        self.skills = skills
        # experiences: list of dict with keys like 'company', 'role', 'duration', 'description'
        self.experiences = experiences
        # education: list of dict with keys like 'institution', 'degree', 'graduation_year'
        self.education = education

    def to_dict(self) -> Dict:
        return {
            "full_name": self.full_name,
            "contact_email": self.contact_email,
            "phone_number": self.phone_number,
            "professional_summary": self.professional_summary,
            "skills": self.skills,
            "experiences": self.experiences,
            "education": self.education,
        }

    @staticmethod
    def from_dict(data: Dict) -> "UserProfile":
        return UserProfile(
            full_name=data.get("full_name", ""),
            contact_email=data.get("contact_email", ""),
            phone_number=data.get("phone_number", ""),
            professional_summary=data.get("professional_summary", ""),
            skills=data.get("skills", []),
            experiences=data.get("experiences", []),
            education=data.get("education", []),
        )


class JobDescription:
    """
    Holds information about a specific job opening.
    """
    def __init__(
        self,
        company_name: str,
        position_title: str,
        responsibilities: str,
        required_skills: List[str],
        job_location: str,
        job_summary: str,
        additional_notes: Optional[str] = None,
    ) -> None:
        self.company_name = company_name
        self.position_title = position_title
        self.responsibilities = responsibilities
        self.required_skills = required_skills
        self.job_location = job_location
        self.job_summary = job_summary
        self.additional_notes = additional_notes

    def to_dict(self) -> Dict:
        return {
            "company_name": self.company_name,
            "position_title": self.position_title,
            "responsibilities": self.responsibilities,
            "required_skills": self.required_skills,
            "job_location": self.job_location,
            "job_summary": self.job_summary,
            "additional_notes": self.additional_notes,
        }

    @staticmethod
    def from_dict(data: Dict) -> "JobDescription":
        return JobDescription(
            company_name=data.get("company_name", ""),
            position_title=data.get("position_title", ""),
            responsibilities=data.get("responsibilities", ""),
            required_skills=data.get("required_skills", []),
            job_location=data.get("job_location", ""),
            job_summary=data.get("job_summary", ""),
            additional_notes=data.get("additional_notes", ""),
        )

# ------------------------------------------------------------------------
# Formatting Classes for Jake's Resume and Dedy's Cover Letter
# ------------------------------------------------------------------------
class JakesResumeFormatter:
    """
    Enforces 'Jake's resume format' on any given resume text.
    This can be used to post-process or instruct an LLM on how
    to structure the final resume content.
    """

    @staticmethod
    def get_format_instructions() -> str:
        """
        Returns a text block that describes Jake's preferred resume format.
        
        Example Format (Jake's):
        1. Header: Candidate Name (bold, large font)
        2. Contact info: Email and Phone
        3. Professional Summary
        4. Core Skills as bullet points
        5. Professional Experience (chronological)
        6. Education
        7. (Optionally) Additional Sections
        """
        instructions = (
            "Use Jake's Resume Format:\n"
            "1. Header with the candidate's name in a bold or emphasized style.\n"
            "2. Immediately below, contact details (email and phone) on one line.\n"
            "3. A short 'Professional Summary' section.\n"
            "4. A 'Skills' section with bullet points.\n"
            "5. An 'Experience' section in chronological order (most recent first).\n"
            "6. An 'Education' section with degrees, institutions, and graduation dates.\n"
            "7. Keep layout neat and minimal, using consistent headings.\n"
        )
        return instructions

    @staticmethod
    def post_process_text(llm_output: str) -> str:
        """
        Optionally modify or refine the LLM's output if you wish
        to impose final formatting details (like ASCII lines, spacing).
        For now, we simply return the text as is.
        """
        # You could do additional string operations here if desired.
        return llm_output


class DedyCoverLetterFormatter:
    """
    Enforces 'Dedy's cover letter format' on any given cover letter text.
    """

    @staticmethod
    def get_format_instructions() -> str:
        """
        Returns a text block that describes Dedy's preferred cover letter format.
        
        Example Format (Dedy’s):
        1. Salutation (Dear [Hiring Manager Name or Team]),
        2. Short introduction paragraph referencing the specific role and company
        3. One or two paragraphs highlighting relevant skills/experience
        4. Closing paragraph with a clear call to action or thank you
        5. Formal sign-off (Sincerely, Best Regards, etc.) and your name
        """
        instructions = (
            "Use Dedy's Cover Letter Format:\n"
            "1. Start with a polite salutation (e.g., 'Dear Hiring Manager at COMPANY').\n"
            "2. A short introduction referencing the position title and why you're interested.\n"
            "3. One or two concise paragraphs connecting your key skills to the job requirements.\n"
            "4. A concluding paragraph that reaffirms your interest and gratitude.\n"
            "5. A formal sign-off (e.g., 'Sincerely,') followed by your full name.\n"
            "6. Maintain a professional yet friendly tone throughout.\n"
        )
        return instructions

    @staticmethod
    def post_process_text(llm_output: str) -> str:
        """
        Optionally tweak final text if you want to enforce specific line breaks,
        spacing, or salutation. Currently, returns as is.
        """
        return llm_output


# ------------------------------------------------------------------------
# Utility Functions for Loading/Saving Data
# ------------------------------------------------------------------------
def load_user_profile(profile_file: str) -> UserProfile:
    """
    Loads user profile data from a JSON file and returns a UserProfile object.
    """
    if not os.path.exists(profile_file):
        print(f"[WARNING] No profile file found at '{profile_file}'. Returning a blank profile.")
        return UserProfile("", "", "", "", [], [], [])

    with open(profile_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return UserProfile.from_dict(data)


def save_user_profile(profile: UserProfile, profile_file: str) -> None:
    """
    Saves user profile data to a JSON file.
    """
    with open(profile_file, "w", encoding="utf-8") as f:
        json.dump(profile.to_dict(), f, indent=4)
    print(f"[INFO] User profile saved to '{profile_file}'.")


def load_job_description(job_file: str) -> JobDescription:
    """
    Loads job description data from a JSON file and returns a JobDescription object.
    """
    if not os.path.exists(job_file):
        print(f"[WARNING] No job description file found at '{job_file}'. Returning a blank job description.")
        return JobDescription("", "", "", [], "", "")

    with open(job_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return JobDescription.from_dict(data)


def save_job_description(job_desc: JobDescription, job_file: str) -> None:
    """
    Saves job description data to a JSON file.
    """
    with open(job_file, "w", encoding="utf-8") as f:
        json.dump(job_desc.to_dict(), f, indent=4)
    print(f"[INFO] Job description saved to '{job_file}'.")


# ------------------------------------------------------------------------
# Interactive CLI Gathering
# ------------------------------------------------------------------------
def gather_user_profile_input() -> UserProfile:
    """
    Interactively gathers user profile info from the CLI.
    """
    print("\n=== Gather User Profile Information ===")
    full_name = input("Full Name: ").strip()
    contact_email = input("Contact Email: ").strip()
    phone_number = input("Phone Number: ").strip()

    print("\nProfessional Summary (one or two sentences):")
    professional_summary = input("> ").strip()

    print("\nList some key skills separated by commas (e.g. Python, Data Analysis, Leadership):")
    raw_skills = input("> ").strip()
    skills_list = [skill.strip() for skill in raw_skills.split(",") if skill.strip()]

    experiences = []
    while True:
        print("\nAdd a work experience? (y/n)")
        choice = input("> ").lower().strip()
        if choice != 'y':
            break
        company = input("Company Name: ").strip()
        role = input("Role/Position: ").strip()
        duration = input("Duration (e.g., 2019-2021): ").strip()
        description = input("Brief Description of Responsibilities: ").strip()

        experiences.append({
            "company": company,
            "role": role,
            "duration": duration,
            "description": description
        })

    education = []
    while True:
        print("\nAdd an education entry? (y/n)")
        choice = input("> ").lower().strip()
        if choice != 'y':
            break
        institution = input("Institution Name: ").strip()
        degree = input("Degree (e.g. BSc in Computer Science): ").strip()
        grad_year = input("Graduation Year: ").strip()

        education.append({
            "institution": institution,
            "degree": degree,
            "graduation_year": grad_year
        })

    return UserProfile(
        full_name=full_name,
        contact_email=contact_email,
        phone_number=phone_number,
        professional_summary=professional_summary,
        skills=skills_list,
        experiences=experiences,
        education=education
    )


def gather_job_description_input() -> JobDescription:
    """
    Interactively gathers job description data from the CLI.
    """
    print("\n=== Gather Job Description ===")
    company_name = input("Company Name: ").strip()
    position_title = input("Position Title: ").strip()
    print("\nProvide responsibilities or summary for this role (multi-line; end with blank line):")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    responsibilities = "\n".join(lines)

    print("\nList required skills separated by commas (e.g. React, Node.js, Team Management):")
    raw_skills = input("> ").strip()
    required_skills_list = [skill.strip() for skill in raw_skills.split(",") if skill.strip()]

    job_location = input("Job Location: ").strip()

    print("\nProvide a quick job summary or desired qualifications (multi-line; end with blank line):")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    job_summary = "\n".join(lines)

    additional_notes = input("\nAny additional notes about the position or application process? ").strip()

    return JobDescription(
        company_name=company_name,
        position_title=position_title,
        responsibilities=responsibilities,
        required_skills=required_skills_list,
        job_location=job_location,
        job_summary=job_summary,
        additional_notes=additional_notes
    )

# ------------------------------------------------------------------------
# Resume & Cover Letter Generators
# ------------------------------------------------------------------------
def build_base_resume_text(user: UserProfile) -> str:
    """
    Creates a basic resume text from the user profile.
    This text is used as input for the LLM to tailor.
    """
    lines = []
    lines.append(f"Name: {user.full_name}")
    lines.append(f"Email: {user.contact_email}")
    lines.append(f"Phone: {user.phone_number}")
    lines.append("\nProfessional Summary:")
    lines.append(user.professional_summary)

    lines.append("\nSkills:")
    for skill in user.skills:
        lines.append(f"- {skill}")

    lines.append("\nExperience:")
    for exp in user.experiences:
        lines.append(f"{exp['role']} at {exp['company']} ({exp['duration']})")
        lines.append(f"  {exp['description']}")

    lines.append("\nEducation:")
    for edu in user.education:
        lines.append(f"{edu['degree']} from {edu['institution']} - {edu['graduation_year']}")

    return "\n".join(lines)


def generate_tailored_resume(user: UserProfile, job: JobDescription) -> str:
    """
    Uses an LLM to propose modifications to the user's resume text that
    highlight relevant experience and skills for the job description.
    Returns a resume as a string in Jake's resume format.
    """
    if not openai.api_key:
        return "[ERROR] OpenAI API key not found. Cannot generate tailored resume."

    base_resume_text = build_base_resume_text(user)
    jake_format_instructions = JakesResumeFormatter.get_format_instructions()

    prompt = (
        "You are a helpful assistant that customizes resumes.\n"
        "Given the following base resume and job description,\n"
        "produce a final tailored resume that emphasizes relevant\n"
        "skills and experiences. Keep length concise but effective.\n\n"
        f"{jake_format_instructions}\n"
        "Base Resume:\n"
        f"{base_resume_text}\n\n"
        "Job Description:\n"
        f"Company Name: {job.company_name}\n"
        f"Position Title: {job.position_title}\n"
        f"Responsibilities:\n{job.responsibilities}\n"
        f"Required Skills: {', '.join(job.required_skills)}\n"
        f"Location: {job.job_location}\n"
        f"Job Summary:\n{job.job_summary}\n"
        f"Additional Notes: {job.additional_notes or 'N/A'}\n\n"
        "Final Tailored Resume (following Jake's format):"
    )

    # Make the call to the OpenAI API
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )
    tailored_resume = response.choices[0].message.content.strip()

    # Optionally post-process if needed
    final_resume_text = JakesResumeFormatter.post_process_text(tailored_resume)
    return final_resume_text


def generate_cover_letter(user: UserProfile, job: JobDescription) -> str:
    """
    Generates a cover letter based on the user's profile and the job description
    in Dedy's cover letter format.
    """
    if not openai.api_key:
        return "[ERROR] OpenAI API key not found. Cannot generate cover letter."

    dedy_format_instructions = DedyCoverLetterFormatter.get_format_instructions()

    # Construct prompt for cover letter
    prompt = (
        "You are an expert at writing professional cover letters. Given the "
        "user's details and the job description, write a cover letter that is "
        "polite, engaging, concise, and highlights the user's relevant skills, "
        "experiences, and genuine interest. Follow Dedy's cover letter format.\n\n"
        f"{dedy_format_instructions}\n\n"
        f"User's Name: {user.full_name}\n"
        f"Professional Summary: {user.professional_summary}\n"
        f"Key Skills: {', '.join(user.skills)}\n\n"
        "User's Experiences:\n"
    )

    for idx, exp in enumerate(user.experiences, start=1):
        prompt += (
            f"{idx}. {exp['role']} at {exp['company']} "
            f"({exp['duration']}): {exp['description']}\n"
        )

    prompt += (
        "\nJob Description:\n"
        f"Company Name: {job.company_name}\n"
        f"Position Title: {job.position_title}\n"
        f"Responsibilities:\n{job.responsibilities}\n"
        f"Required Skills: {', '.join(job.required_skills)}\n"
        f"Location: {job.job_location}\n"
        f"Job Summary:\n{job.job_summary}\n"
        f"Additional Notes: {job.additional_notes}\n\n"
        "Now write the cover letter following Dedy's format."
    )

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )

    cover_letter = response.choices[0].message.content.strip()
    final_cover_letter = DedyCoverLetterFormatter.post_process_text(cover_letter)
    return final_cover_letter

# ------------------------------------------------------------------------
# File Saving Utilities
# ------------------------------------------------------------------------
def save_document_to_file(document_content: str, output_filename: str) -> None:
    """
    Saves the text content to a file.
    """
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(document_content)
    print(f"[INFO] Document saved to '{output_filename}'.")


def create_output_filenames(base_name: str = "application") -> Dict[str, str]:
    """
    Creates timestamped output filenames for the tailored resume and cover letter.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    resume_filename = f"{base_name}_resume_{timestamp}.txt"
    cover_letter_filename = f"{base_name}_cover_letter_{timestamp}.txt"
    return {
        "resume": resume_filename,
        "cover_letter": cover_letter_filename
    }

# ------------------------------------------------------------------------
# Main Program Flow
# ------------------------------------------------------------------------
def main():
    """
    High-level flow:
    1. Load existing user profile or prompt to create one.
    2. Load existing job description or prompt to create one.
    3. Generate tailored resume (Jake's format).
    4. Generate cover letter (Dedy's format).
    5. Save files.
    """
    print("\n=============================================")
    print("       Welcome to the Job Application Assistant")
    print("=============================================\n")

    user_profile = None
    job_desc = None

    # Step 1: Check if user wants to load or create a user profile
    print("Do you want to (l)oad an existing user profile or (c)reate a new one?")
    choice_profile = input("> ").strip().lower()
    if choice_profile == 'l':
        print(f"\n[INFO] Loading user profile from '{DEFAULT_USER_PROFILE_FILE}'...")
        user_profile = load_user_profile(DEFAULT_USER_PROFILE_FILE)
    else:
        user_profile = gather_user_profile_input()
        # Save after creation
        save_user_profile(user_profile, DEFAULT_USER_PROFILE_FILE)

    # Step 2: Check if user wants to load or create a job description
    print("\nDo you want to (l)oad a job description or (c)reate a new one?")
    choice_job = input("> ").strip().lower()
    if choice_job == 'l':
        print(f"\n[INFO] Loading job description from '{DEFAULT_JOB_DESCRIPTION_FILE}'...")
        job_desc = load_job_description(DEFAULT_JOB_DESCRIPTION_FILE)
    else:
        job_desc = gather_job_description_input()
        save_job_description(job_desc, DEFAULT_JOB_DESCRIPTION_FILE)

    # Step 3: Generate the tailored resume (Jake's format)
    print("\n[INFO] Generating a tailored resume in Jake's format using OpenAI LLM...")
    tailored_resume = generate_tailored_resume(user_profile, job_desc)

    # Step 4: Generate the cover letter (Dedy's format)
    print("\n[INFO] Generating the cover letter in Dedy's format using OpenAI LLM...")
    cover_letter = generate_cover_letter(user_profile, job_desc)

    # Step 5: Save the results to files
    filenames = create_output_filenames(base_name="job_app")
    save_document_to_file(tailored_resume, filenames["resume"])
    save_document_to_file(cover_letter, filenames["cover_letter"])

    print("\n[SUCCESS] Your tailored resume and cover letter have been generated and saved.")
    print(f"Resume: {filenames['resume']}")
    print(f"Cover Letter: {filenames['cover_letter']}")

# ------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------
if __name__ == "__main__":
    main()
