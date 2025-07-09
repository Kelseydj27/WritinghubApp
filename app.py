import os
from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import datetime
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'doc', 'docx'}

# TODO: Configure these securely, e.g., via environment variables
SENDER_EMAIL = "YOUR_GMAIL_SENDER_ADDRESS@gmail.com"  # Replace with your Gmail address
SENDER_PASSWORD = "YOUR_GMAIL_APP_PASSWORD"      # Replace with your Gmail App Password
RECIPIENT_EMAIL = "obakengmathibe3@gmail.com"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24) # For flashing messages
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit for uploads

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_submission_email(user_details, attachment_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"New Writing Hub Submission: {user_details.get('subject', 'N/A')} by {user_details.get('name', 'N/A')}"

        body = f"""
        New Writing Hub Submission:

        Name: {user_details.get('name', 'N/A')}
        Student Number: {user_details.get('student_number', 'N/A')}
        Faculty: {user_details.get('faculty', 'N/A')}
        Subject: {user_details.get('subject', 'N/A')}
        Original Filename: {user_details.get('original_filename', 'N/A')}

        The document is attached.
        """
        msg.attach(MIMEText(body, 'plain'))

        # Attach the file
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f"attachment; filename= {os.path.basename(attachment_path)}",
        )
        msg.attach(part)

        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Secure the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
        server.quit()
        print(f"Email sent successfully to {RECIPIENT_EMAIL}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        # You might want to log this error more formally
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'document' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['document']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Sanitize filename and make it unique
            original_filename = secure_filename(file.filename)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            unique_id = uuid.uuid4().hex[:6]
            # new_filename = f"{timestamp}_{unique_id}_{original_filename}" # This might be too long
            base, ext = os.path.splitext(original_filename)
            new_filename = f"{base}_{timestamp}_{unique_id}{ext}"


            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            try:
                file.save(file_path)
            except Exception as e:
                print(f"Error saving file: {e}") # Log for admin
                flash("An error occurred while saving the file. Please try again or contact support.")
                return redirect(request.url)


            # Get other form data
            name = request.form.get('name')
            subject = request.form.get('subject')
            faculty = request.form.get('faculty')
            student_number = request.form.get('student_number')

            # Placeholder for email sending logic
            print(f"File saved: {new_filename}")
            print(f"Name: {name}, Subject: {subject}, Faculty: {faculty}, Student Number: {student_number}")

            user_details = {
                "name": name,
                "subject": subject,
                "faculty": faculty,
                "student_number": student_number,
                "original_filename": original_filename
            }
            
            email_sent = send_submission_email(user_details, file_path)

            if email_sent:
                flash(f"File '{original_filename}' uploaded successfully by {name} and submission email sent.")
            else:
                flash(f"File '{original_filename}' uploaded successfully by {name}, but there was an error sending the submission email. Please contact support.")

            return redirect(url_for('success_page'))
        else:
            flash('Allowed file types are .doc, .docx')
            return redirect(request.url)
    return redirect(url_for('index')) # Should not happen with POST only route

@app.route('/success')
def success_page():
    return render_template('success.html')

# Placeholder for admin panel - will be developed in a later step
@app.route('/admin/panel')
def admin_panel():
    submissions = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename == '.gitkeep': # Skip .gitkeep if present
                continue
            
            parts = filename.split('_')
            original_filename_parts = []
            timestamp_str = "N/A"
            
            # Attempt to parse filename: originalbase_timestamp_uuid.ext
            # This is a bit naive and depends on filenames not having underscores
            # or being structured exactly as saved.
            if len(parts) >= 3: # expecting at least base_timestamp_uuid.ext
                try:
                    # Last part is uuid.ext, second to last is timestamp
                    timestamp_str = parts[-2]
                    # Reconstruct original filename, excluding timestamp and uuid
                    original_filename_parts = parts[:-2]
                    
                    # Handle extension correctly
                    base_name_with_uuid = "_".join(original_filename_parts)
                    # The last part of original_filename_parts might actually be part of the uuid if original name had no underscores
                    # This parsing is tricky. Let's try a simpler approach for original name:
                    # Remove timestamp and uuid.ext
                    
                    # Simpler parsing:
                    # filename: some_original_name_YYYYMMDDHHMMSS_uuid.ext
                    # We want "some_original_name.ext"
                    
                    # Get the extension
                    name_without_ext, ext = os.path.splitext(filename)
                    
                    # Split by underscore
                    name_parts = name_without_ext.split('_')

                    if len(name_parts) >= 3: # base_timestamp_uuid
                        original_base = "_".join(name_parts[:-2])
                        timestamp_str = name_parts[-2]
                        # uuid_part = name_parts[-1] # not used in display
                        parsed_original_filename = original_base + ext
                    else: # Could not parse as expected
                        parsed_original_filename = "N/A (cannot parse original)"

                    # Format timestamp for display if it's valid
                    try:
                        dt_obj = datetime.datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
                        display_timestamp = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        display_timestamp = timestamp_str # Show raw if not parsable
                        
                except IndexError:
                    parsed_original_filename = "N/A (parse error)"
                    display_timestamp = "N/A"
            else:
                # If filename doesn't match expected pattern, show raw filename
                parsed_original_filename = filename 
                display_timestamp = "N/A"

            submissions.append({
                'saved_filename': filename,
                'original_filename': parsed_original_filename,
                'timestamp': display_timestamp,
            })
        
        # Sort by timestamp, most recent first (if timestamp is parsable)
        # This sort is a bit naive if timestamps are "N/A"
        submissions.sort(key=lambda s: s['timestamp'], reverse=True)

    return render_template('admin.html', submissions=submissions)

# Route to serve uploaded files for the admin panel (and potentially other uses)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
