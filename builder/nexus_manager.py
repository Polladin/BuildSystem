
import pycurl
from urllib.parse import urlencode


class NexusManager:

    def __init__(self):

        pass

    def upload_file(self):

        c = pycurl.Curl()
        c.setopt(c.URL, 'http://192.168.56.101:8081/repository/repo_4/org/fee/1.1/fee-1.1.txt')

        c.setopt(pycurl.VERBOSE, 1)

        # c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
        c.setopt(pycurl.USERPWD, 'admin' + ':' + 'admin123')

        c.setopt(c.HTTPPOST, [
            ('fileupload', (
                c.FORM_BUFFER, 'storage/group_build_ver.json',
                c.FORM_BUFFERPTR, 'This is a fancy readme file',
            )),
        ])

        c.setopt(pycurl.CUSTOMREQUEST, "PUT")

        c.perform()
        c.close()


NexusManager().upload_file()

