from .structs import Member


class MemberManager:
    """Utitility function related to lineage and their members"""

    def __init__(self, root: Member) -> None:
        self.root = root
        self.members = list()
        self.has_flatten = False
        self.all_paths = []
        self.has_all_paths = False

    def _flatten(self, member, result=list()) -> list[Member]:
        """Flattens the tree"""
        
        if member:
            result.append(member)
            for child in member.members:
                self._flatten(child, result)
        return result

    def flatten(self) -> list[Member]:
        """Flattens the tree of members into a list"""
        
        if self.has_flatten:
            return self.members
        
        par = self.root
        res = self._flatten(par)

        # poping first item as it is par
        if res:
            res = res[1:]

        self.members = res
        self.has_flatten = True
        return self.members
    
    def sort(self, reverse=False) -> list[Member]:
        """For sorting according to memebers age"""
        
        members = self.members[:]
        members.sort(reverse=reverse)
        return members
    
    def get_sorted_members(self) -> list[Member]:
        """Returns sorted list of members"""
        
        members = self.members
        members.sort()
        return members
    
    def print_members(self) -> str:
        """Returns output as string for all members"""
        
        members = self.flatten()

        out = ""
        for id, member in enumerate(members):
            out += str(member) + "\n"
        return out

    def _get_all_paths(self, node, current_path=[]) -> None:
        """Fetches all the paths in a tree"""
        
        if node:
            current_path.append(node)
            if not node.members:
                self.all_paths.append(current_path.copy()[1:])
            for child in node.members:
                self._get_all_paths(child, current_path.copy())

    def get_all_paths(self) -> list[Member]:
        """
        Returns all the paths in a tree
        Avoids recomputation
        """
        
        if self.has_all_paths:
            return self.all_paths
        
        par = self.root
        self._get_all_paths(par)
        self.has_all_paths = True

        # Sorting via length
        self.all_paths = sorted(self.all_paths, key=len)
        return self.all_paths    
    
    def print_all_paths(self) -> str:
        """Reuturn strings containing all the paths"""

        all_paths = self.get_all_paths()
        out = ""
        for path in all_paths:
            out += str(path) + "\n"
        return out

    def get_lineage_period(self) -> tuple[int, int]:
        """Return tuple for period of the lineage"""

        members = self.flatten()

        _min = 10e+10
        _max = -_min

        for member in members:
            _min = min(_min, member.birth_year)
            _max = max(_max, member.death_year)

        return (_min, _max)
    
    def get_youngest_died(self) -> Member:
        """Returns youngest members of lineage"""

        members = self.get_sorted_members()
        return members[0]
    
    def get_oldest_to_live(self) -> Member:
        """Returns olders member to live in lineage"""

        members = self.get_sorted_members()
        return members[-1]
    
    def get_mean_age(self):
        """Returns mean age"""

        members = self.flatten()

        tot = 0
        for member in members:
            tot += member.age
        
        return tot / len(members)

    def get_meadian_age(self):
        """Return meadian age"""

        members = self.get_sorted_members()
        length = len(members)

        if length % 2 == 1:
            # If the list has an odd number of elements
            median = members[length // 2].age
        else:
            # If the list has an even number of elements
            middle1 = members[(length // 2) - 1].age
            middle2 = members[length // 2].age
            median = (middle1 + middle2) / 2

        return median
    
    # TODO : implement grouping using IQR
