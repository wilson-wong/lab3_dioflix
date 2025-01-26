import uuid

class MovieRequest:
    def __init__(self, title: str, year: int, video: str, thumbnail: str):
        self.id = str(uuid.uuid4())
        self.title = title
        self.year = year
        self.video = video
        self.thumbnail = thumbnail

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "video": self.video,
            "thumbnail": self.thumbnail
        }