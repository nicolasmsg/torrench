import abc


class BaseModule(metaclass=abc.ABCMeta):

  def __init__(self):
    pass

  @abc.abstractmethod
  def select_torrent(self):
    """TODO"""