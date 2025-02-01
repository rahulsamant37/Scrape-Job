from agents import JobSuggestionAgent

def main():
    agent = JobSuggestionAgent(csv_path='careerjet_all_jobs_20250110_162215.csv')
    while True:
        user_input = input("Enter your query or 'upload' to upload a PDF: ")
        if user_input.lower() == 'upload':
            pdf_path = input("Enter the path to your PDF: ")
            suggestions = agent.perform_ocr_and_suggest_jobs(pdf_path)
        else:
            suggestions = agent.suggest_jobs(user_input)
        print("Job Suggestions:")
        for suggestion in suggestions:
            print(suggestion)

if __name__ == "__main__":
    main()