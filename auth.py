
from models import User, UserRole


fake_users_db = {
    "alice": User(username="alice", role=UserRole.admin),
    "bob": User(username="bob", role=UserRole.viewer),
}
