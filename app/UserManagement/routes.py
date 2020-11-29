from app.UserManagement import UserManagement

@UserManagement.route('/')
def hello_world():
    return "hello!"