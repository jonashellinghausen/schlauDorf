from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize limiter with function to retrieve remote address
limiter = Limiter(key_func=get_remote_address)
