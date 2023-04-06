class ConcentVO():
    __conID = ""
    __p_date = ''
    __energy = 0
    __p_state = 0
    def __init__(self,conID):
        self.__conID = conID
    def getConID(self):
        return self.__conID
    
    def getDate(self):
        return self.__p_date
    
    def getEnergy(self):
        return self.__energy
    
    def getState(self):
        return self.__p_state
    
    def setConID(self,__conID):
        self.__conID = __conID
        return self.__conID
    
    def setDate(self,__p_date):
        self.__p_date = __p_date
        return self.__p_date
    
    def setEnergy(self,__energy):
        self.__energy = __energy
        return self.__energy
    
    def setState(self,__p_state):
        self.__p_state = __p_state
        return self.__p_state
    