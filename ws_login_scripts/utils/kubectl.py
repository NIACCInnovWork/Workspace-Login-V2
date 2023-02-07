import subprocess as sp
import json
import base64
import time

class Secret:
    def __init__(self, raw):
        self.raw = raw

    def get_secret(self, secret_key):
        if secret_key not in self.raw['data']:
            raise ValueError("Value not found in secret")
        return base64.b64decode(self.raw['data'][secret_key])


class PortForwardSession:
    def __init__(self, p):
        self.p = p

    def close(self):
        self.p.terminate()
        try:
            self.p.wait(timeout=5)
        except sp.TimeoutExpired:
            eprint("Failed to shutdown port forwarding session. killing...")
            self.p.kill()


class KubeCtl:
    def __init__(self):
        pass

    def fetch_secrets(self, secret: str):
        p = sp.run(["kubectl", "get", "secret", secret, "--output=json"], capture_output=True)
        return Secret(json.loads(p.stdout))

    def port_forward(self, service: str, port: int):
        p = sp.Popen(["kubectl", "port-forward", "service/" + service, str(port) + ":" + str(port)])
        time.sleep(2) # Give it a sec to see if it died
        if p.poll() is not None:
            raise IOError("Failed to open port forwarding")

        return PortForwardSession(p)

