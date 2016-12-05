from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "DAS USER MODEL"


Base.metadata.create_all(engine)

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')

# this custom-made Session class will create new Session objects which are bound to our database
Session = sessionmaker(bind=engine)

# then whenever you need to have a conversation with the database, you instantiate a Session
session = Session()
# the above Session is associated with our SQLite-enabled Engine, but it hasn't opened any connections yet.
# When it's first used, it retrieves a connection from a pool of connections maintained by the Engine,
# and holds onto it until we commit all changes and/or close the session object.

# To persist our User object, we add() it to our Session:
session.add(ed_user)
# at this point, we say that the instance is pending, no SQL has yet been issued and
# the object is not yet represented by a row in the database.
# The Session will issue the SQL to persist "Ed Jones" as soon as is needed, using a process known as a flush.
# If we query the database for "Ed Jones", all pending information will first be flushed,
# and the query is issued immediately thereafter.

session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')
])

ed_user.password = 'f8s7ccs'

# We tell the Session that we'd like to issue all remaining changes to the database and commit the transaction, which
# has been in progr
# ess throughout.
session.commit()
# this flushes whatever remaining changes remain to the database, and commits the transaction
# The connection resources referenced by the session are now returned to the connection pool.




