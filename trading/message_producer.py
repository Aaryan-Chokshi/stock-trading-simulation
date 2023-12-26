import stomp



def sendMessage(dbid, message):

    user = "admin"
    password = "password"
    host = "localhost"
    port = 61613

    conn = stomp.Connection(host_and_ports = [(host, port)])
    conn.connect(login=user,passcode=password)
    conn.send(body=message, destination=f"/queue/{dbid}", persistent='false')
    conn.disconnect()