from web.blueprints.login.views import blueprint as login
from web.blueprints.register.views import blueprint as register
from web.blueprints.home.views import blueprint as home
from web.blueprints.location.views import blueprint as location
from web.blueprints.logout.views import blueprint as logout
from web.blueprints.movement.views import blueprint as movement
from web.blueprints.product.views import blueprint as product
from web.blueprints.customer.views import blueprint as customer
from web.blueprints.Supplier.views import blueprint as Supplier

tenant_list = [login, register, home, location, logout, movement, product, customer, Supplier]
