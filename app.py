#bekir
#main app upload flask framework python
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
#to modify user viex 
import os, random, uuid, io, zipfile, re
# Replace with a secure random key in production



app = Flask(__name__)
app.secret_key = "BekirSecretKey12345"  #bekir
# which folers to upload files and output files
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
# check if the folder exists, if not create it
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------- Functions ----------
# normalize text to make all letters lowercase and delete extra spaces      
def normalize_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())

# Function to delete the labels of choices like A. B) C: etc.
def strip_choice_label(line: str) -> str:
    return re.sub(r'^[A-Za-z]\s*[\.\)\-\:]\s*', '', line).strip()

# Function to ignore empty lines
def parse_text_lines(path):
    return [line.rstrip("\n") for line in open(path, encoding="utf-8").read().splitlines() if line.strip() != ""]

# Function to parse choices blocks separated by double new lines
def parse_choices_blocks(path):
    raw = open(path, encoding="utf-8").read().strip()
    if raw == "":
        return []
    blocks = [b for b in raw.split("\n\n") if b.strip() != ""]
    parsed = []
    for block in blocks:
        lines = [l for l in block.splitlines() if l.strip() != ""]
        cleaned = [strip_choice_label(l) for l in lines]
        parsed.append(cleaned)
    return parsed

# ---------- Routes ----------
#for frontend
 #GET and POST methods
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")#RENDER HTML MAIN COMPONENT

    # ensure files present
    if "q" not in request.files or "c" not in request.files or "a" not in request.files:
        flash("Please upload questions, choices and answers files.", "error")
        return redirect(url_for("index"))

    try:
        q_file = request.files["q"]#questions file
        c_file = request.files["c"]#choices file
        a_file = request.files["a"]#answers file
            #number of groups
        groups = int(request.form.get("g", 2))
    except Exception:
        flash("Missing files or invalid group number.", "error")#eneterd wrong input 
        return redirect(url_for("index"))
    #print avreything is ok
    flash("uploads received.", "success")
    # save uploads
    #------------Saving-------------
    run_id = uuid.uuid4().hex[:8]
    q_name = f"{run_id}_{secure_filename(q_file.filename)}"
    c_name = f"{run_id}_{secure_filename(c_file.filename)}"
    a_name = f"{run_id}_{secure_filename(a_file.filename)}"

    q_path = os.path.join(UPLOAD_FOLDER, q_name)
    c_path = os.path.join(UPLOAD_FOLDER, c_name)
    a_path = os.path.join(UPLOAD_FOLDER, a_name)

    q_file.save(q_path)
    c_file.save(c_path)
    a_file.save(a_path)

    # parse inputs
    questions = parse_text_lines(q_path)
    choices_blocks = parse_choices_blocks(c_path)
    answers = parse_text_lines(a_path)

#----------Main Functionality----------
# validate input lengths
    if not (len(questions) == len(choices_blocks) == len(answers)):
        flash(f"Input length mismatch: questions={len(questions)}, choices={len(choices_blocks)}, answers={len(answers)}", "error")
        return redirect(url_for("index"))

    # generate and package as zip to user to download
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        # PER-GROUP loop: everything for one group happens inside this loop
        for g in range(1, groups + 1):
            q_order = list(range(len(questions)))
            random.shuffle(q_order)

            exam_lines = []
            key_lines = []

            # per-question in group
            for out_i, q_idx in enumerate(q_order, start=1):
                q_text = questions[q_idx]
                exam_lines.append(f"{out_i}. {q_text}")

                original_opts = choices_blocks[q_idx]  # stripped labels
                opts = original_opts.copy()
                random.shuffle(opts)

                # write options with fresh labels
                for j, opt_text in enumerate(opts):
                    label = chr(ord('A') + j)
                    exam_lines.append(f"   {label}) {opt_text}")
                exam_lines.append("")

                # resolve correct answer (index, letter or text)
                ans_raw = answers[q_idx].strip()
                found_label = None

                # 1) numeric index (1-based)
                if re.fullmatch(r"\d+", ans_raw):
                    try:
                        orig_index = int(ans_raw) - 1
                        if 0 <= orig_index < len(original_opts):
                            target = normalize_text(original_opts[orig_index])
                            for j, opt_text in enumerate(opts):
                                if normalize_text(opt_text) == target:
                                    found_label = chr(ord('A') + j)
                                    break
                    except Exception:
                        found_label = None

                # 2) letter (A/B/C)
                if found_label is None and re.fullmatch(r"[A-Za-z]", ans_raw):
                    letter_index = ord(ans_raw.upper()) - ord('A')
                    if 0 <= letter_index < len(original_opts):
                        target = normalize_text(original_opts[letter_index])
                        for j, opt_text in enumerate(opts):
                            if normalize_text(opt_text) == target:
                                found_label = chr(ord('A') + j)
                                break

                # 3) full text fallback
                if found_label is None:
                    target = normalize_text(ans_raw)
                    for j, opt_text in enumerate(opts):
                        if normalize_text(opt_text) == target:
                            found_label = chr(ord('A') + j)
                            break

                key_lines.append(f"{out_i}. {found_label if found_label else 'UNKNOWN'}")

            # write this group's files into the zip
            zf.writestr(f"group_{g}_exam.txt", "\n".join(exam_lines))
            zf.writestr(f"group_{g}_answers.txt", "\n".join(key_lines))
        flash("Exam generation complete.", "success")
    zip_buffer.seek(0)
    
    return send_file(zip_buffer, mimetype="application/zip", download_name=f"exams_{run_id}.zip", as_attachment=True)

#route for card component IN THE FRONTEND
@app.route("/card")
def card():
    return render_template("card.html")

#deleted doont run
#@app.route("/success")
# def success():
#     return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)#leave this line debuuging internal problem 
    #dont touch 

# which folers to upload files and output files
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
# check if the folder exists, if not create it
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------- Functions ----------
# normalize text to make all letters lowercase and delete extra spaces      
def normalize_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())

# Function to delete the labels of choices like A. B) C: etc.
def strip_choice_label(line: str) -> str:
    return re.sub(r'^[A-Za-z]\s*[\.\)\-\:]\s*', '', line).strip()

# Function to ignore empty lines
def parse_text_lines(path):
    return [line.rstrip("\n") for line in open(path, encoding="utf-8").read().splitlines() if line.strip() != ""]

# Function to parse choices blocks separated by double new lines
def parse_choices_blocks(path):
    raw = open(path, encoding="utf-8").read().strip()
    if raw == "":
        return []
    blocks = [b for b in raw.split("\n\n") if b.strip() != ""]
    parsed = []
    for block in blocks:
        lines = [l for l in block.splitlines() if l.strip() != ""]
        cleaned = [strip_choice_label(l) for l in lines]
        parsed.append(cleaned)
    return parsed

# ---------- Routes ----------
#for frontend
 #GET and POST methods
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")#RENDER HTML MAIN COMPONENT

    # ensure files present
    if "q" not in request.files or "c" not in request.files or "a" not in request.files:
        flash("Please upload questions, choices and answers files.", "error")
        return redirect(url_for("index"))

    try:
        q_file = request.files["q"]#questions file
        c_file = request.files["c"]#choices file
        a_file = request.files["a"]#answers file
            #number of groups
        groups = int(request.form.get("g", 2))
    except Exception:
        flash("Missing files or invalid group number.", "error")#eneterd wrong input 
        return redirect(url_for("index"))
    #print avreything is ok
    flash("uploads received.", "success")
    # save uploads
    #------------Saving-------------
    run_id = uuid.uuid4().hex[:8]
    q_name = f"{run_id}_{secure_filename(q_file.filename)}"
    c_name = f"{run_id}_{secure_filename(c_file.filename)}"
    a_name = f"{run_id}_{secure_filename(a_file.filename)}"

    q_path = os.path.join(UPLOAD_FOLDER, q_name)
    c_path = os.path.join(UPLOAD_FOLDER, c_name)
    a_path = os.path.join(UPLOAD_FOLDER, a_name)

    q_file.save(q_path)
    c_file.save(c_path)
    a_file.save(a_path)

    # parse inputs
    questions = parse_text_lines(q_path)
    choices_blocks = parse_choices_blocks(c_path)
    answers = parse_text_lines(a_path)

#----------Main Functionality----------
# validate input lengths
    if not (len(questions) == len(choices_blocks) == len(answers)):
        flash(f"Input length mismatch: questions={len(questions)}, choices={len(choices_blocks)}, answers={len(answers)}", "error")
        return redirect(url_for("index"))

    # generate and package as zip to user to download
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        # PER-GROUP loop: everything for one group happens inside this loop
        for g in range(1, groups + 1):
            q_order = list(range(len(questions)))
            random.shuffle(q_order)

            exam_lines = []
            key_lines = []

            # per-question in group
            for out_i, q_idx in enumerate(q_order, start=1):
                q_text = questions[q_idx]
                exam_lines.append(f"{out_i}. {q_text}")

                original_opts = choices_blocks[q_idx]  # stripped labels
                opts = original_opts.copy()
                random.shuffle(opts)

                # write options with fresh labels
                for j, opt_text in enumerate(opts):
                    label = chr(ord('A') + j)
                    exam_lines.append(f"   {label}) {opt_text}")
                exam_lines.append("")

                # resolve correct answer (index, letter or text)
                ans_raw = answers[q_idx].strip()
                found_label = None

                # 1) numeric index (1-based)
                if re.fullmatch(r"\d+", ans_raw):
                    try:
                        orig_index = int(ans_raw) - 1
                        if 0 <= orig_index < len(original_opts):
                            target = normalize_text(original_opts[orig_index])
                            for j, opt_text in enumerate(opts):
                                if normalize_text(opt_text) == target:
                                    found_label = chr(ord('A') + j)
                                    break
                    except Exception:
                        found_label = None

                # 2) letter (A/B/C)
                if found_label is None and re.fullmatch(r"[A-Za-z]", ans_raw):
                    letter_index = ord(ans_raw.upper()) - ord('A')
                    if 0 <= letter_index < len(original_opts):
                        target = normalize_text(original_opts[letter_index])
                        for j, opt_text in enumerate(opts):
                            if normalize_text(opt_text) == target:
                                found_label = chr(ord('A') + j)
                                break

                # 3) full text fallback
                if found_label is None:
                    target = normalize_text(ans_raw)
                    for j, opt_text in enumerate(opts):
                        if normalize_text(opt_text) == target:
                            found_label = chr(ord('A') + j)
                            break

                key_lines.append(f"{out_i}. {found_label if found_label else 'UNKNOWN'}")

            # write this group's files into the zip
            zf.writestr(f"group_{g}_exam.txt", "\n".join(exam_lines))
            zf.writestr(f"group_{g}_answers.txt", "\n".join(key_lines))
        flash("Exam generation complete.", "success")
    zip_buffer.seek(0)
    
    return send_file(zip_buffer, mimetype="application/zip", download_name=f"exams_{run_id}.zip", as_attachment=True)

#route for card component IN THE FRONTEND
@app.route("/card")
def card():
    return render_template("card.html")

#deleted doont run
#@app.route("/success")
# def success():
#     return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)#leave this line debuuging internal problem 
    #dont touch 
