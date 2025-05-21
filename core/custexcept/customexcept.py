
class TemplateUseError(Exception):
    def __init__(self, message="Template Used Error. User correct pattern"):
        self.message = message
        super().__init__(self.message)

class PathTypeError(Exception):
    def __init__(self, message="Uncorrected path or file type"):
        self.message = message
        super().__init__(self.message)

class ParametersAssignError(Exception):
    def __init__(self, message="Cannot assign MODELS or START_CHAT"):
        self.message = message
        super().__init__(self.message)

class BadConnectionError(Exception):
    def __init__(self, message="Bad connection"):
        self.message = message
        super().__init__(self.message)

class GPUFindError(Exception):
    def __init__(self, message="Cannot search GPU or don't have video memory"):
        self.message = message
        super().__init__(self.message)