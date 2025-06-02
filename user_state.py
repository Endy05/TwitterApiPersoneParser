class UserState:
    def __init__(self):
        self.name = None
        self.username = None
        self.avatar_url = None
        self.banner_url = None

    def get_changes(self, new_name, new_username, new_avatar, new_banner):
        profile_url = f"https://x.com/{new_username}"
        changes = []
        
        if self.avatar_url != new_avatar:
            changes.append(
                f"NEW AVA {new_username.upper()}\n"
                f"{new_avatar}\n\n"
                f"OLD AVA {new_username.upper()}\n"
                f"{self.avatar_url}\n\n"
                f"Profile: {profile_url}"
            )
        if self.banner_url != new_banner and new_banner:  
            changes.append(
                f"NEW BANNER {new_username.upper()}\n"
                f"{new_banner}\n\n"
                f"OLD BANNER {new_username.upper()}\n"
                f"{self.banner_url or 'Default banner'}\n\n"
                f"Profile: {profile_url}"
            )
        if self.name != new_name:
            changes.append(f"NAME CHANGING\n\n{self.name} ➜ {new_name}\n\nProfile: {profile_url}")
        
        return changes
