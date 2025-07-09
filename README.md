# Eduvos Mbombela - Writing Hub Submission Portal

This Flask web application provides a portal for students to submit documents for the Writing Hub. Submissions are saved to the server, and an email notification with the student's details and the submitted document is sent to a designated email address. An admin panel is available to view all submissions.

## Setup Instructions

1.  **Environment Setup:**
    *   It's highly recommended to use a Python virtual environment to manage dependencies.
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        ```

2.  **Install Dependencies:**
    *   Ensure you have Python 3.6+ and pip installed.
    *   Install the required packages:
        ```bash
        pip install -r requirements.txt
        ```

## Configuration

The primary configuration you need to perform is for sending emails via Gmail.

**Email Sending Configuration (in `app.py`):**

Open the `app.py` file and locate the following lines:

```python
# TODO: Configure these securely, e.g., via environment variables
SENDER_EMAIL = "YOUR_GMAIL_SENDER_ADDRESS@gmail.com"  # Replace with your Gmail address
SENDER_PASSWORD = "YOUR_GMAIL_APP_PASSWORD"      # Replace with your Gmail App Password
RECIPIENT_EMAIL = "obakengmathibe3@gmail.com" # This is pre-configured
```

1.  **`SENDER_EMAIL`**:
    *   Replace `"YOUR_GMAIL_SENDER_ADDRESS@gmail.com"` with the Gmail address you want to use to send the submission emails.

2.  **`SENDER_PASSWORD`**:
    *   **Important:** It is strongly recommended to use an **App Password** instead of your regular Gmail password, especially if you have 2-Step Verification enabled on your Google account.
    *   **How to Generate an App Password for Gmail:**
        1.  Go to your Google Account: [https://myaccount.google.com/](https://myaccount.google.com/)
        2.  Navigate to **Security**.
        3.  Under "Signing in to Google," click on **App passwords**. (You may need to sign in again).
            *   *If you don't see this option, 2-Step Verification might not be set up, or it's managed by your organization if it's a GSuite account.*
        4.  At the bottom, click "Select app" and choose **Mail**.
        5.  Click "Select device" and choose **Other (Custom name)**.
        6.  Enter a descriptive name (e.g., "Flask Writing Hub App") and click **Generate**.
        7.  Google will provide a 16-character App Password. **Copy this password.** This is what you will use for `SENDER_PASSWORD`.
        8.  Replace `"YOUR_GMAIL_APP_PASSWORD"` in `app.py` with this generated 16-character App Password.
    *   If you do not have 2-Step Verification enabled (not recommended), you might need to enable "Less secure app access" in your Google account settings for the application to send emails with your regular password. However, using an App Password is the preferred and more secure method.

3.  **`RECIPIENT_EMAIL`**:
    *   This is already set to `obakengmathibe3@gmail.com` as per your request. You can change it if needed.

**Security Note:** For production environments, it's best practice to store sensitive credentials like email passwords in environment variables or a secure configuration management system, rather than hardcoding them directly in the source code.

## Running the Application

1.  **Start the Flask Development Server:**
    *   Ensure your virtual environment is activated.
    *   Navigate to the project's root directory (where `app.py` is located).
    *   Run the following command in your terminal:
        ```bash
        python app.py
        ```

2.  **Access the Application:**
    *   Open your web browser and go to:
        [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

    *   You should see the Writing Hub Submission form.

## Features

*   **Student Submission Form:** Allows students to enter their name, subject, faculty, student number, and upload a Word document (`.doc` or `.docx`).
*   **Email Notification:** Upon successful submission, an email is sent to the configured recipient with all the student's details and the submitted document as an attachment.
*   **File Storage:** Uploaded documents are saved in the `uploads/` directory on the server with unique filenames.
*   **Admin Panel:** Accessible at `/admin/panel`, it lists all submitted documents, showing the saved filename, parsed original filename, upload timestamp, and a link to view/download each document.
*   **Error Handling:** Includes validation for file types, file selection, and provides user feedback for various scenarios, including upload size limits (16MB).

---
Remember to replace placeholder credentials in `app.py` before running.
