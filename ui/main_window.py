import tkinter as tk
from tkinter import filedialog


class ResumeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Analyzer")
        self.root.geometry("700x500")

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
            width=20
        )
        self.resume_btn.grid(row=0, column=0, padx=10)

        self.jd_btn = tk.Button(
            btn_frame,
            text="Upload Job Description",
            width=20
        )
        self.jd_btn.grid(row=0, column=1, padx=10)

        self.analyze_btn = tk.Button(
            self.root,
            text="Analyze",
            width=30,
            height=2
        )
        self.analyze_btn.pack(pady=15)

        self.output = tk.Text(
            self.root,
            height=15,
            width=80
        )
        self.output.pack(pady=10)


def launch_app():
    root = tk.Tk()
    ResumeAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_app()
