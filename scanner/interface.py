from abc import abstractmethod


class ITagScanner:
    @abstractmethod
    def scan_by_tag(self, tag: str, limit: int = 50):
        pass


class ITypeScanner:
    @abstractmethod
    def scan_by_type(self, file_type: str, limit: int = 50):
        pass
