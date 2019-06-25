import ipfsapi
import os


class DecentralizedStorage:

    def __init__(self):
        self.host = 'localhost'
        self.port = 5001
        self.ipfs_client = ipfsapi.Client(self.host, 5001)

    def load_ipfs_file(self, hash):
        self.ipfs_client.get(hash)

    def add_ipfs_file(self, file):
        ipfs_res = self.ipfs_client.add(file)
        print(ipfs_res)
        return ipfs_res

    def save_persona(self, persona):
        return

    def update_file(self, hash):
        ipfs_res = self.ipfs_client.name_publish(hash)
        print(ipfs_res)
        print(self.ipfs_client.resolve(ipfs_res['Name']))
        print(self.ipfs_client.name_resolve())

    def store(self, file):
        res = self.add_ipfs_file(file)
        return res['Hash']

    def retrieve(self, hash, dir_name, file_name):
        # self.ipfs_client.get(hash)
        content = self.ipfs_client.cat(hash)
        if not os.path.exists(os.path.dirname(dir_name)):
            try:
                os.makedirs(os.path.dirname(dir_name))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        file_name = os.path.join(dir_name, file_name)
        f = open(file_name, "wb")
        f.write(content)
        return file_name

