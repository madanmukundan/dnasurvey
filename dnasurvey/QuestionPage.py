import pandas as pd
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class QuestionPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create variables for the response
        self.response_var = tk.StringVar()

        # Create main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header with progress info
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)

        self.progress_label = ctk.CTkLabel(
            self.header_frame,
            text="Question 0 of 0",
            font=ctk.CTkFont(size=16)
        )
        self.progress_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Save progress button
        self.save_button = ctk.CTkButton(
            self.header_frame,
            text="Save Progress",
            command=self.save_progress,
            fg_color="#FFA500",
            hover_color="#FF8C00"
        )
        self.save_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # Question content
        self.question_frame = ctk.CTkFrame(self)
        self.question_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.question_frame.grid_columnconfigure(0, weight=1)

        self.question_label = ctk.CTkLabel(
            self.question_frame,
            text="Question will appear here",
            font=ctk.CTkFont(size=18, weight="bold"),
            wraplength=700
        )
        self.question_label.grid(row=0, column=0, padx=20, pady=(20, 30), sticky="ew")

        # Response options
        self.options_frame = ctk.CTkFrame(self.question_frame, fg_color="transparent")
        self.options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.options_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Response buttons
        responses = [
            ("Strongly Agree with Left", "1"),
            ("Agree with Left", "2"),
            ("Neutral", "3"),
            ("Agree with Right", "4"),
            ("Strongly Agree with Right", "5")
        ]

        for i, (text, value) in enumerate(responses):
            option = ctk.CTkRadioButton(
                self.options_frame,
                text=text,
                value=value,
                variable=self.response_var,
                font=ctk.CTkFont(size=14)
            )
            option.grid(row=0, column=i, padx=10, pady=20, sticky="ew")

        # Navigation buttons
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.grid(row=2, column=0, padx=20, pady=(20, 20), sticky="ew")
        self.nav_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.prev_button = ctk.CTkButton(
            self.nav_frame,
            text="Previous",
            command=self.prev_question,
            fg_color="#757575",
            hover_color="#616161"
        )
        self.prev_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.main_menu_button = ctk.CTkButton(
            self.nav_frame,
            text="Main Menu",
            command=lambda: controller.show_frame("StartPage"),
            fg_color="#607D8B",
            hover_color="#455A64"
        )
        self.main_menu_button.grid(row=0, column=1, padx=10, pady=10)

        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Next",
            command=self.next_question,
            fg_color="#2196F3",
            hover_color="#0b7dda"
        )
        self.next_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    def update_question(self):

        if self.controller.questions_df is None:
            return

        # Get current question index (using randomized order)
        current_idx = self.controller.current_question_index
        total = self.controller.total_questions

        # Map to original index using randomized order
        original_idx = self.controller.randomized_order[current_idx]

        self.controller.status_label.configure(text=f"Question ID #{original_idx + 1}")

        # Update progress label
        self.progress_label.configure(text=f"Question {current_idx + 1} of {total}")

        # Update question text
        question_text = self.controller.questions_df.iloc[original_idx, 0]
        self.question_label.configure(text=question_text)

        # Update response button selection
        current_response = self.controller.responses_df.loc[original_idx, 'Response']
        if current_response != '<missing>':
            self.response_var.set(current_response)
        else:
            self.response_var.set("<missing>")

        # Update button states
        self.prev_button.configure(state="normal" if current_idx > 0 else "disabled")

    def next_question(self):
        response = self.response_var.get()
        self.controller.next_question(response)

    def prev_question(self):
        response = self.response_var.get()

        # Save current response before going back
        if response:
            original_index = self.controller.randomized_order[self.controller.current_question_index]
            self.controller.responses_df.loc[original_index, 'Response'] = response

        self.controller.prev_question()

    def save_progress(self):
        response = self.response_var.get()

        # Save current response before saving progress
        if response:
            original_index = self.controller.randomized_order[self.controller.current_question_index]
            self.controller.responses_df.loc[original_index, 'Response'] = response

        success = self.controller.save_responses()
        if success:
            messagebox.showinfo("Success", "Progress saved successfully")

    def __str__(self):
        return "QuestionPage"
