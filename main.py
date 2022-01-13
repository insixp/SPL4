from repository import REPOSITORY
from DAO import DAO
from DTO import Hat,Supplier,Order
import sys

def main():
    if(len(sys.argv) != 5):
        print("Usage: main.py <config> <orders> <output> <db>")
        return 0
    
    repository = REPOSITORY(sys.argv[4])
    repository.create_table()
    hats        = DAO(repository.getConnection(), Hat)
    suppliers   = DAO(repository.getConnection(), Supplier)
    orders      = DAO(repository.getConnection(), Order)
    order_id    = 1
    output      = ""

    #   Config
    with open(sys.argv[1], "r") as config_f:
        hats_s, suppliers_s = [int(s) for s in config_f.readline().strip().split(',')]
        for i in range(suppliers_s):
            suppliers.insert(Supplier(i+1, "Uninitialized"))
        for i in range(hats_s):
            hats.insert(Hat(i+1, "Uninitialized", 0, -1))

        #   Initialize every line   
        for line in config_f:
            parsed = line.strip().split(',')
            if(len(parsed) == 2):
                suppliers.update({"name":parsed[1]}, {"id":parsed[0]})
            elif(len(parsed) == 4):
                hats.update({"topping":parsed[1], "supplier":parsed[2], "quantity":parsed[3]}, {"id":parsed[0]})
            else:
                raise Exception("Invalid config file")
    
    with open(sys.argv[2], "r") as order_f:
        for order_l in order_f:
            order_loc, order_topping = order_l.strip().split(',')
            supply_options = hats.find({"topping":order_topping}, "supplier")
            if(len(supply_options) < 1):
                raise Exception("No suppliers available")
            supply_option = supply_options[0]
            orders.insert(Order(order_id, order_loc, supply_option.id))
            order_id += 1
            _supplier = suppliers.find({"id":supply_option.supplier})
            output += "{},{},{}\n".format(order_topping, _supplier[0].name, order_loc)
            if(supply_option.quantity > 1):
                supply_option.quantity -= 1
                hats.update({"quantity":supply_option.quantity}, {"id":supply_option.id})
            else:
                hats.delete(id=supply_option.id)

    with open(sys.argv[3], "w") as output_f:
        output_f.write(output)
            
    repository.commit()

if __name__ =="__main__":
    main()