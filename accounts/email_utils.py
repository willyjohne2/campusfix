"""
Email utility functions using Brevo (Sendinblue) API
Handles sending transactional emails for verification codes and password resets
"""

import os
import requests


BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
BREVO_SENDER_NAME = os.environ.get("BREVO_SENDER_NAME", "CampusFix")
BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL", "onboarding@campusfix.tk")
CONTACT_RECEIVER_EMAIL = os.environ.get("CONTACT_RECEIVER_EMAIL", BREVO_SENDER_EMAIL)


def send_verification_email(email, code):
    """
    Send verification code email using Brevo API

    Args:
        email (str): Recipient email address
        code (str): 6-digit verification code

    Returns:
        bool: True if successful, False otherwise
    """
    if not BREVO_API_KEY:
        print("Error: BREVO_API_KEY not set in environment variables")
        return False

    try:
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "sender": {
                "name": BREVO_SENDER_NAME,
                "email": BREVO_SENDER_EMAIL,
            },
            "to": [{"email": email}],
            "subject": "CampusFix Email Verification",
            "htmlContent": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2>Welcome to CampusFix!</h2>
                <p>Your email verification code is:</p>
                <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0;">
                    <h1 style="font-size: 32px; letter-spacing: 5px; color: #333; margin: 0;">{code}</h1>
                </div>
                <p>This code will expire in <strong>1 hour</strong>.</p>
                <p>If you didn't create this account, please ignore this email.</p>
                <hr>
                <p style="font-size: 12px; color: #666;">
                    CampusFix - Campus Issue Reporting System
                </p>
            </div>
            """,
            "textContent": f"Your CampusFix verification code is: {code}. This code will expire in 1 hour.",
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Verification email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"Error sending verification email: {str(e)}")
        return False


def send_password_reset_email(email, reset_code):
    """
    Send password reset email using Brevo API

    Args:
        email (str): Recipient email address
        reset_code (str): 8-character password reset code

    Returns:
        bool: True if successful, False otherwise
    """
    if not BREVO_API_KEY:
        print("Error: BREVO_API_KEY not set in environment variables")
        return False

    try:
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "sender": {
                "name": BREVO_SENDER_NAME,
                "email": BREVO_SENDER_EMAIL,
            },
            "to": [{"email": email}],
            "subject": "CampusFix Password Reset Code",
            "htmlContent": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2>Password Reset Request</h2>
                <p>You requested to reset your CampusFix password. Your reset code is:</p>
                <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0;">
                    <h1 style="font-size: 32px; letter-spacing: 5px; color: #333; margin: 0;">{reset_code}</h1>
                </div>
                <p>Enter this code on the password reset page along with your new password.</p>
                <p>This code will expire in <strong>1 hour</strong>.</p>
                <p>If you didn't request this, please ignore this email and your password will remain unchanged.</p>
                <hr>
                <p style="font-size: 12px; color: #666;">
                    CampusFix - Campus Issue Reporting System
                </p>
            </div>
            """,
            "textContent": f"Your CampusFix password reset code is: {reset_code}. This code will expire in 1 hour.",
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Password reset email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"Error sending password reset email: {str(e)}")
        return False


def send_contact_email(name, from_email, subject, message_body):
    """Send a contact message to site admins using Brevo API.

    This uses the verified sender as the `sender` and sets `replyTo` to the user-provided email.
    """
    if not BREVO_API_KEY:
        print("Error: BREVO_API_KEY not set in environment variables")
        return False

    try:
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": CONTACT_RECEIVER_EMAIL}],
            "subject": f"[Contact] {subject}",
            "replyTo": {"email": from_email, "name": name},
            "htmlContent": f"""
            <div style='font-family: Arial, sans-serif; max-width: 680px; margin: 0 auto;'>
              <h3>New contact message from {name} &lt;{from_email}&gt;</h3>
              <p><strong>Subject:</strong> {subject}</p>
              <hr />
              <div style='white-space: pre-wrap'>{message_body}</div>
              <hr />
              <p style='font-size:12px;color:#666;'>This message was sent via CampusFix contact form.</p>
            </div>
            """,
            "textContent": f"Contact message from {name} <{from_email}>\n\nSubject: {subject}\n\n{message_body}",
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Contact email sent successfully from {from_email}")
        return True
    except Exception as e:
        print(f"Error sending contact email: {str(e)}")
        return False


def send_reply_email(to_email, subject, message_body):
    """Send a reply email from the verified sender to an arbitrary recipient."""
    if not BREVO_API_KEY:
        print("Error: BREVO_API_KEY not set in environment variables")
        return False

    try:
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {"api-key": BREVO_API_KEY, "Content-Type": "application/json"}
        payload = {
            "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
            "to": [{"email": to_email}],
            "subject": subject,
            "htmlContent": f"""
            <div style='font-family: Arial, sans-serif; max-width: 680px; margin: 0 auto;'>
              <div style='white-space: pre-wrap'>{message_body}</div>
              <hr />
              <p style='font-size:12px;color:#666;'>This message was sent via CampusFix.</p>
            </div>
            """,
            "textContent": message_body,
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Reply email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Error sending reply email: {str(e)}")
        return False
