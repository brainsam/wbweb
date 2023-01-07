import subprocess
import re

class configReader():
    config: str

    def getConfig(self):
        result = subprocess.run(['sudo', 'wg', 'show'], stdout=subprocess.PIPE)
        if result.returncode == 0:
            return result.stdout.decode("utf-8")
        else:
            return result.stderr.decode("utf-8")

    def _parseLine(self, line: str):
        pattern = {
            'interface': re.compile(r'interface: (?P<interface>.*)'),
            'publicKey': re.compile(r'public key: (?P<publicKey>.+)'),
            'listeningPort': re.compile(r'listening port: (?P<listeningPort>.*)'),
            'peer': re.compile(r'peer: (?P<peer>.+=)'),
            'allowedIPs': re.compile(r'allowed ips: (?P<allowedIPs>.+)'),
            'endpoint': re.compile(r'endpoint: (?P<endpoint>.+)'),
            'latestHandshake': re.compile(r'latest handshake: (?P<latestHandshake>.+)'),
            'bandwith': re.compile(r'bandwith: (?P<bandwith>.+)'),
            'transfer': re.compile(r'transfer: (?P<transfer>.+)'),
            'persistentKeepalive': re.compile(r'persistent keepalive: (?P<persistentKeepalive>.+)')
        }
        for key, rx in pattern.items():
            match = rx.search(line)
            if match:
                return key, match.group(key)
        return None, None

    def parseConfig(self):
        structuredConfig = []
        peer = {}
        for line in self.getConfig().split("\n"):
            key, match = self._parseLine(line)
            if key == 'peer' or key == 'interface':
                if peer != {}:
                    structuredConfig.append(peer)
                peer = {key: match}
            elif key:
                peer.update({key: match})
        structuredConfig.append(peer)
        return structuredConfig
