def send_Email():
    import os
    import csv

    os.system('cls')

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    
    response_path = "media//responses.csv"
    if not os.path.exists(response_path):
        print("Error")
        return

    Stud_Info = {}
    with open(response_path, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if line[6] != 'Roll Number':
                Stud_Info[(line[6]).upper()] = [line[1], line[4]]

    

    j = 0
    for key, value in Stud_Info.items():
        if key == "ANSWER":
            continue
        for email in value:
            fromaddr = "vkcs384@gmail.com"
            toaddr = email
            
            # instance of MIMEMultipart
            msg = MIMEMultipart()
            
            # storing the senders email address  
            msg['From'] = fromaddr
            
            # storing the receivers email address 
            msg['To'] = toaddr
            
            # storing the subject 
            msg['Subject'] = "Subject of the Mail"
            
            # string to store the body of the mail
            body = "Body_of_the_mail"
            
            # attach the body with the msg instance
            msg.attach(MIMEText(body, 'plain'))
            
            # open the file to be sent 
            filename = str(key) + ".xlsx"
            attachment = open("Project_App//marksheets/" + filename, "rb")
            
            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')
            
            # To change the payload into encoded form
            p.set_payload((attachment).read())
            
            # encode into base64
            encoders.encode_base64(p)
            
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            
            # attach the instance 'p' to instance 'msg'
            msg.attach(p)
            
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            
            # start TLS for security
            s.starttls()
            
            # Authentication
            s.login(fromaddr, "abcd@1234")
            
            # Converts the Multipart msg into a string
            text = msg.as_string()
            
            # sending the mail
            s.sendmail(fromaddr, toaddr, text)
            
            # terminating the session
            print(email)
            # print("DONE")

            s.quit()
        j += 1
        if j == 3:
            print("DONE")
            break

# send_Email()