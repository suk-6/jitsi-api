import paramiko
from scp import SCPClient, SCPException

from app.config import Settings

env = Settings()


class JibriSCP:
    def __init__(self):
        self.ssh_client = None
        self.create_ssh_client()

    def create_ssh_client(self):
        """Create SSH client session"""
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )
            self.ssh_client.connect(
                hostname=env.jibri_ssh_host,
                port=env.jibri_ssh_port,
                username=env.jibri_ssh_user,
                password=env.jibri_ssh_password,
            )
        else:
            print("SSH client session exist.")

    def close_ssh_client(self):
        """Close SSH client session"""
        self.ssh_client.close()

    def get_recording_file(self, room_id: str):
        """Get a single file from remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                sftp = self.ssh_client.open_sftp()
                sftp.chdir(f"{env.jibri_recordings_path}/{room_id}")
                file_list = sftp.listdir()
                if not file_list:
                    raise SCPException.message("No files found")

                video_file = [f for f in file_list if f.endswith(".mp4")][0]

                scp.get(
                    f"{env.jibri_recordings_path}/{room_id}/{video_file}",
                    f"/tmp/{room_id}.mp4",
                )
        except SCPException:
            raise SCPException.message
