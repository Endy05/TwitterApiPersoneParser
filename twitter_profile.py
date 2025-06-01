import requests
import json
from datetime import datetime

class TwitterProfile:
    def __init__(self, config_data):
        self.url = "https://x.com/i/api/graphql/xWw45l6nX7DP2FKRyePXSw/UserByScreenName"
        self.variables = config_data['request_data']['profile']['variables_userByScreenName']
        self.features = config_data['request_data']['profile']['features_userByScreenName']
        self.headers = config_data['request_data']['profile']['headers']
        self.cookies = config_data['request_data']['profile']['cookies']
        
        self.params = {
            "variables": json.dumps(self.variables),
            "features": json.dumps(self.features),
            "fieldToggles": json.dumps({"withAuxiliaryUserLabels": True})
        }

    def get_full_avatar_url(self, url):
        if url and '_normal.' in url:
            return url.replace('_normal.', '.')
        return url

    async def check_profile(self):
        try:
            response = requests.get(self.url, headers=self.headers, cookies=self.cookies, params=self.params)
            current_time = datetime.now().strftime("%H:%M:%S")
            
            if response.ok:
                data = response.json()
                user = data["data"]["user"]["result"]
                return {
                    'status': 'ok',
                    'name': user["core"]["name"],
                    'username': user["core"]["screen_name"],
                    'avatar_url': self.get_full_avatar_url(user.get("avatar", {}).get("image_url", None)),
                    'banner_url': f"{user['legacy']['profile_banner_url']}/600x200" if "profile_banner_url" in user.get("legacy", {}) else None,
                    'current_time': current_time
                }
            
            return {
                'status': 'error',
                'code': response.status_code,
                'current_time': current_time
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'current_time': datetime.now().strftime("%H:%M:%S")
            }
