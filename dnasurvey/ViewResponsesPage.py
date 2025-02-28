import customtkinter as ctk

class ViewResponsesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Survey Responses",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # User info
        self.info_label = ctk.CTkLabel(
            self,
            text="Responses for: ",
            font=ctk.CTkFont(size=16)
        )
        self.info_label.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Responses display (scrollable)
        self.responses_container = ctk.CTkFrame(self)
        self.responses_container.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.responses_container.grid_columnconfigure(0, weight=1)
        self.responses_container.grid_rowconfigure(0, weight=1)

        # Create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.responses_container)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Buttons container
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.grid(row=3, column=0, padx=20, pady=(20, 20), sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        # Back to main menu button
        main_menu_button = ctk.CTkButton(
            buttons_frame,
            text="Main Menu",
            command=lambda: controller.show_frame("StartPage"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        main_menu_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Exit button
        exit_button = ctk.CTkButton(
            buttons_frame,
            text="Exit",
            command=self.controller.quit,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        exit_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Call the update method
        self.tkraise()
        self.update_responses()

    def update_responses(self):
        # Update user info
        self.info_label.configure(
            text=f"Responses for: {self.controller.first_name} {self.controller.last_name}"
        )

        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Check if we have responses
        if self.controller.responses_df is None:
            no_data_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No response data available",
                font=ctk.CTkFont(size=16)
            )
            no_data_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            return

        # Drop missing
        responses_df = self.controller.responses_df[~self.controller.responses_df["Responses"].str.contains("missing")]

        # Create headers
        headers_frame = ctk.CTkFrame(self.scrollable_frame)
        headers_frame.grid(row=0, column=0, padx=5, pady=(5, 10), sticky="ew")
        headers_frame.grid_columnconfigure(0, weight=3)
        headers_frame.grid_columnconfigure(1, weight=1)

        question_header = ctk.CTkLabel(
            headers_frame,
            text="Question",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        question_header.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        response_header = ctk.CTkLabel(
            headers_frame,
            text="Response",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        response_header.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Display each question and response
        for i, (_, row) in enumerate(responses_df.iterrows()):
            row_frame = ctk.CTkFrame(self.scrollable_frame)
            row_frame.grid(row=i+1, column=0, padx=5, pady=0, sticky="ew")
            row_frame.grid_columnconfigure(0, weight=3)
            row_frame.grid_columnconfigure(1, weight=1)

            # Question text
            question_label = ctk.CTkLabel(
                row_frame,
                text=row['Questions'],
                wraplength=450,
                justify="left",
                font=ctk.CTkFont(size=12)
            )
            question_label.grid(row=0, column=0, padx=5, pady=0, sticky="w")

            # Convert response to descriptive text
            response_text = row['Responses']
            if response_text == '1':
                response_text = "1 - Strongly Agree with Left"
            elif response_text == '2':
                response_text = "2 - Agree with Left"
            elif response_text == '3':
                response_text = "3 - Neutral"
            elif response_text == '4':
                response_text = "4 - Agree with Right"
            elif response_text == '5':
                response_text = "5 - Strongly Agree with Right"

            # Response text
            response_label = ctk.CTkLabel(row_frame,
                text=response_text,
                font=ctk.CTkFont(weight="bold"),
                justify="right"
            )
            response_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    def __str__(self):
        return "ViewResponsesPage"
