import warnings
warnings.filterwarnings('ignore')
import os
from time import sleep
import requests
from bs4 import BeautifulSoup
import pickle
from urllib.parse import urlparse, unquote
from urllib.parse import parse_qs

class FacebookPostsScraper:

    # We need the email and password to access Facebook, and optionally the text in the Url that identifies the "view full post".
    def __init__(self, email, password,save_cookies, post_url_text='Xem thêm'):
        self.email = email
        self.save_cookies=save_cookies
        self.password = password
        self.headers = {  # This is the important part: Nokia C3 User Agent
            'User-Agent': 'NokiaC3-00/5.0 (07.20) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 AppleWebKit/420+ (KHTML, like Gecko) Safari/420+'
        }
        self.session = requests.session()  # Create the session for the next requests
        self.cookies_path = 'cookies/session_facebook.cki'  # Give a name to store the session in a cookie file.

        # At certain point, we need find the text in the Url to point the url post, in my case, my Facebook is in
        # English, this is why it says 'Full Story', so, you need to change this for your language.
        self.post_url_text = post_url_text

        # Evaluate if NOT exists a cookie file, if NOT exists the we make the Login request to Facebook,
        # else we just load the current cookie to maintain the older session.
        
        if self.new_session():
            self.login()

    # We need to check if we already have a session saved or need to log to Facebook
    def new_session(self):
        if not os.path.exists(self.cookies_path):
            return True

        f = open(self.cookies_path, 'rb')
        cookies = pickle.load(f)
        self.session.cookies = cookies
        return False

    # Utility function to make the requests and convert to soup object if necessary
    def make_request(self, url, method='GET', data=None, is_soup=True):
        if len(url) == 0:
            raise Exception(f'Empty Url')

        if method == 'GET':
            resp = self.session.get(url, headers=self.headers)
        elif method == 'POST':
            resp = self.session.post(url, headers=self.headers, data=data)
        else:
            raise Exception(f'Method [{method}] Not Supported')

        if resp.status_code != 200:
            raise Exception(f'Error [{resp.status_code}] > {url}')

        if is_soup:
            return BeautifulSoup(resp.text, 'lxml')
        return resp

    def login(self):
        url_home = "https://m.facebook.com/"
        soup = self.make_request(url_home)
        if soup is None:
            raise Exception("Couldn't load the Login Page")
        lsd = soup.find("input", {"name": "lsd"}).get("value")
        jazoest = soup.find("input", {"name": "jazoest"}).get("value")
        m_ts = soup.find("input", {"name": "m_ts"}).get("value")
        li = soup.find("input", {"name": "li"}).get("value")
        try_number = soup.find("input", {"name": "try_number"}).get("value")
        unrecognized_tries = soup.find("input", {"name": "unrecognized_tries"}).get("value")

        url_login = "https://m.facebook.com/login/device-based/regular/login/?refsrc=https%3A%2F%2Fm.facebook.com%2F&lwv=100&refid=8"
        payload = {
            "lsd": lsd,
            "jazoest": jazoest,
            "m_ts": m_ts,
            "li": li,
            "try_number": try_number,
            "unrecognized_tries": unrecognized_tries,
            "email": self.email,
            "pass": self.password,
            "login": "Iniciar sesión",
            "prefill_contact_point": "",
            "prefill_source": "",
            "prefill_type": "",
            "first_prefill_source": "",
            "first_prefill_type": "",
            "had_cp_prefilled": "false",
            "had_password_prefilled": "false",
            "is_smart_lock": "false",
            "_fb_noscript": "true"
        }
        soup = self.make_request(url_login, method='POST', data=payload, is_soup=True)
        if soup is None:
            print("Login failed! The login request couldn't be made")
            raise Exception(f"The login request couldn't be made: {url_login}")

        redirect = soup.select_one('a')
        if not redirect:
            print("Login failed. Please log in desktop/mobile Facebook and change your password")
            raise Exception("Please log in desktop/mobile Facebook and change your password")

        url_redirect = redirect.get('href', '')
        resp = self.make_request(url_redirect)
        if resp is None:
            print("The login request couldn't be made")
            raise Exception(f"The login request couldn't be made: {url_redirect}")
        if self.save_cookies==True:
            cookies = self.session.cookies
            f = open(self.cookies_path, 'wb')
            pickle.dump(cookies, f)

        return {'code': 200}

    def get_posts_from_profile(self, url_profile):
        # Prepare the Url to point to the posts feed
        if "www." in url_profile: url_profile = url_profile.replace('www.', 'm.')
        if 'v=timeline' not in url_profile:
            if '?' in url_profile:
                url_profile = f'{url_profile}&v=timeline'
            else:
                url_profile = f'{url_profile}?v=timeline'

        is_group = '/groups/' in url_profile

        # Make a simple GET request
        soup = self.make_request(url_profile)
        # return soup
        if soup is None:
            print(f"Couldn't load the Page: {url_profile}")
            return []
        else:
            return soup
    @staticmethod
    def convert_between_bs4_to_string(bs4_file):
        return str(bs4_file)
        
def run_get_cookies(email,password,single_profile):
    try:
        fps = FacebookPostsScraper(email,password,save_cookies=False)
        cookies = fps.get_posts_from_profile(single_profile)
        return FacebookPostsScraper.convert_between_bs4_to_string(cookies),single_profile
    except:
        return None,single_profile




