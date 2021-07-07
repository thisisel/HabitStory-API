from app.core.security.auth import UsersAuth
current_active_user = UsersAuth.get_fastapiusers().current_user(active=True)