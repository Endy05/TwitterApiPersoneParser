class DataRotator:
    def __init__(self, data_list):
        self.data_list = data_list
        self.current_index = 0

    def get_next(self):
        data = self.data_list[self.current_index]
        auth_id = data['cookies']['auth_token'][:10]  # Get first 10 chars of auth token
        self.current_index = (self.current_index + 1) % len(self.data_list)
        return data, auth_id
