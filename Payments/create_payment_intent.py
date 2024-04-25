import stripe
import os
stripe.api_key = os.environ["STRIPE_ACCESS"]
id = "price_1P9RhdAQ31n3E5NFyOQlOm3M"
object = stripe.Product.list()
print(object)
