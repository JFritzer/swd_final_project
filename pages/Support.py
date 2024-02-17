import streamlit as st
import smtplib as smt
from email.mime.text import MIMEText

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
        server.login(email_support, "wwdsjpxgvxwsuptk")
        server.sendmail(email_customer, email_support, email.as_string())
        server.quit()

        st.write("Email sent successfully.")



    except:
        st.write("Aufgrund aktueller technischer Probleme konnte die Email nicht gesendet werden. Bitte versuchen Sie es später erneut.")



#Quelle: https://github.com/tonykipkemboi/streamlit-smtp-test/blob/main/streamlit_app.py
#Bei der Problemsuche bezüglich 2-FA dann auch das: https://discuss.streamlit.io/t/send-email-with-smtp-and-gmail-address/48145/4
        


