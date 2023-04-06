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
    