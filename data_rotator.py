class DataRotator:
    def __init__(self, data_list):
        self.data_list = data_list
        self.current_index = 0

    def get_proxy_info(self, data):
        """Get readable proxy information from auth data"""
        proxy = data.get('proxy', None)
        if not proxy:
            return "[No proxy]"
        proxy_url = proxy.get('https', None)
        if not proxy_url:
            return "[Invalid proxy]"
        try:
            # Extract proxy details
            auth_host = proxy_url.split('@')
            if len(auth_host) != 2:
                return "[Malformed proxy]"
            user_pass, host_port = auth_host
            protocol, credentials = user_pass.split('://')
            username = credentials.split(':')[0]
            host = host_port.split(':')[0]
            return f"[Proxy: {protocol}://{username}@{host}]"
        except:
            return "[Error parsing proxy]"

    def get_next(self):
        data = self.data_list[self.current_index]
        auth_id = data['cookies']['auth_token'][:10]  # Get first 10 chars of auth token
        proxy_info = self.get_proxy_info(data)
        self.current_index = (self.current_index + 1) % len(self.data_list)
        return data, auth_id, proxy_info
