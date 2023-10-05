

class BaseCommand:
    pass


class BaseEvent:
    pass


class BaseRepository:

    def __init__(self):
        self.seen = []


class BaseService:
    pass


class BaseUnitOfWork(BaseService):

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def get_events(self):
        for item in self.repository.seen:
            events = getattr(item, "events", [])
            while events:
                yield events.pop(0)
