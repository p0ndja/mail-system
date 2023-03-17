try:
    import PondJaMail as PJMail
    import mysql.connector
    import time
    import json
    import os
    from os import path
except Exception as e:
    print("[!] ERROR on importing module:\n",e)
    exit(0)

dbconnector = None
mycursor = None

def dbconnect():
    global dbconnector, mycursor
    # Check if settings is exist.
    if not path.isfile("settings.json"):
        json = """{
        "database": {
            "host":     "<<IP>>",
            "username": "<<USERNAME>>",
            "password": "<<PASSWORD>>",
            "database": "<<DATABASE>>"
        }
    }"""
        
        f = open("settings.json","w")
        f.write(str(json))
        print("/!\ Please config your connection settings first. /!\\")
        exit(0)

    #Loading settings.json
    f = json.loads(open("settings.json", "r").read())
    try:
        dbconnector = mysql.connector.connect(host=f['database']['host'],user=f['database']['username'],password=f['database']['password'],database=f['database']['database'])
        mycursor = dbconnector.cursor(buffered=True)
    except Exception as e:
        print("[!] ERROR on establishing database:\n", e)
        exit(0)

def findQueue():
    while True:
        try:
            mycursor.execute("SELECT `id`,`title`,`sender`,`receiver`,`mail`,`variable` FROM `mailsystem` WHERE isSend = 0 ORDER BY `id`") #Get specific data from submission SQL where result is W (Wait)
            return mycursor.fetchall() #fetchone() -> fetch 1 data matched, fetchall() -> fetch all data matched
        except Exception as e:
            print("[!] ERROR losing connection to database:\n", e)
            print("[!] The system will be halt for 30 seconds and will try again.")
            time.sleep(30)
            dbconnect()

if __name__ == '__main__':
    print("[/] Mail System, Starto!")
    while(1):
        dbconnect()
        queue = findQueue()
        if (len(queue)):
            print(f"Found waiting mail queue: {len(queue)}\n{queue}")
        for task in queue:
            tries = 0
            statusCode = 0
            #Check sender data
            senderData = json.loads(task[2])
            if (len(senderData) != 3):
                print(f"[!] Sender Data for ID #{task} is invalid! [!]\nPlease specify sender's name, email and password, in JSON.")
                statusCode = -1
            mid = task[0]
            title = task[1]
            receiver = task[3]
            mail = task[4]
            var = task[5]

            while(1):
                tries+=1
                send = PJMail.sendEmail(f"{senderData['name']};{senderData['email']};{senderData['password']}",receiver,title,mail,var)
                # 1 : Success
                if (send == 1):
                    #print(f"Sent email to {receiver}.")
                    statusCode = 1
                    break
                # 0 : Unsuccess -> Missing Sender Data
                elif (send == 0):
                    print(f"Missing sender data.")
                    statusCode = -1
                    break
                # -1 : Unsuccess -> URL response not 200
                elif (send == -1):
                    print(f"Invalid email template URL.")
                    statusCode = -2
                    break
                # -9 : Email Sending Error
                elif (send == -9):
                    if (tries != 5):
                        print(f"Unable to send email....Will try again in 5 seconds. Try: {tries}/5")
                        time.sleep(5)
                    else:
                        print(f"Unable to send email....But reached maximum tries, SKIPPED.")
                        statusCode = -9
                        break
                else:
                    statusCode = -99
                    print(f"WTF, THERE'S NO ERROR CODE LIKE {send}....WHAT!?")
                    break
            
            query = (f"UPDATE `mailsystem` SET `isSend` = {statusCode} WHERE `id` = {mid}")
            mycursor.execute(query)
            print(f"Finished sending email #{mid} from {senderData['name']} to {receiver}")
            dbconnector.commit()
            time.sleep(1)
        dbconnector.commit()
        dbconnector.close()
        time.sleep(10)
        #Time sleep interval for 5 second.
