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

def process_files(paths):
    sock = mayaclient.create_client(mayaclient.start_process())
    for path in paths:
        print 'Processing', path
        try:
            process(sock, path)
            print 'Success!', path
        except RuntimeError:
            print 'Failed!', path

if __name__ == '__main__':
    import threading
    paths = [f for f in os.listdir(os.getcwd())
             if f.endswith(('.ma', '.mb'))]
    threads = []
    num_procs = 4 # Or number of CPU cores, etc.
    for i in range(num_procs):
        chunk = [paths[j] for j in range(i, len(paths), num_procs)]
        t = threading.Thread(target=process_files, args=[chunk])
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
