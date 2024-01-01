from app_logger import logger

from .messages import ErrorMessages
from .exceptions import NotAValidInteger
from .structs import Member


class TreeParser:

    def __init__(self, json_data):
        self.data = json_data

    def _get_int_value(self, val: str|int) -> int|Exception:
        """
        Returns a custom exception or int value
        while converting given string input 

        Args:
            val (str|int): value

        Raises:
            Exception: Exceptin

        Returns:
            int|Exception: Integer value repective of input
        """
        try:
            return int(val)
        except ValueError as err:
            logger.error(
                f"Error occured while converting {val} to integer", 
                stack_info=True,
                exc_info=True,
            )
            raise NotAValidInteger()

    def _get_node(self, data: dict, level: int = 0) -> Member|None: 
        """
        Returns a member node or none, while analysing and validating
        the given input

        Args:
            data (dict): Members structure
            level (int): level of the member in the tree

        Returns:
            Member|None: A member node
        """

        name = data.get("Name", "NoName")

        try:
            birth_year = self._get_int_value(data.get("BirthYear", "0"))
        except NotAValidInteger:
            logger.error(
                f"Member failing the validation of having data : {data}",
            )
            raise NotAValidInteger(f"BirthYear : Value is not a valid integer")
        
        try:
            death_year = self._get_int_value(data.get("DeathYear", "0"))
        except NotAValidInteger:
            logger.error(
                f"Member failing the validation of having data : {data}",
            )
            raise NotAValidInteger(f"DeathYear : Value is not a valid integer")
        

        if birth_year > death_year:
            logger.info(ErrorMessages.InvalidLifeSpan)
            logger.error(
                f"Member failing the validation of having data : {data}",
            )
            return None
        
        return Member(name, birth_year, death_year, level=level+1)
        

    
    def _build_tree(self, json_data, par=None) -> Member:
        """
        Builds the tree recusively

        Args:
            json_data (dict): Input data as dict
            par (Member, optional): Parent Member Node. Defaults to None.

        Returns:
            Memeber: Return complete tree
        """
    
        if isinstance(json_data, dict):
            node = self._get_node(json_data, par.level if par else 0)
            members = json_data.get("Members", [])
            for member_data in members:
                child = self._build_tree(member_data, node)
                if child:
                    node.members.append(child)

            return node

        elif isinstance(json_data, list):
            for item in json_data:
                child = self._build_tree(item, par)
                if child:
                    par.members.append(child)
            return par
        else:
            node = self._get_node(json_data, par.level if par else 0)
            return None

    def get_tree(self):
        """
        Returns parent node of the tree, after building it
        """
        
        par = Member(name = self.data["lineage"]["FamilyTree"])
        self._build_tree(self.data["lineage"]["Members"], par=par)
        return par
