from app.models.payment import Payment
from app.controllers import CoreController, CoreControllerOne

class PaymentController(CoreController):
    def __init__(self):
        super().__init__(Payment)

class PaymentControllerOne(CoreControllerOne):
    def __init__(self):
        super().__init__(Payment)
