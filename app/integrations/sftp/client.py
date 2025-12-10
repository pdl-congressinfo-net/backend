import paramiko

from app.core.config import settings


class SFTPClient:
    def __init__(self, host=None, username=None, password=None, port=21):
        host = host or settings.SFTP_HOST
        username = username or settings.SFTP_USER
        password = password or settings.SFTP_PASSWORD
        port = port or settings.SFTP_PORT
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def upload(self, local_path: str, remote_path: str):
        with paramiko.Transport((self.host, self.port)) as transport:
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(local_path, remote_path)
            sftp.close()

    def download(self, remote_path: str, local_path: str):
        with paramiko.Transport((self.host, self.port)) as transport:
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.get(remote_path, local_path)
            sftp.close()

    def delete(self, remote_path: str):
        with paramiko.Transport((self.host, self.port)) as transport:
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.remove(remote_path)
            sftp.close()
