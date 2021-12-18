class ApiError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Api call to Monzo failed, reason={self.message}, code={self.code}'

    def is_unauthorised(self):
        return self.code.split('.')[0] == 'unauthorized'
