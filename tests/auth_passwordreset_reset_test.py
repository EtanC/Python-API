import pytest
import imaplib, ssl, re
from src.error import InputError, AccessError
from fake.auth import auth_passwordreset_request, auth_passwordreset_reset, auth_register, auth_login
from fake.channels import channels_create
from fake.other import clear
from json import dumps
from src.config import RESET_CODE_LENGTH, DUMMY_EMAIL, DUMMY_PASSWORD

@pytest.fixture(autouse=True)
def reset_data():
    clear()

@pytest.fixture
def user1():
    user = auth_register(
        DUMMY_EMAIL, 'Password1', 'John', 'Smith'
    )
    return user

def setup_imap_server(email, password):
    # Setup context
    context = ssl.create_default_context()
    # Initiate ssl connection
    server = imaplib.IMAP4_SSL(host='imap.gmail.com', port=993, ssl_context=context)
    # Login with valid credentials
    server.login(email, password)
    # Select mailbox (if no arguments provided, defaults to selecting "Inbox")
    server.select()
    return server

def get_reset_code(server):
    # Get all messages in inbox
    _, ids = server.search(None, 'ALL')
    # Get message id of most recent email (most likely the one Streams has sent)
    message_id = ids[0].split()[-1]
    # Retrieve message
    message = server.fetch(message_id, 'BODY[]')[1]
    body = message[0][1].decode('utf-8')
    # Check the subject of the email
    returnlist = re.search(r'Subject:[A-Za-z ]*', body)
    # Verify that this is the email sent from Streams app
    #-------------------------------------------------------------------
    # TODO: make sure these hard coded pieces of text go into config.py
    #-------------------------------------------------------------------
    if returnlist[0] == "Subject:Streams password reset":
        # Read reset code
        returnlist = re.search(r'Your password reset code is: [0-9]*', body)
        reset_code = returnlist[0][-RESET_CODE_LENGTH:]
    # Delete email so that it doesnt clog up space
    server.store(message_id, '+FLAGS', '\\Deleted')
    server.expunge()
    return reset_code

# Test valid reset

def test_valid_passwordreset_reset(user1):
    auth_passwordreset_request(DUMMY_EMAIL)
    server = setup_imap_server(DUMMY_EMAIL, DUMMY_PASSWORD)
    reset_code = get_reset_code(server)
    with pytest.raises(InputError):
        auth_passwordreset_reset(reset_code, "new_password")
    auth_login(DUMMY_EMAIL, "new_password")

# Test invalid reset

def test_invalid_reset_code_passwordreset_reset(user1):
    with pytest.raises(InputError):
        auth_passwordreset_reset("123456", "new_password")

def test_short_password_passwordreset_reset(user1):
    auth_passwordreset_request(DUMMY_EMAIL)
    server = setup_imap_server(DUMMY_EMAIL, DUMMY_PASSWORD)
    reset_code = get_reset_code(server)
    with pytest.raises(InputError):
        auth_passwordreset_reset(reset_code, "pass")
