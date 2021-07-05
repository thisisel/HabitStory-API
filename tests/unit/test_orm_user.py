from app.db.models import UserModel

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    user = UserModel('patkennedy79@gmail.com', 'FlaskIsAwesome')
    assert user.email == 'patkennedy79@gmail.com'
    assert user.hashed_password != 'FlaskIsAwesome'
    assert user.role == 'user'
    assert user.__repr__() == '<User: patkennedy79@gmail.com>'
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous