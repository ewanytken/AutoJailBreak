
class TemplateUseError(Exception):
    def __init__(self, message="Template Used Error. User correct pattern"):
        self.message = message
        super().__init__(self.message)


class PathTypeError(Exception):
    def __init__(self, message="Uncorrected path or file type"):
        self.message = message
        super().__init__(self.message)

