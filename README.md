📘 Exam Generator – Flask Web Application

A Flask-based web application that automatically generates multiple randomized exam versions from uploaded text files (questions, choices, and answers) and packages them into a downloadable ZIP file.

🚀 Features

Upload questions, choices, and answers as text files

Generate multiple exam groups with:

Randomized question order

Randomized answer choices

Automatically produces:

Exam files for students

Answer keys for each group

Outputs everything as a ZIP file

Simple and clean web interface

🧠 How It Works

Upload:

questions.txt → one question per line

choices.txt → choices separated by blank lines

answers.txt → correct answers (number, letter, or full text)

Select the number of exam groups

The app:

Shuffles questions and options

Matches correct answers correctly after shuffling

Download a ZIP containing:

group_X_exam.txt

group_X_answers.txt

📂 Project Structure
proj_Bekir/
│
├── app.py
├── templates/
│   ├── index.html
│   └── card.html
├── uploads/
├── output/
├── static/
└── README.md

🛠️ Technologies Used

Python 3

Flask

HTML / CSS

Standard Python libraries:

os, random, uuid, zipfile, re

▶️ How to Run Locally
1. Install Flask
pip install flask

2. Run the app
python app.py

3. Open in browser
http://127.0.0.1:5000

🔐 Important Note (Sessions)

This app uses Flask flash messages, so a secret key is required:

app.secret_key = "your-secret-key"


(Replace with a secure value in production.)

📝 Input File Format
questions.txt
What is 2 + 2?
What is the capital of France?

choices.txt
A) 3
B) 4
C) 5

A) Berlin
B) Madrid
C) Paris

answers.txt
B
C


✔ Answers can be:

Letter (A, B, C…)

Number (1, 2, 3…)

Full answer text

📦 Output Example
group_1_exam.txt
group_1_answers.txt
group_2_exam.txt
group_2_answers.txt


All files are bundled into a single ZIP download.

👨‍💻 Author

Emir Fenina
Software Engineering Student
GitHub: https://github.com/amirf95

📄 License

This project is for educational use.
Feel free to modify and improve it.
