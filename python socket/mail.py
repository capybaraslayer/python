import poplib as p
import imaplib as imap
import smtplib as s
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from  email.message import EmailMessage
import email

USER = "catalinzavtone@gmail.com"
APP_PASS = "fmod ekql qbtq wrvj"

while True:
    print("                           ")
    print("=============================")
    print("1.Vizionare emailuri cu POP3:")
    print("2.Vizionare emailuri cu IMAP:")
    print("3.Descarca:")
    print("4.Trimite email doar text:")
    print("5.Trimite emil cu atasament:")
    print("0.Exit:")

    numar = int(input("Introdu numarul comenzii:"))
    match numar:
        case 0:
            print("====Programul sa incheiat====")
            break
        case 1:
            print("====Inbox POP3====")
            SERVER_POP = "pop.gmail.com"
            server_pop = p.POP3_SSL(SERVER_POP)
            server_pop.user(USER)
            server_pop.pass_(APP_PASS)
            num_mesaje, _ = server_pop.stat()
            start = max(1, num_mesaje - 9)
            for i in range(num_mesaje, start - 1, -1):
                email = []
                resp, lines, octets = server_pop.retr(i)
                for line in lines:
                    data = line.decode("UTF-8")
                    if data.startswith("From:"):
                        email.append(data)
                    if data.startswith("Subject:"):
                        email.append(data)
                if email:
                    print(f"Mesaj #{i}: {email}")
            server_pop.quit()
        case 2:
            print("====Inbox IMAP====")
            server_imap = imap.IMAP4_SSL("imap.gmail.com")
            server_imap.login(USER, APP_PASS)
            server_imap.select("INBOX")
            status, data = server_imap.search(None, "ALL")
            id_list = data[0].split()
            id_list.reverse()
            if status.startswith("OK"):
                for num in id_list[:10]:
                    status, date = server_imap.fetch(num, "(RFC822)")
                    for parte in date:
                        if isinstance(parte, tuple):
                            mes = email.message_from_bytes(parte[1])
                            mes = {"expeditor": mes["From"], "subiect": mes["Subject"]}
                        print(mes)
            server_imap.logout()
        case 3:
            print("====Descarca email====")
            server_imap = imap.IMAP4_SSL("imap.gmail.com")
            server_imap.login(USER, APP_PASS)
            server_imap.select("inbox")
            status, data = server_imap.search(None, "ALL")
            if status != 'OK':
                print ("No messages found!")
            else:
                last_ids=data[0].split()[-10]
                rv, data = server_imap.fetch(last_ids, '(RFC822)')
                with open('email.txt', 'ab') as f:
                    f.write(data[0][1])
        case 4:
            print('====Trimite email====')
            msg=EmailMessage()
            msg['Subject']=input('Subiect:')
            msg["From"] = USER
            msg["To"] = input("Email:")
            msg['Reply-To'] = input("Reply-To (adresa pentru raspuns): ")
            msg.set_content(input('Text:'))
            with s.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(USER, APP_PASS)
                smtp.send_message(msg)
                print('Mesajul a fost transmis cu succes')
        case 5:
            print("==== Trimite email cu atasament ====")
            subiect = "Email cu atasament"
            to = input("Cui doresti sa-i trimit emailul?: ")
            corp=input('Scrie mesajul:')
            mes = MIMEMultipart()
            mes["From"] = USER
            mes["To"] = to
            mes["Subject"] = subiect
            mes["Reply-To"] = input("Reply-To (adresa pentru raspuns): ")
            mes.attach(MIMEText(corp, "plain"))

            with open("cat.jpg", "rb") as f:
                parte = MIMEBase("application", "octet-stream")
                parte.set_payload(f.read())

            encoders.encode_base64(parte)
            parte.add_header("Content-Disposition", 'attachment; filename="cat.jpg"')
            mes.attach(parte)

            with s.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(USER, APP_PASS)
                server.sendmail(USER, to, mes.as_string())
                print("Email trimis cu succes!")
