    
class ImageURLExtractor(InformationBase):
        
    def X_train_data(self, object):
        print (object)
        return
    
    def Y_train_data(self, object):
        print (object)
        return
    
    def X_action_data(self, object):
        print (object)
        return   
    
e = ImageURLExtractor()
e.X_train_data("sdfdsf")


# In[18]:

import abc
from cStringIO import StringIO

class ABCWithConcreteImplementation(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def retrieve_values(self, input):
        print 'base class reading data'
        return input.read()

class ConcreteOverride(ABCWithConcreteImplementation):
    
    def retrieve_values(self, input):
        base_data = super(ConcreteOverride, self).retrieve_values(input)
        print 'subclass sorting data'
        response = sorted(base_data.splitlines())
        return response

input = StringIO("""line one
line two
line three
""")

reader = ConcreteOverride()
print reader.retrieve_values(input)
print


# In[ ]:



