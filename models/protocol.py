from models.base import Base, PHMixin


class Protocol(PHMixin, Base):
    __tablename__ = 'protocol'

    def __init__(self, **kwargs):
        kwargs.pop('content', None)
        super(Protocol, self).__init__(**kwargs)

    def get_content(self):
        return 'test'
