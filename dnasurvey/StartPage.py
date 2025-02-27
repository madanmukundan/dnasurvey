
import os
import customtkinter as ctk
from tkinterdnd2 import DND_FILES
import tkinter as tk
from tkinter import messagebox
import re

class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Title
        title_label = ctk.CTkLabel(self, text="Survey Application", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # Input fields container
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        # Name fields
        ctk.CTkLabel(input_frame, text="First Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ctk.CTkEntry(input_frame, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Last Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ctk.CTkEntry(input_frame, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Questions source
        questions_frame = ctk.CTkFrame(self)
        questions_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        questions_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(questions_frame, text="Questions Source:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.questions_path_var = tk.StringVar()
        self.questions_path_var.set(os.path.join(os.path.abspath("."), "Questions", "Questions.xlsx"))
        self.questions_path_entry = ctk.CTkEntry(questions_frame, textvariable=self.questions_path_var)
        self.questions_path_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Drag and drop capability
        self.questions_path_entry.drop_target_register(DND_FILES)
        self.questions_path_entry.dnd_bind('<<Drop>>', self.drop_questions_file)

        browse_questions_btn = ctk.CTkButton(questions_frame, text="Browse", command=self.browse_questions)
        browse_questions_btn.grid(row=0, column=2, padx=10, pady=5)

        # Randomize questions checkbox
        self.randomize_var = tk.BooleanVar(value=False)
        randomize_check = ctk.CTkCheckBox(questions_frame, text="Randomize Questions", variable=self.randomize_var)
        randomize_check.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        # Load existing responses
        responses_frame = ctk.CTkFrame(self)
        responses_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        responses_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(responses_frame, text="Load Responses:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.responses_path_var = tk.StringVar()
        self.responses_path_entry = ctk.CTkEntry(responses_frame, textvariable=self.responses_path_var)
        self.responses_path_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Drag and drop capability for responses
        self.responses_path_entry.drop_target_register(DND_FILES)
        self.responses_path_entry.dnd_bind('<<Drop>>', self.drop_responses_file)

        browse_responses_btn = ctk.CTkButton(responses_frame, text="Browse", command=self.browse_responses)
        browse_responses_btn.grid(row=0, column=2, padx=10, pady=5)

        # Buttons container
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.grid(row=4, column=0, padx=20, pady=(20, 20), sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Start survey button
        start_button = ctk.CTkButton(
            buttons_frame,
            text="Start Survey",
            command=self.start_survey,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        start_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Load and view responses button
        view_button = ctk.CTkButton(
            buttons_frame,
            text="View Loaded Responses",
            command=self.view_responses,
            fg_color="#2196F3",
            hover_color="#0b7dda"
        )
        view_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Exit button
        exit_button = ctk.CTkButton(
            buttons_frame,
            text="Exit",
            command=self.controller.quit,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        exit_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    def drop_questions_file(self, event):
        file_path = event.data

        # Clean up the file path (remove curly braces and quotes if present)
        file_path = re.sub(r'^{|}$|"', '', file_path)

        if file_path.lower().endswith('.xlsx'):
            self.questions_path_var.set(file_path)
        else:
            messagebox.showerror("Error", "Please drag an Excel file (.xlsx)")

    def drop_responses_file(self, event):
        file_path = event.data

        # Clean up the file path (remove curly braces and quotes if present)
        file_path = re.sub(r'^{|}$|"', '', file_path)

        if file_path.lower().endswith('.xlsx'):
            self.responses_path_var.set(file_path)
        else:
            messagebox.showerror("Error", "Please drag an Excel file (.xlsx)")

    def browse_questions(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.questions_path_var.set(file_path)

    def browse_responses(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.responses_path_var.set(file_path)

    def start_survey(self):
        # Validate first and last name
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()

        if not first_name or not last_name:
            messagebox.showerror("Error", "Please enter your first and last name")
            return

        # Save first and last name to controller
        self.controller.first_name = first_name
        self.controller.last_name = last_name

        # Load questions
        questions_path = self.questions_path_var.get()
        if not questions_path:
            messagebox.showerror("Error", "Please select a questions file")
            return

        # Load questions with randomization option
        success = self.controller.load_questions(questions_path, self.randomize_var.get())
        if success:
            self.controller.show_frame("QuestionPage")

    def view_responses(self):
        responses_path = self.responses_path_var.get()
        if not responses_path:
            messagebox.showerror("Error", "Please select a responses file")
            return

        success = self.controller.load_responses(responses_path)
        if success:
            self.controller.show_frame("ViewResponsesPage")

    def reset_fields(self):
        # Update the first and last name fields with current values
        self.first_name_var.set(self.controller.first_name)
        self.last_name_var.set(self.controller.last_name)

        # Update the questions path if it exists
        if self.controller.questions_path:
            self.questions_path_var.set(self.controller.questions_path)

        # Update the responses path if it exists
        if self.controller.response_path:
            self.responses_path_var.set(self.controller.response_path)

    def __str__(self):
        return "StartPage"
