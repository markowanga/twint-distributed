class ProxyConfig:

    def __init__(self, host: str, port: int, proxy_type: str):
        self._host = host
        self._port = port
        self._proxy_type = proxy_type
        return

    def get_host(self):
        return self._host

    def get_port(self):
        return self._port

    def get_proxy_type(self):
        return self._proxy_type

    def to_string(self):
        return 'ProxyConfig(host=' + self.get_host() + '; port=' + str(
            self.get_port()) + '; proxy_type=' + self.get_proxy_type() + ')'


default_proxy_config = ProxyConfig('localhost', 9050, 'socks5')
