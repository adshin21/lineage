# To keep all the classes

class Member:
    """
    Stores the info about the memeber and provides
    helper functions
    *_year = 0 represents it as a parent node
    """
    def __init__(
            self, 
            name : str = "", 
            birth_year : int = 0, 
            death_year : int = 0, 
            level : int = 0
    ) -> None:
        self.name = name
        self.birth_year = birth_year
        self.death_year = death_year
        self.members = list()
        self.level = level
        self.id = id(self)
    
    def __str__(self) -> str:
        return f"{{Name: {self.name} Age: {self.age}}}"
    
    def __repr__(self) -> str:
        return f"{{Name: {self.name} Age: {self.age}}}"
    
    @property
    def age(self) -> int:
        return self.death_year - self.birth_year
    
    def __gte__(self, other):
        if not isinstance(other, Member):
            raise NotImplementedError()
        
        if self.age == other.age:
            return self.birth_year < other.birth_year
        if self.age > other.age:
            return True
        else:
            return False

    def __lte__(self, other):
        if not isinstance(other, Member):
            raise NotImplementedError()
        if self.age == other.age:
            return self.birth_year > other.birth_year
        
        if self.age > other.age:
            return False
        return True
    
    # required to have .sort() compatible
    def __lt__(self, other):
        if not isinstance(other, Member):
            raise NotImplementedError()
        
        if self.age == other.age:
            return self.birth_year > other.birth_year
        
        if self.age > other.age:
            return False
        return True
