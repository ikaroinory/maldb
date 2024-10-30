from abc import abstractmethod
from typing import Any, Callable, Iterator, List

from tqdm import tqdm


class ApiKey:
    def __init__(self, key_list: List[str]) -> None:
        self.key_index: int = 0
        self.key_list: List[str] = key_list
        self.start_index: int = 0

    def get_key(self) -> str | None:
        if self.key_index == len(self.key_list):
            return None
        else:
            return self.key_list[self.key_index]

    def get_key_next(self) -> str:
        key = self.get_key()
        self.key_index += 1
        return key

    def key_iter(self) -> Iterator[str]:
        for key in self.key_list:
            yield key

    def run2key(self, func: Callable[[str, Any], bool], item_list: list) -> bool:
        key = self.get_key_next()
        if key is None:
            return False

        for item in tqdm(item_list):
            while key is not None:
                if func(key, item):
                    break
                else:
                    key = self.get_key_next()
            if key is None:
                break

        return key is not None


class SampleDownloader:
    def __init__(self, download_path: str):
        self.download_path = download_path

    @abstractmethod
    def download(self):
        pass
