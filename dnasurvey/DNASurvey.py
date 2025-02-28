import os
import random
import pandas as pd
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
from tkinter import messagebox
from StartPage import StartPage
from QuestionPage import QuestionPage
from ThankYouPage import ThankYouPage
from ViewResponsesPage import ViewResponsesPage

class DNASurveyApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        
        # Set up the main window
        self.title("Survey Application")
        self.geometry("1010x460")
        self.minsize(600, 400)
        
        # Set the theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Initialize variables
        self.questions_path = None
        self.questions_df = None
        self.responses_df = None
        self.current_question_index = 0
        self.total_questions = 0
        self.randomized_order = []
        self.original_order = []
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.phone = ""
        self.patient = ""
        self.response_path = None
        
        # Create Responses directory if it doesn't exist
        if not os.path.exists("Responses"):
            os.makedirs("Responses")
        
        # Initialize frame container
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        # Create frames
        self.frames = {}
        for F in (StartPage, QuestionPage, ThankYouPage, ViewResponsesPage):
            frame = F(self.container, self)
            self.frames[str(frame)] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            # frame.pack(side="bottom", padx=10)

        # Status bar at bottom
        status_frame = ctk.CTkFrame(self.container, height=30)
        # status_frame.pack(side="bottom", fill="x", pady=10)
        status_frame.grid(row=1, column=0, sticky="nsew")

        status_frame.grid_columnconfigure(0,weight=1)
        status_frame.grid_columnconfigure(1,weight=0)
        
        self.status_label = ctk.CTkLabel(status_frame, text="Ready", anchor="w")
        # self.status_label.pack(side="left", padx=10)
        self.status_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        version_label = ctk.CTkLabel(status_frame, text="v1.01", anchor="e")
        # version_label.pack(side="right", padx=10)
        version_label.grid(row=1, column=1, padx=15, pady=5, sticky="e")
        
        # Show the start page
        self.show_frame("StartPage")
    
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        if page == "StartPage":
            self.status_label.configure(text="Ready")
            self.frames["StartPage"].reset_fields()
        elif page == "QuestionPage":
            self.frames["QuestionPage"].update_question()
        elif page == "ThankYouPage":
            self.status_label.configure(text="Thank You!")
            self.frames["ThankYouPage"].update_info()
        elif page == "ViewResponsesPage":
            self.status_label.configure(text="Viewing Responses...")
            self.frames["ViewResponsesPage"].update_responses()

    
    def load_questions(self, file_path, randomize=False):
        self.status_label.configure(text="Loading questions...")

        try: 
            df = pd.read_excel(file_path, usecols=["Questions"]).dropna()
            
            self.questions_df = df
            self.questions_path = file_path
            self.total_questions = len(self.questions_df)

            # Initialize responses dataframe
            if self.responses_df is None:
                self.responses_df = pd.DataFrame(
                    {
                        'Questions': self.questions_df["Questions"].tolist(),
                        'Responses': ['<missing>'] * self.total_questions
                    }
                )

            self.current_question_index = 0
        
            # Create original order
            self.original_order = list(range(self.total_questions))
            
            # Create randomized order if requested
            if randomize:
                self.randomized_order = list(range(self.total_questions))
                random.shuffle(self.randomized_order)
            else:
                self.randomized_order = self.original_order.copy()
            
            self.status_label.configure(text="Questions loaded.")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {str(e)}")
            return False
     
    def randomize_questions(self, randomize=False):
        # Create original order
            self.original_order = list(range(self.total_questions))
            
            # Create randomized order if requested
            if randomize:
                self.randomized_order = list(range(self.total_questions))
                answered_questions = self.responses_df.index[self.responses_df["Responses"]!='<missing>'].to_list()
                self.randomized_order = self.responses_df.index[self.responses_df["Responses"]=='<missing>'].to_list()
                random.shuffle(self.randomized_order)
                self.current_question_index = len(answered_questions)
                self.randomized_order = [*answered_questions, *self.randomized_order]
            else:
                self.randomized_order = self.original_order.copy()
                self.current_question_index = self.responses_df.index[self.responses_df["Responses"]=='<missing>'][0].astype(int)

    def load_responses(self, file_path):
        self.status_label.configure(text="Loading responses...")

        try:
            self.response_path = file_path
            loaded_responses = pd.read_excel(file_path)
            
            self.first_name = loaded_responses['First Name'].iloc[0]
            self.last_name = loaded_responses['Last Name'].iloc[0]
            self.email = loaded_responses['Email'].iloc[0]
            self.phone = loaded_responses['Phone Number'].iloc[0]
            self.patient = loaded_responses['Patient Number'].iloc[0]
            loaded_responses = loaded_responses.drop(['First Name', 'Last Name','Email','Phone Number','Patient Number'], axis=1)
            
            # Update the responses DataFrame
            self.responses_df = loaded_responses
            
            self.status_label.configure(text="Responses loaded.")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load responses: {str(e)}")
            return False
    
    def save_responses(self):
        if self.responses_df is None:
            messagebox.showerror("Error", "No responses to save")
            return False
        
        try:
            # Create a copy with first and last name
            save_df = self.responses_df.copy()
            
            # Add first and last name to the DataFrame
            save_df.insert(0, 'Last Name', self.last_name)
            save_df.insert(0, 'First Name', self.first_name)
            save_df.insert(0, 'Patient Number', self.patient)
            save_df.insert(0, 'Phone Number', self.phone)
            save_df.insert(0, 'Email', self.email)
            
            # Determine file path
            file_name = f"{self.first_name}_{self.last_name}_{self.patient}_responses.xlsx"
            file_path = os.path.join("Responses", file_name)
            
            # Save to file
            save_df.to_excel(file_path, index=False)
            self.response_path = file_path
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save responses: {str(e)}")
            return False
    
    def reset(self):
        self.questions_path = None
        self.questions_df = None
        self.responses_df = None
        self.current_question_index = 0
        self.total_questions = 0
        self.randomized_order = []
        self.original_order = []
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.phone = ""
        self.patient = ""
        self.response_path = None
        self.status_label.configure(text="Ready")
        self.show_frame("StartPage")

    def next_question(self, response=None):
        # Save the current response if provided
        if response is not None:
            # Map to original index
            original_index = self.randomized_order[self.current_question_index]
            self.responses_df.loc[original_index, 'Responses'] = response
        
        # Move to the next question
        self.current_question_index += 1
        
        # If we've gone through all questions, go to thank you page
        if self.current_question_index >= self.total_questions:
            self.show_frame("ThankYouPage")
        else:
            self.frames["QuestionPage"].update_question()
    
    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.frames["QuestionPage"].update_question()

    def __str__(self):
        return "DNASurveyApp"


def main():
    app = DNASurveyApp()
    app.mainloop()


if __name__ == "__main__":
    main()
