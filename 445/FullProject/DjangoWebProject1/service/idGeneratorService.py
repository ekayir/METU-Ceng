import uuid

class IdGeneratorService:
    def getNewId(self):
        id = uuid.uuid4()
        return str(id)