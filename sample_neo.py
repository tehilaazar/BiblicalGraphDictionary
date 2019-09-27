# must install via the command:
# pip3 install neomodel
# or using Settings / the plus sign
# pip3 install neomodel

# the following is heavily modified from the Getting Started from here:
# https://neomodel.readthedocs.io/en/latest/getting_started.html#defining-node-entities-and-relationships

from neomodel import db

from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom)

config.DATABASE_URL = 'bolt://neo4j:qwerty@localhost:7687'  # default
db.set_connection('bolt://neo4j:qwerty@localhost:7687')

class Country(StructuredNode):
    code = StringProperty(unique_index=True, required=True)
    inhabitant = RelationshipFrom('Person', 'INHABITANT_OF')

class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)

    # traverse outgoing IS_FROM relations, inflate to Country objects
    country = RelationshipTo('Country', 'IS_FROM')

jim = Person(name='Jim', age=3).save() # Create
jim.age = 4
jim.save() # Update, (with validation)
jim.delete()
#jim.refresh() # reload properties from the database
#print(jim.id) # neo4j internal id

# looking up Persons
all_nodes = Person.nodes.all()
for node in all_nodes:
    print(node)

# Returns Person by Person.name=='Jim' or raises neomodel.DoesNotExist if no match
jim = Person.nodes.get(name='Jim')
print(jim)

# Will return None unless "bob" exists
someone = Person.nodes.get_or_none(name='bob')

# Will return the first Person node with the name bob. This raises neomodel.DoesNotExist if there's no match.
#someone = Person.nodes.first(name='bob')

# Will return the first Person node with the name bob or None if there's no match
someone = Person.nodes.first_or_none(name='bob')

# Return set of nodes
people = Person.nodes.filter(age__gt=3)
for p in people:
    print(p)

germany = Country(code='DE').save()
jim.country.connect(germany)
germany.inhabitant.connect(jim)

if jim.country.is_connected(germany):
    print("Jim's from Germany")

for p in germany.inhabitant.all():
    print(p.name) # Jim
