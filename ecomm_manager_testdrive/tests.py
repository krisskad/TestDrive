import inspect
from ecomm_manager_testdrive.utils import (
    send_test_csv_report,
    send_mail,
    get_user_token,
    get_data_listing,
    flatten,
    diff,
    store_test_logs
    )
from django.core.validators import URLValidator
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient, APITestCase, APISimpleTestCase, APITransactionTestCase
from django.test import TestCase, TransactionTestCase, LiveServerTestCase

from rest_framework import status
import requests
import json
import datetime
from .models import TestLog


# BASE URL of the API
URL = "https://category-insights.ongil.io/"

# Mention the email & password from you want to test all API's
EMAIL = 'gokulkrishnan@ongil.io'
PASSWORD = 'Admin@123'

# Making user token global
try:
    TOKEN = get_user_token(
        email=EMAIL,
        password=PASSWORD
    )

    HEADER = {
      'Authorization': f'Token {TOKEN}',
      'Content-Type': 'application/json'
    }

    PROFILE_DATA = get_data_listing(URL+'api/v1/profile/', HEADER)
except Exception as e:
    print(e)


class GetTokenAPITestCase(TestCase):
    """
    Test Cases:
        Status code
        JSON validation
        Response time
        Json Response
        Link checker
    """
    def setUp(self) -> None:
        self.url = URL + 'api/v1/user/login/'
        # self.test_name = inspect.currentframe().f_code.co_name
        self.test_name = 'User Token'
        self.test_description = f"Generating Access token for user: {EMAIL}",
        self.request_method = "POST"
        self.header = HEADER

        self.payload = {
            'email': EMAIL,
            'password': PASSWORD
        }

    @classmethod
    def tearDownClass(cls):
        pass

    def test_run(self):
        self.setup_logs()
        if self.request_method.lower() == "get":
            self.get()
        elif self.request_method.lower() == "post":
            self.post()

        self.status_code()
        self.json_validation()
        self.response_time()
        self.link_checker()
        self.database()
        # self.mail_test_logs()

    def setup_logs(self):
        self.logs = {
            "api_endpoint": self.url,
            "test_name":self.test_name,
            "test_description":self.test_description,
            "exception":[],
            "request_method":self.request_method,
            "json_payload": self.payload
        }

    def get(self):
        self.response = requests.get(self.url, headers=self.header)

    def post(self):
        self.response = requests.post(self.url, data=self.payload)

    def status_code(self):
        """
        In this Test Case we are testing the 'api/v1/user/login/'.
        """
        exception = None
        is_passed = False

        try:
            # Write your code here
            is_passed = self.response.status_code == status.HTTP_200_OK
            self.logs["json_response"] = self.response.json()
        except Exception as e:
            exception = e

        # Database
        self.logs["status_code"] = is_passed
        self.logs["exception"].append(exception)

    def json_validation(self):
        """
        In this Test Case we are validating json keys.
        """

        exception = None
        is_passed = False

        try:
            # Write your code here
            is_passed = "token" in self.response.json()
        except Exception as e:
            exception = e

        # Database
        self.logs["json_validation"] = is_passed
        self.logs["exception"].append(exception)

    def response_time(self):
        """
        In this Test Case we are testing the 'api/v1/user/login/'.
        """
        exception = None
        response_time = 0
        try:
            # Write your code here
            response_time = self.response.elapsed.total_seconds()
        except Exception as e:
            exception = e

        # Database
        self.logs["response_time"] = response_time
        self.logs["exception"].append(exception)

    def link_checker(self):
        """
        In this Test Case we are testing the 'api/v1/user/login/'.
        """
        exception = None
        is_passed = False

        validator = URLValidator()
        try:
            validator(self.url)
            is_passed = True
        except ValidationError as e:
            exception = e

        # Database
        self.logs["link_checker"] = is_passed
        self.logs["exception"].append(exception)

    def database(self):
        self.logs["exception"] = list(set(self.logs["exception"]))
        self.logs["result"] = all([
                self.logs["status_code"],
                self.logs["json_validation"],
                self.logs["link_checker"]
            ])
        store_test_logs(self.logs)

    def mail_test_logs(self):
        send_mail(self.logs)


class GetProfileDataTestCase(TestCase):
    """
    Test Cases:
        Status code
        JSON validation
        Response time
        Json Response
        Link checker
    """
    def setUp(self) -> None:
        self.url = URL + 'api/v1/profile/'
        # self.test_name = inspect.currentframe().f_code.co_name
        self.test_name = 'Get User Profile'
        self.test_description = f"Getting User Profile Information of: {EMAIL}",
        self.request_method = "GET"
        self.header = HEADER

        self.payload = {}

    @classmethod
    def tearDownClass(cls):
        pass

    def test_run(self):
        self.setup_logs()
        if self.request_method.lower() == "get":
            self.get()
        elif self.request_method.lower() == "post":
            self.post()

        self.status_code()
        self.json_validation()
        self.response_time()
        self.link_checker()
        self.database()
        # self.mail_test_logs()

    def setup_logs(self):
        self.logs = {
            "api_endpoint": self.url,
            "test_name":self.test_name,
            "test_description":self.test_description,
            "exception":[],
            "request_method":self.request_method,
            "json_payload":self.payload
        }

    def get(self):
        self.response = requests.get(self.url, headers=self.header)

    def post(self):
        self.response = requests.post(self.url, data=self.payload)

    def status_code(self):
        """
        In this Test Case we are testing the 'api/v1/profile/'.
        """
        exception = None
        is_passed = False

        try:
            # Write your code here
            is_passed = self.response.status_code == status.HTTP_200_OK
            self.logs["json_response"] = self.response.json()
        except Exception as e:
            exception = e

        # Database
        self.logs["status_code"] = is_passed
        self.logs["exception"].append(exception)

    def json_validation(self):
        """
        In this Test Case we are validating json keys.
        """
        exception = None
        is_passed = False

        try:
            # Write your code here
            profile = self.response.json()
            # List of clients
            CLIENTS = list(profile["profileData"]["clients"].keys())

            # List of Countries
            COUNTRIES = flatten(
                [list(profile["profileData"]["country_retailer_access"][x]["countries_access"].keys()) for x in
                 CLIENTS])

            # List Of Retailers
            RETAILERS = []
            for cli in CLIENTS:
                country = profile["profileData"]["country_retailer_access"][cli]["retailer_access"].keys()
                for ctry in country:
                    RETAILERS += profile["profileData"]["country_retailer_access"][cli]["retailer_access"][ctry]
            is_passed = True
        except Exception as e:
            exception = e

        # Database
        self.logs["json_validation"] = is_passed
        self.logs["exception"].append(exception)

    def response_time(self):
        """
        In this Test Case we are testing the 'api/v1/profile/'.
        """
        exception = None
        response_time = 0
        try:
            # Write your code here
            response_time = self.response.elapsed.total_seconds()
        except Exception as e:
            exception = e

        # Database
        self.logs["response_time"] = response_time
        self.logs["exception"].append(exception)

    def link_checker(self):
        """
        In this Test Case we are testing the 'api/v1/profile/'.
        """
        exception = None
        is_passed = False

        validator = URLValidator()
        try:
            validator(self.url)
            is_passed = True
        except ValidationError as e:
            exception = e

        # Database
        self.logs["link_checker"] = is_passed
        self.logs["exception"].append(exception)

    def database(self):
        self.logs["exception"] = list(set(self.logs["exception"]))
        self.logs["result"] = all([
                self.logs["status_code"],
                self.logs["json_validation"],
                self.logs["link_checker"]
            ])
        store_test_logs(self.logs)

    def mail_test_logs(self):
        send_mail(self.logs)


class CategoryBrandListTestCase(TestCase):
    """
    Test Cases:
        Status code
        JSON validation
        Response time
        Json Response
        Link checker
    """
    def setUp(self) -> None:
        self.url = URL + 'api/v1/category-brand-list'
        # self.test_name = inspect.currentframe().f_code.co_name
        self.test_name = 'Category Brand List API'
        self.test_description = f"Category Brand List API Testing with" \
                                f"all the combination of retailer, client and country" \
                                f"generated from {EMAIL} profile data",
        self.request_method = "POST"
        self.header = HEADER

        self.data = get_data_listing(URL+'api/v1/profile/', self.header)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_run(self):
        # running test for every payload
        combinations = self.data["combinations"]
        for client, country, retailer in combinations:
            self.payload = {
                "client": client,
                "country": country,
                "retailer": retailer
            }
            self.setup_logs()
            if self.request_method.lower() == "get":
                self.get()
            elif self.request_method.lower() == "post":
                self.post()

            self.status_code()
            self.json_validation()
            self.response_time()
            self.link_checker()
            self.database()
            # self.mail_test_logs()

    def setup_logs(self):
        self.logs = {
            "api_endpoint": self.url,
            "test_name":self.test_name,
            "test_description":self.test_description,
            "exception":[],
            "request_method":self.request_method,
            "json_payload":self.payload
        }

    def get(self):
        self.response = requests.get(self.url, headers=self.header)

    def post(self):
        # print(self.payload)
        self.response = requests.post(self.url, data=json.dumps(self.payload), headers=self.header)
        # print(self.response)

    def status_code(self):
        """
        In this Test Case we are testing the 'api/v1/category-brand-list'.
        """
        exception = None
        is_passed = False

        try:
            # Write your code here
            is_passed = self.response.status_code == status.HTTP_200_OK
            self.logs["json_response"] = self.response.json()
        except Exception as e:
            exception = e

        # Database
        self.logs["status_code"] = is_passed
        self.logs["exception"].append(exception)

    def json_validation(self):
        """
        In this Test Case we are validating json keys.
        """
        exception = None
        is_passed = False

        try:
            fetched = TestLog.objects.filter(json_payload__iexact=self.payload)
            if fetched.exists():
                golden_json = list(fetched.values_list("json_response", flat=True).distinct())[-1]

                if self.logs["json_response"] == golden_json:
                    is_passed = True
                else:
                    is_passed = False
            else:

                # Write your code here
                if "brand" in self.logs["json_response"] and "category" in self.logs["json_response"]:
                    is_passed = True
                else:
                    is_passed = False

        except Exception as e:
            exception = e

        # Database
        self.logs["json_validation"] = is_passed
        self.logs["exception"].append(exception)

    def response_time(self):
        """
        In this Test Case we are testing the 'api/v1/category-brand-list'.
        """
        exception = None
        response_time = 0
        try:
            # Write your code here
            response_time = self.response.elapsed.total_seconds()
        except Exception as e:
            exception = e

        # Database
        self.logs["response_time"] = response_time
        self.logs["exception"].append(exception)

    def link_checker(self):
        """
        In this Test Case we are testing the 'api/v1/category-brand-list'.
        """
        exception = None
        is_passed = False

        validator = URLValidator()
        try:
            validator(self.url)
            is_passed = True
        except ValidationError as e:
            exception = e

        # Database
        self.logs["link_checker"] = is_passed
        self.logs["exception"].append(exception)

    def database(self):
        self.logs["exception"] = list(set(self.logs["exception"]))
        self.logs["result"] = all([
                self.logs["status_code"],
                self.logs["json_validation"],
                self.logs["link_checker"]
            ])
        store_test_logs(self.logs)

    def mail_test_logs(self):
        send_mail(self.logs)


# class TestAPI:
#     """
#     Test Cases:
#         Status code
#         JSON validation
#         Response time
#         Json Response
#         Link checker
#     """
#     def __init__(self, url=None, test_name=None, test_description=None, request_method=None, header=None, payload=None):
#         self.client = APIClient()
#         self.url = url
#         self.test_name = test_name
#         self.test_description = test_description
#         self.request_method = request_method
#         self.header = header
#
#         self.logs = {"exception":[]}
#         db = TestLog()
#
#     def run(self):
#         if self.request_method.lower() == "get":
#             self.get()
#         elif self.request_method.lower() == "post":
#             self.post()
#
#         self.test_status_code()
#         self.test_json_validation()
#         self.test_response_time()
#         self.test_link_checker()
#         self.database()
#
#     def database(self):
#         # Send Test logs on EMAILS
#         # send_mail(TEST_RESULTS)
#
#         # Save logs into Database
#         db.api_endpoint = self.url
#         db.json_response = self.response.json()
#         db.request_method = self.request_method
#         db.result= all([
#             self.logs["status_code"],
#             self.logs["json_validation"],
#             self.logs["link_checker"]
#         ])
#         db.exception= self.logs["exception"]
#         db.status_code= self.logs["status_code"]
#         db.save()
#         print("Data Saved: ", db)
#
#     def get(self):
#         self.response = requests.get(self.url, headers=self.header)
#
#     def post(self):
#         self.response = requests.post(self.url, headers=self.header, data = self.payload)
#
#     def test_status_code(self):
#         """
#         In this Test Case we are testing the 'api/v1/profile/'.
#         """
#         exception = None
#         is_passed = False
#
#         try:
#             # Write your code here
#             is_passed = self.response.status_code == status.HTTP_200_OK
#         except Exception as e:
#             exception = e
#
#         # Database
#         self.logs["status_code"] = is_passed
#         self.logs["exception"].append(exception)
#
#     def test_json_validation(self):
#         """
#         In this Test Case we are validating json keys.
#         """
#
#         exception = None
#         is_passed = False
#
#         try:
#             # Write your code here
#             profile = self.response.json()
#             # List of clients
#             CLIENTS = list(profile["profileData"]["clients"].keys())
#
#             # List of Countries
#             COUNTRIES = flatten(
#                 [list(profile["profileData"]["country_retailer_access"][x]["countries_access"].keys()) for x in
#                  CLIENTS])
#
#             # List Of Retailers
#             RETAILERS = []
#             for cli in CLIENTS:
#                 country = profile["profileData"]["country_retailer_access"][cli]["retailer_access"].keys()
#                 for ctry in country:
#                     RETAILERS += profile["profileData"]["country_retailer_access"][cli]["retailer_access"][ctry]
#             is_passed = True
#         except Exception as e:
#             exception = e
#
#         # Database
#         self.logs["json_validation"] = is_passed
#         self.logs["exception"].append(exception)
#
#     def test_response_time(self):
#         """
#         In this Test Case we are testing the 'api/v1/user/login/'.
#         """
#         exception = None
#         is_passed = False
#
#         try:
#             # Write your code here
#             is_passed = self.response.elapsed.total_seconds() <= 2
#         except Exception as e:
#             exception = e
#
#         # Database
#         self.logs["response_time"] = is_passed
#         self.logs["exception"].append(exception)
#
#     def test_link_checker(self):
#         """
#         In this Test Case we are testing the 'api/v1/profile/'.
#         """
#         exception = None
#         is_passed = False
#
#         try:
#             validate = URLValidator(verify_exists=True)
#             is_passed = validate(self.url)
#         except Exception as e:
#             exception = e
#
#         # Database
#         self.logs["link_checker"] = is_passed
#         self.logs["exception"].append(exception)
#

# if __name__ == '__main__':
#     a = TestAPI(
#         url=URL + 'api/v1/profile/',
#         test_name="User Profile",
#         test_description=f"Testing User Profile API of {EMAIL}",
#         request_method="GET",
#         header=HEADER
#     )
#
#     a.run()