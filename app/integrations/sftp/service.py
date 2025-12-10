from app.common.exceptions import DomainError
from app.integrations.sftp.client import SFTPClient


def upload_event_header(path, event_id):
    if not path.endswith(".png"):
        raise DomainError("Only PNGs allowed")

    client = SFTPClient()
    client.upload(path, f"/events/header/{event_id}.png")


def upload_event_logo(path, event_id):
    if not path.endswith(".png"):
        raise DomainError("Only PNGs allowed")

    client = SFTPClient()
    client.upload(path, f"/events/logo/{event_id}.png")


def download_event_header(event_id, local_path):
    client = SFTPClient()
    client.download(f"/events/header/{event_id}.png", local_path)


def download_event_logo(event_id, local_path):
    client = SFTPClient()
    client.download(f"/events/logo/{event_id}.png", local_path)


def delete_event_header(event_id):
    client = SFTPClient()
    client.delete(f"/events/header/{event_id}.png")


def delete_event_logo(event_id):
    client = SFTPClient()
    client.delete(f"/events/logo/{event_id}.png")
