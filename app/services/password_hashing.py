from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
	"""
	Hashing password

	password -- Real password
	"""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
	"""
	Verification password

	password -- The candidate password
	hashed -- Hash from real password
	"""
    return pwd_context.verify(password, hashed)