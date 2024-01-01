import json
from app_logger import logger

from famtree.manager import MemberManager
from famtree.treeparser import TreeParser

def run(data):
    tp = TreeParser(data)

    par = tp.get_tree()

    out = "\nb. All Lines\n"
    memeber_manager = MemberManager(par)
    out += memeber_manager.print_all_paths() + '\n'

    # get all paths to print smallest and largest lines
    all_lines = memeber_manager.get_all_paths()

    # Since it is sorted
    out += "\nb. 1. Shortest line\n"
    out += ' -> '.join([str(line) for line in all_lines[0]]) + "\n"


    out += "\nb. 2. Largest line\n"
    out += ' -> '.join([str(line) for line in all_lines[-1]]) + "\n"

    out += "\nc. All Memebers\n"
    out += memeber_manager.print_members() + "\n"

    out += "\nd. Ordered Age\n"
    out += ', '.join([str(member) for member in memeber_manager.sort()]) + "\n"

    out += "\ne. Lineage Active Range \n"
    out += str(memeber_manager.get_lineage_period()) + "\n"

    out += "\nf. Mean Age \n"
    out += str(memeber_manager.get_mean_age()) + "\n"

    out += "\ng. Median Age \n"
    out += str(memeber_manager.get_meadian_age()) + "\n"


    out += "\ni. 1. Younges to die \n"
    out += str(memeber_manager.get_youngest_died()) + "\n"

    out += "\ni. 2. Oldest to live \n"
    out += str(memeber_manager.get_oldest_to_live()) + "\n"

    return out    

if __name__ == '__main__':
    logger.info(f"Starting app ...")

    # TODO : Add dir walk and write support
    with open("famtree/inputs/familytree 4.json") as fp:
        data = json.loads(fp.read())

    res = run(data)
    
    with open("famtree/outputs/output.txt", "w+") as file:
        file.write(res)
    