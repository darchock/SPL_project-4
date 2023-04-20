import persistence
from persistence import *

import sys

def main(args : list[str]):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            #TODO: apply the action (and insert to the table) if possible
            activityObj = Activitie(*splittedline)


            product = repo.products.find(id = activityObj.product_id)[0]
            if int(product.quantity) + int(activityObj.quantity) >= 0: # if it's a supply arrival quantity > 0, if it's a sell quantity < 0
                _new_val = int(product.quantity) + int(activityObj.quantity)
                persistence.repo.products.update(id = activityObj.product_id, new_val = _new_val)
                persistence.repo.activities.insert(activityObj)





if __name__ == '__main__':
    main(sys.argv)