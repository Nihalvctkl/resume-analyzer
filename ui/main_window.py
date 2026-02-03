import tkinter as tk
from tkinter import filedialog

from parser.pdf_parser import parse_pdf
from parser.docx_parser import parse_docx
from utils.cleaner import clean_text
from analyzer.skill_extractor import load_skills, extract_skills
from analyzer.score import calculate_score
from analyzer.jd_matcher import match_jd_with_resume


class ResumeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Analyzer")
        self.root.geometry("700x500")

        self.resume_path = None
        self.jd_path = None

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="Resume Analyzer",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.resume_btn = tk.Button(
            btn_frame,
            text="Upload Resume",
            width=20,
            command=self.select_resume
        )
        self.resume_btn.grid(row=0, column=0, padx=10)

        self.jd_btn = tk.Button(
            btn_frame,
            text="Upload Job Description",
            width=20,
            command=self.select_jd
        )
        self.jd_btn.grid(row=0, column=1, padx=10)

        self.analyze_btn = tk.Button(
            self.root,
            text="Analyze",
            width=30,
            height=2,
            command=self.analyze
        )
        self.analyze_btn.pack(pady=15)

        self.output = tk.Text(
            self.root,
            height=15,
            width=80
        )
        self.output.pack(pady=10)

    def select_resume(self):
        path = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[("Resume Files", "*.pdf *.docx")]
        )
        if path:
            self.resume_path = path
            self.output.insert(tk.END, f"Selected resume: {path}\n")

    def select_jd(self):
        path = filedialog.askopenfilename(
            title="Select Job Description",
            filetypes=[("Text Files", "*.txt")]
        )
        if path:
            self.jd_path = path
            self.output.insert(tk.END, f"Selected JD: {path}\n")

    def analyze(self):
        self.output.delete("1.0", tk.END)

        if not self.resume_path:
            self.output.insert(tk.END, "Please upload a resume first.\n")
            return

        # Read resume
        if self.resume_path.lower().endswith(".pdf"):
            raw_text = parse_pdf(self.resume_path)
        else:
            raw_text = parse_docx(self.resume_path)

        cleaned_resume = clean_text(raw_text)
        skills = load_skills("data/skills.txt")

        # JD vs Resume mode
        if self.jd_path:
            with open(self.jd_path, "r", encoding="utf-8") as f:
                jd_text = f.read()

            cleaned_jd = clean_text(jd_text)

            result = match_jd_with_resume(
                cleaned_jd,
                cleaned_resume,
                skills
            )

            self.output.insert(tk.END, "JD vs Resume Analysis\n")
            self.output.insert(tk.END, "---------------------\n")
            self.output.insert(tk.END, f"JD Skills       : {result['jd_skills']}\n")
            self.output.insert(tk.END, f"Resume Skills  : {result['resume_skills']}\n")
            self.output.insert(tk.END, f"Missing Skills : {result['missing_skills']}\n")
            self.output.insert(tk.END, f"Score          : {result['score']['score']}%\n")

        # Resume-only mode
        else:
            found_skills = extract_skills(cleaned_resume, skills)
            score = calculate_score(found_skills, skills)

            self.output.insert(tk.END, "Resume Analysis\n")
            self.output.insert(tk.END, "---------------\n")
            self.output.insert(tk.END, f"Matched Skills : {found_skills}\n")
            self.output.insert(tk.END, f"Score          : {score['score']}%\n")


def launch_app():
    root = tk.Tk()
    ResumeAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_app()
