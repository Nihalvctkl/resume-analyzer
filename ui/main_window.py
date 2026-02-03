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
        self.root.geometry("800x550")

        # App state
        self.resume_path = None
        self.jd_path = None

        self.build_ui()

    # ---------------- UI BUILD ---------------- #

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="Resume Analyzer",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)

        # Button section
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.resume_btn = tk.Button(
            btn_frame,
            text="Upload Resume",
            width=22,
            command=self.select_resume
        )
        self.resume_btn.grid(row=0, column=0, padx=10)

        self.jd_btn = tk.Button(
            btn_frame,
            text="Upload Job Description",
            width=22,
            command=self.select_jd
        )
        self.jd_btn.grid(row=0, column=1, padx=10)

        self.analyze_btn = tk.Button(
            self.root,
            text="Analyze",
            width=30,
            height=2,
            bg="#4CAF50",
            fg="white",
            command=self.analyze
        )
        self.analyze_btn.pack(pady=15)

        # Output area with scrollbar
        output_frame = tk.Frame(self.root)
        output_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(output_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output = tk.Text(
            output_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.output.yview)
        self.output.config(state=tk.DISABLED)

        # Status bar
        self.status = tk.Label(
            self.root,
            text="Ready",
            anchor="w"
        )
        self.status.pack(fill=tk.X, padx=8, pady=4)

    # ---------------- HELPERS ---------------- #

    def write_output(self, text: str):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.config(state=tk.DISABLED)

    def clear_output(self):
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.config(state=tk.DISABLED)

    # ---------------- ACTIONS ---------------- #

    def select_resume(self):
        path = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[("Resume Files", "*.pdf *.docx")]
        )
        if path:
            self.resume_path = path
            self.status.config(text="Resume selected")
            self.write_output(f"Selected resume:\n{path}\n\n")

    def select_jd(self):
        path = filedialog.askopenfilename(
            title="Select Job Description",
            filetypes=[("Text Files", "*.txt")]
        )
        if path:
            self.jd_path = path
            self.status.config(text="Job description selected")
            self.write_output(f"Selected job description:\n{path}\n\n")

    def analyze(self):
        self.clear_output()

        if not self.resume_path:
            self.write_output("Please upload a resume first.\n")
            self.status.config(text="Waiting for resume")
            return

        self.status.config(text="Analyzing...")

        # Parse resume
        if self.resume_path.lower().endswith(".pdf"):
            raw_resume = parse_pdf(self.resume_path)
        else:
            raw_resume = parse_docx(self.resume_path)

        cleaned_resume = clean_text(raw_resume)
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

            self.write_output("JD vs Resume Analysis\n")
            self.write_output("---------------------\n")
            self.write_output(f"JD Skills       : {result['jd_skills']}\n")
            self.write_output(f"Resume Skills  : {result['resume_skills']}\n")
            self.write_output(f"Missing Skills : {result['missing_skills']}\n")
            self.write_output(f"Score          : {result['score']['score']}%\n")

        # Resume-only mode
        else:
            found = extract_skills(cleaned_resume, skills)
            score = calculate_score(found, skills)

            self.write_output("Resume Analysis\n")
            self.write_output("---------------\n")
            self.write_output(f"Matched Skills : {found}\n")
            self.write_output(f"Score          : {score['score']}%\n")

        self.status.config(text="Analysis complete")


# ---------------- ENTRY ---------------- #

def launch_app():
    root = tk.Tk()
    ResumeAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_app()
