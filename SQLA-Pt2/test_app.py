import pytest
from app import app, db
from models import User, Post  # Assuming you have these models

@pytest.fixture
def client():
    """Fixture to set up and tear down the Flask test client."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a test DB
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # Create a test user and post
            user = User(first_name='Test', last_name='User', image_url='test.jpg')
            db.session.add(user)
            db.session.commit()

            post = Post(title='Test Post', content='This is a test post.', user_id=user.id)
            db.session.add(post)
            db.session.commit()

            yield client  # Provide the test client for testing

            db.session.remove()
            db.drop_all()

def test_create_post(client):
    """Test the /users/<user_id>/posts/new route to create a new post."""
    # Get the user created in the fixture
    user = User.query.first()

    # Test POST request to create a new post
    response = client.post(f'/users/{user.id}/posts/new', data={
        'title': 'New Post',
        'content': 'This is a newly created post.'
    })
    assert response.status_code == 302  # Expecting a redirect after successful post creation
    assert response.location == f'/users/{user.id}'  # Redirect to user page


# Test case for viewing a single post
def test_view_single_post(client):
    """Test the /posts/<id> route to ensure it shows the correct post."""
    # Get the post created in the fixture
    response = client.get('/posts/1')  # Assuming the post ID is 1
    assert response.status_code == 200
    assert b'Test Post' in response.data  # Check if the post title appears in the response
    assert b'This is a test post.' in response.data  # Check post content

def test_edit_post(client):
    """Test the /posts/<post_id>/edit route to edit an existing post."""
    # Get the post created in the fixture
    post = Post.query.first()

    # Test POST request to edit the post
    response = client.post(f'/posts/{post.id}/edit', data={
        'title': 'Updated Title',
        'content': 'Updated content for the post.'
    })
    assert response.status_code == 302  # Expecting a redirect after successful edit
    assert response.location == f'/posts/{post.id}'  # Redirect to the updated post
