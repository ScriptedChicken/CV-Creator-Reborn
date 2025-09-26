import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from cv_creator.creator import Creator, Replacements
from cv_creator.seek_api import SeekApi


class CoverLetterCreatorGUI:
    def __init__(self, root, name="", template_path="", output_dir=""):
        self.root = root
        self.root.title("Cover Letter Creator")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        self.url_var = tk.StringVar()
        self.template_path_var = tk.StringVar(value=template_path)
        self.status_var = tk.StringVar(value="Ready")
        self.name_var = tk.StringVar(value=name)
        self.output_dir_var = tk.StringVar(value=output_dir)

        self.api = SeekApi()
        self.is_processing = False

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="Your name:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=50)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))

        ttk.Label(main_frame, text="Job URL:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))

        ttk.Label(main_frame, text="Template File:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        template_frame = ttk.Frame(main_frame)
        template_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        template_entry = ttk.Entry(
            template_frame, textvariable=self.template_path_var, width=40
        )
        template_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        template_entry.columnconfigure(0, weight=1)

        ttk.Button(template_frame, text="Browse", command=self.browse_template).grid(
            row=0, column=1, sticky=tk.E
        )

        ttk.Label(main_frame, text="Output directory:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        output_dir_entry = ttk.Entry(
            main_frame, textvariable=self.output_dir_var, width=50
        )
        output_dir_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))

        self.process_btn = ttk.Button(
            main_frame, text="Generate cover letter", command=self.start_processing
        )
        self.process_btn.grid(row=4, column=0, columnspan=2, pady=20)

        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=6, column=0, columnspan=2, pady=5)

        ttk.Label(main_frame, text="Processing Log:").grid(
            row=7, column=0, sticky=tk.W, pady=(20, 5)
        )

        text_frame = ttk.Frame(main_frame)
        text_frame.grid(
            row=8, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5
        )
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(text_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        main_frame.rowconfigure(8, weight=1)

    def browse_template(self):
        file_path = filedialog.askopenfilename(
            title="Select Template File",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")],
        )
        if file_path:
            self.template_path_var.set(file_path)

    def start_processing(self):
        if self.is_processing:
            return

        url = self.url_var.get().strip()
        template_path = self.template_path_var.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a job URL")
            return

        if not template_path:
            messagebox.showerror("Error", "Please select a template file")
            return

        self.is_processing = True
        self.process_btn.state(["disabled"])
        self.progress.start()
        self.status_var.set("Processing...")
        self.log_text.delete(1.0, tk.END)

        thread = threading.Thread(target=self.process_cv, args=(url, template_path))
        thread.daemon = True
        thread.start()

        self.check_thread_status(thread)

    def process_cv(self, url, template_path):
        try:
            self.log_message(f"Starting processing for URL: {url}")
            self.log_message(f"Using template: {template_path}")

            creator = Creator(template_path)
            results_count = 0

            for result in self.api.from_url(url):
                results_count += 1
                self.log_message(f"Processing result {results_count}...")

                replacements = Replacements.from_result(result)
                output_path = creator.run(
                    replacements=replacements,
                    description=result.description,
                    output_dir=self.output_dir_var.get(),
                    applicant_name=self.name_var.get(),
                )

                self.log_message(f"Created: {output_path}")

            self.log_message(
                f"Processing completed. {results_count} cover letter(s) generated."
            )
            self.status_var.set(f"Completed: {results_count} cover letter(s) generated")

        except Exception as e:
            error_msg = f"Error during processing: {str(e)}"
            self.log_message(error_msg)
            self.status_var.set("Error occurred")

            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))

        finally:
            self.is_processing = False
            self.root.after(0, self.processing_finished)

    def processing_finished(self):
        self.progress.stop()
        self.process_btn.state(["!disabled"])

    def check_thread_status(self, thread):
        if thread.is_alive():
            self.root.after(100, lambda: self.check_thread_status(thread))
        else:
            self.processing_finished()

    def log_message(self, message):
        def update_log():
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)

        self.root.after(0, update_log)


def main():
    root = tk.Tk()
    app = CoverLetterCreatorGUI(root)
    app.root.mainloop()


if __name__ == "__main__":
    main()
