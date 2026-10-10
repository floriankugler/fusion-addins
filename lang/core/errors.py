class LangError(Exception):
    """An error in a build, naming the part it concerns.

    `path` is the dotted path of the part or scope (`kitchen.drawer2.left`)
    or None for errors outside any part."""

    def __init__(self, message: str, path: str | None = None):
        self.path = path
        self.message = message
        super().__init__(f"{path}: {message}" if path else message)
