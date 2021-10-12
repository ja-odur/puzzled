from abc import ABCMeta, abstractmethod


class AbstractConsumer(metaclass=ABCMeta):
    @abstractmethod
    def subscribe(self, id):
        pass

    @abstractmethod
    def unsubscribe(self):
        pass

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self):
        pass

    @abstractmethod
    def type(self):
        pass

    @classmethod
    def __subclasshook__(cls, sub):
        """Method to check for subclasses and instances (including virtual sub-classes) of AbstractConsumer

        :param sub (class): sub class to check
        :return: boolean True or NotImplemented
        """
        return (
                (
                        hasattr(sub, 'subscribe') and callable(sub.subscribe) and
                        hasattr(sub, 'unsubscribe') and callable(sub.unsubscribe) and
                        hasattr(sub, 'serialize') and callable(sub.serialize) and
                        hasattr(sub, 'deserialize') and callable(sub.deserialize) and
                        hasattr(sub, 'type') and callable(sub.type)
                )
                or NotImplemented
        )
