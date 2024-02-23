import streamlit as st
import smtplib as smt
from email.mime.text import MIMEText


st.set_page_config(page_title="Support", page_icon="💩", layout="wide")

def passwort_auslesen(dateiname):
    try:
        with open(dateiname, 'r') as file:
            passwort = file.read().strip()  # Passwort aus der Datei lesen und führende/trailing Leerzeichen entfernen
        return passwort
    except FileNotFoundError:
        print("Die Datei wurde nicht gefunden.")
        return None
    
dateiname = "password.txt"
passwort = passwort_auslesen(dateiname)




st.header("Support")
st.write("If you have any questions or need help, please feel free to contact us.")

st.write(" ")
st.write(" ")

email_support = "pandasengineeringsup@gmail.com"
email_customer = st.text_input("Enter your email address:")
email_subject = st.text_input("Enter the subject of your email:")
email_text = st.text_area("Enter your message:")

if st.button("Send email"):
    try:
        email_text_with_customer = f"From: {email_customer}\n\n{email_text}"
        email = MIMEText(email_text_with_customer)
        email['From'] = email_customer
        email['To'] = email_support
        email['Subject'] = email_subject

        server = smt.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_support, passwort)
        server.sendmail(email_customer, email_support, email.as_string())
        server.quit()

        st.write("Email sent successfully.")



    except:
        st.write("Aufgrund aktueller technischer Probleme konnte die Email nicht gesendet werden. Bitte versuchen Sie es später erneut.")


