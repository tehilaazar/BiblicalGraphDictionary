from neomodel import db

from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom, Relationship)

# config.DATABASE_URL = 'bolt://neo4j:qwerty@localhost:7687'  # default
# db.set_connection('bolt://neo4j:qwerty@localhost:7687')

config.DATABASE_URL = 'bolt://neo4j:qwerty@172.104.219.113:7687'  # default
db.set_connection('bolt://neo4j:qwerty@172.104.219.113:7687')


class Shoresh(StructuredNode):
    heName = StringProperty(unique_index=True, required=True)
    enName = StringProperty(unique_index = True, required=True)
    similarity = Relationship('Shoresh', 'IS_SIMILAR')

class ClarkPhonemicClass(StructuredNode):
    group = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index = True, required=True)

class ClarkShoresh(StructuredNode):
    root = StringProperty(unique_index=True, required=True)
    meaning = StringProperty(unique_index=True, required=True)
    memberOf = RelationshipTo('ClarkPhonemicClass', 'MEMBER_OF')







