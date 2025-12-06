from django.core.files.storage import FileSystemStorage
from .utils import normalize_filename

class NormalizedFileSystemStorage(FileSystemStorage):
    def get_valid_name(self, name):
        return normalize_filename(name)

