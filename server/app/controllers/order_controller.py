from app.models.order import Order
from app.utils.core_controllers import CoreController, CoreControllerOne

class OrderController(CoreController):
    def __init__(self):
        super().__init__(Order)

class OrderControllerOne(CoreControllerOne):
    def __init__(self):
        super().__init__(Order)

# Instantiate controllers
order_controller = OrderController()
order_controller_one = OrderControllerOne()

# Function-based route handlers
def create_order():
    return order_controller.post()

def get_all_orders():
    return order_controller.get()

def get_order(order_id):
    return order_controller_one.get(order_id)

def update_order_status(order_id):
    return order_controller_one.patch(order_id)

def delete_order(order_id):
    return order_controller_one.delete(order_id)
