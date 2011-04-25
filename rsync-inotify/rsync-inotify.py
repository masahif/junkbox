import pyinotify
import shlex
import subprocess
import sys, os
import logging
from FsQueue import Queue

class RsyncHandler(pyinotify.ProcessEvent):
    def __init__(self, src, dest, queue):
        self.src = src
        self.dest = dest
        self.queue = queue
    
    def process_IN_CLOSE_WRITE(self, event):
        logging.debug("IN_CLOSE_WRITE: %s" % event.pathname)
        self.rsync()

    def process_IN_MOVED_TO(self, event):
        logging.debug("IN_MOVED_TO: %s" % event.pathname)
        self.rsync()

    def process_IN_CREATE(self, event):
        if os.path.isdir(event.pathname):
            logging.debug("IN_CREATE|IN_ISDIR: %s" % event.pathname)
            self.rsync()

    def queue_put(self, item):
        if self.queue:
            self.queue.put(item)
            
    def rsync(self):
        cmd = "rsync -avxt --delete-after --safe-links --out-format='%i;%f'"
        args = shlex.split(cmd) + [self.src, self.dest]

        try:
            logging.debug("RSYNC: %s" % " ".join(args))

            p = subprocess.Popen(args, stdout=subprocess.PIPE)
            sout = p.communicate()[0]

            files = []
            for line in sout.split("\n"):
                logging.debug("RSYNC: %s" % line)
                try:
                    line.index(">")
                    files.append(line.split(";")[1])
                except ValueError:
                    pass

            self.queue_put(files)

        except OSError, e:
            logging.info(e)
            sys.exit(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    if len(sys.argv) not in [3,4]:
        print 'Usage: %s src dest [FsQueue dir]' % sys.argv[0]
        sys.exit(1)

    if (not os.path.isdir(sys.argv[1])) or (not os.path.isdir(sys.argv[2])):
        print "src and dest should be directories."
        sys.exit(1)

    queue = None
    if len(sys.argv) is 4:
        if not os.path.isdir(sys.argv[3]):
            print "Queue should be FsQueue's directory."
            sys.exit()
        queue = Queue(dir=sys.argv[3], init=True)
    
    # Watch Manager
    wm = pyinotify.WatchManager()

    # watched events
    mask = pyinotify.IN_CLOSE_WRITE|pyinotify.IN_MOVED_TO|pyinotify.IN_CREATE

    handler = RsyncHandler(sys.argv[1], sys.argv[2], queue)
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(sys.argv[1], mask, rec=True)

    logging.debug("Start notifier loop")
    notifier.loop()
