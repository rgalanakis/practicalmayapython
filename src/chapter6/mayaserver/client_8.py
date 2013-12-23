"""
GUI server.
"""

import client_1
client_1.MAYAEXE = client_1.MAYAEXE.replace('mayabatch.exe', 'maya.exe')
import client_7
client_7.COMMAND = client_7.SETCMD('_gui', client_7.ORIGCOMMAND)

if __name__ == '__main__':
    sock = client_7.create_client(client_7.start_process())
    client_7.sendrecv(sock, ('exec', 'import pymel.core as pmc'))
    client_7.sendrecv(sock, ('exec', 'pmc.polySphere()'))
    import time
    time.sleep(20)
