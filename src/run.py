from remote_file_transfer import ProjectCopier

if __name__=='__main__':
    # Define what the directory for your project is
    remote_project = "/home/alopresto/Project1/src/"
    copier = ProjectCopier(ip="10.10.11.64", user="alopresto", password="M@st3r5u3l", remote_project=remote_project, filename="main.py")
    #Run main.py and return the results to this console
    copier.deploy()
