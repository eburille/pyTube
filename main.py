from mailer import *
from downloader import Download
from time import sleep

class pyTuber():
    def check_email_received(self):
        if numero_de_emails() > 0:
            return True
        else:
            return False

    def get_email(self, From: str):
        e_mail = From.split("<")[-1][0:-1]
        print(e_mail)
        return e_mail

    def run(self):

        if self.check_email_received():
            From, link = get_last_message()
            e_mail = self.get_email(From)

            try:
                nome_video = Download(link)
                
                try:    
                    send_video(nome_video, e_mail)
                except:
                    send_message("Não foi possivel enviar o video", "fail envio", e_mail)

            except:
                send_message("Não foi possivel baixar o video", "fail dowload", e_mail)

        
        sleep(10)


if __name__ == "__main__":
    pytuber = pyTuber()
    while True:
        pytuber.run()