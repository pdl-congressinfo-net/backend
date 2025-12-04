import paramiko

from app.core.config import settings


def sftp_connect():
    transport = paramiko.Transport((settings.SFTP_HOST, settings.SFTP_PORT))
    transport.connect(username=settings.SFTP_USER, password=settings.SFTP_PASSWORD)
    return paramiko.SFTPClient.from_transport(transport)
