import os
import paramiko

class ProjectCopier:

    def __init__(self, ip, user, password, remote_project, filename):
        self.ip = ip
        self.user = user
        self.password = password
        self.remote_project = remote_project
        self.filename = filename

        self.ssh = paramiko.SSHClient()
        self.ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        self.sftp = None

    def _connect(self):
        self.ssh.connect(self.ip, username=self.user, password=self.password)
        self.sftp = self.ssh.open_sftp()

    def _disconnect(self):
        if self.sftp is not None:
            self.sftp.close()
        if self.ssh is not None:
            self.ssh.close()

    def _initialize_project(self):
        self.mkdir(self.remote_project, ignore_existing=True)


    def copy_src(self):
        path = os.path.dirname(os.path.abspath(__file__))         # Grab src directory
        self.put_dir(path, self.remote_project)

    def put_dir(self, source, target):
        if "__pycache__" in source:
            pass
        else:
            for item in os.listdir(source):
                cur = os.path.join(source, item)
                if os.path.isfile(cur):
                    #print("Copying %s"%cur)
                    self.sftp.put(cur, '%s/%s' % (target, item))
                else:
                    self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                    self.put_dir(cur, '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        try:
            self.sftp.mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise

    def run(self):
        std = self.ssh.exec_command("cd %s;python3 %s"% (self.remote_project, self.filename))
        stdout,stderr = std[1], std[2]
        [print(line, end="") for line in stderr]
        [print(line, end="") for line in stdout]

    def deploy(self):
        self._connect()
        self._initialize_project()
        self.copy_src()
        self.run()
        self._disconnect()




