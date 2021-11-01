import pytest
import imaplib, ssl, re
from src.error import InputError, AccessError
from fake.auth import auth_passwordreset_request, auth_passwordreset_reset, auth_register, auth_login
from fake.channels import channels_create
from fake.other import clear
from json import dumps
from src.config import RESET_CODE_LENGTH, DUMMY_EMAIL, DUMMY_PASSWORD

@pytest.fixture
def reset_data():
    clear()

@pytest.fixture
def user1():
    user = auth_register(
        'smithjohn177013@gmail.com', 'Password1', 'John', 'Smith'
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
    returnlist = re.findall(r'Subject:[A-Za-z ]*', body)
    # Verify that this is the email sent from Streams app
    #-------------------------------------------------------------------
    # TODO: make sure these hard coded pieces of text go into config.py
    #-------------------------------------------------------------------
    if returnlist[0] == "Subject:Streams password reset":
        # Read reset code
        returnlist = re.findall(r'Your password reset code is: [0-9]*', body)
        reset_code = returnlist[0][-RESET_CODE_LENGTH:]
    # Delete email so that it doesnt clog up space
    server.store(message_id, '+FLAGS', '\\Deleted')
    server.expunge()
    return reset_code

## VALID TEST NEEDS auth/passwordreset/reset/v1

# # Test valid password reset
# def test_valid_passwordreset_request(reset_data, user1):
#     auth_passwordreset_request('smithjohn177013@gmail.com')
#     server = setup_imap_server(DUMMY_EMAIL, DUMMY_PASSWORD)
#     reset_code = get_reset_code(server)
#     auth_passwordreset_reset(reset_code, "new_password")
#     # Login should not raise error, password changed
#     auth_login('smithjohn177013@gmail.com', 'new_password')

# Test log out of all sessions passwordreset_request
def test_logout_all_sessions_passwordreset_request(reset_data, user1):
    auth_passwordreset_request('smithjohn177013@gmail.com')
    server = setup_imap_server(DUMMY_EMAIL, DUMMY_PASSWORD)
    reset_code = get_reset_code(server)
    with pytest.raises(AccessError):
        channels_create(user1['token'], 'channel_name', True)

# Test invalid email no error
def test_invalid_email_no_error_passwordreset_request(reset_data):
    auth_passwordreset_request('johnsmith177013@gmail.com')

