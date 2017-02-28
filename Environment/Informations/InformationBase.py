from abc import ABCMeta, abstractmethod

class InformationBase:
    __metaclass__ = abc.ABCMeta
        
    @abstractmethod
    def X_train_data(self, object):
        pass
    
    @abstractmethod
    def Y_train_data(self, object):
        pass
    
    @abstractmethod
    def X_action_data(self, object):
        pass
    