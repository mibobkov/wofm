class EntityManager:
    def __init__(self, session):
        self.session = session

    def add(self, entity):
        self.session.add(entity)

    def getEntityByField(self, entClass, field, value):
        return self.session.query(entClass).filter_by(**{field: value}).first()

    def getAllByField(self, entClass, field, value):
        return self.session.query(entClass).filter_by(**{field: value})

    def delete(self, entity):
        self.session.delete(entity)

    def getAll(self, entClass):
        return self.session.query(entClass)

    def commit(self):
        self.session.commit()



