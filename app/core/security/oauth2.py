from httpx_oauth.clients.google import GoogleOAuth2
from ..config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

google_oauth_client = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)