import customtkinter as ctk

class ThankYouPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Thank you message
        title_label = ctk.CTkLabel(
            self,
            text="Thank You!",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(40, 10), sticky="ew")

        self.message_label = ctk.CTkLabel(
            self,
            text="Your responses have been recorded.",
            font=ctk.CTkFont(size=16)
        )
        self.message_label.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Buttons container
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.grid(row=2, column=0, padx=20, pady=(20, 20), sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # View responses button
        view_responses_button = ctk.CTkButton(
            buttons_frame,
            text="View Responses",
            command=lambda: controller.show_frame("ViewResponsesPage"),
            fg_color="#2196F3",
            hover_color="#0b7dda"
        )
        view_responses_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Start new survey button
        new_survey_button = ctk.CTkButton(
            buttons_frame,
            text="Start New Survey",
            command=lambda: controller.show_frame("StartPage"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        new_survey_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Exit button
        exit_button = ctk.CTkButton(
            buttons_frame,
            text="Exit",
            command=self.controller.quit,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        exit_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    def update_info(self):
        # Save final responses
        success = self.controller.save_responses()
        if success:
            self.message_label.configure(
                text=f"Thank you, {self.controller.first_name} {self.controller.last_name}! "
                     f"Your responses have been saved."
            )
        else:
            self.message_label.configure(
                text=f"Thank you, {self.controller.first_name} {self.controller.last_name}! "
                     f"There was an issue saving your responses."
            )
    def __str__(self):
        return "ThankYouPage"
