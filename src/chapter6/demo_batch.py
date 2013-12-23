import os
os.chdir(r'C:\Users\rgalanakis\Documents\maya\projects\default\scenes')
import mayaserver.client_7 as mayaclient

execstr = """import pymel.core as pmc
pmc.openFile(%r, force=True)
for item in pmc.ls(type='unknown'):
    if item.exists():
        pmc.delete(item)
pmc.system.saveAs(%r)"""

def process(socket, path):
    newpath = os.path.splitext(path)[0] + '_clean.ma'
    mayaclient.sendrecv(
        socket, ('exec', execstr % (path, newpath)))

if __name__ == '__main__':
    sock = mayaclient.create_client(mayaclient.start_process())
    paths = [p for p in os.listdir(os.getcwd())
             if p.endswith(('.ma', '.mb'))]
    for p in paths:
        if p.endswith(('.ma', '.mb')):
            print 'Processing', p
            try:
                process(sock, p)
                print 'Success!', p
            except RuntimeError:
                print 'Failed!', p
