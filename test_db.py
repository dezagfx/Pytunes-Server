from database.models import User

u = User.get_by_name('kjhgf')
print(u)