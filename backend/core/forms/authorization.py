from fastapi import Form


class CustomLoginForm:
    def __init__(
            self,
            domain_number: int = Form(...),
            username: str = Form(...),
            password: str = Form(...),
    ):
        self.domain_number = domain_number
        self.username = username
        self.password = password
