import pytest
from src.error import InputError, AccessError
from fake.other import clear
from fake.auth import auth_register
from fake.channels import channels_create
from fake.dm import dm_create
from fake.message import message_send, message_senddm
from fake.users import users_stats
from datetime import datetime, timezone
from json import dumps
import time

TIME_STEP = 1
MAX_TIME_DIFF = 2

def current_timestamp():
    return datetime.now().replace(tzinfo=timezone.utc).timestamp()

class workspace_stats:
    def __init__(self):
        '''
        Initialises stats to their respective initial values, which are
        all currently 0. Also records the time_stamps of these stats
        '''
        curr_timestamp = current_timestamp()
        self.channels_exist = [{
            'num_channels_exist' : 0,
            'time_stamp' : curr_timestamp,
        }]
        self.dms_exist = [{
            'num_dms_exist' : 0,
            'time_stamp' : curr_timestamp,
        }]
        self.messages_exist = [{
            'num_messages_exist' : 0,
            'time_stamp' : curr_timestamp,
        }]
    def add_channel(self):
        total_channels = self.channels_exist[-1]['num_channels_exist']
        self.channels_exist.append({
            'num_channels_exist' : total_channels + 1,
            'time_stamp' : current_timestamp(),
        })
    def add_dm(self):
        total_dms = self.dms_exist[-1]['num_dms_exist']
        self.dms_exist.append({
            'num_dms_exist' : total_dms + 1,
            'time_stamp' : current_timestamp(),
        })
    def add_message(self):
        total_messages = self.messages_exist[-1]['num_messages_exist']
        self.messages_exist.append({
            'num_messages_exist' : total_messages + 1,
            'time_stamp' : current_timestamp(),
        })
    def __str__(self):
        '''
        For use in debugging, returns all the data stored in workspace_stats as
        string in an easy to read format
        '''
        return dumps({'workspace_stats' : {
            'channels_exist' : self.channels_exist,
            'dms_exist' : self.dms_exist,
            'messages_exist' : self.messages_exist,
        }}, indent=4)
    # def remove_dm(self):
    # def remove_message(self):

def compare_users_stats(users_stats_return, users_stats_expected):
    '''
    Compares an instance of a "users_stats" dictionary to a workspace_stats class
    '''
    assert len(users_stats_return['channels_exist']) == \
            len(users_stats_expected.channels_exist)
    compare = zip(users_stats_return['channels_exist'],
                  users_stats_expected.channels_exist)
    for entry, expected in compare:
        assert entry['num_channels_exist'] == expected['num_channels_exist']
        assert abs(entry['time_stamp'] - expected['time_stamp']) < MAX_TIME_DIFF
    assert len(users_stats_return['dms_exist']) == \
            len(users_stats_expected.dms_exist)
    compare = zip(users_stats_return['dms_exist'],
                  users_stats_expected.dms_exist)
    for entry, expected in compare:
        assert entry['num_dms_exist'] == expected['num_dms_exist']
        assert abs(entry['time_stamp'] - expected['time_stamp']) < MAX_TIME_DIFF
    assert len(users_stats_return['messages_exist']) == \
            len(users_stats_expected.messages_exist)
    compare = zip(users_stats_return['messages_exist'],
                  users_stats_expected.messages_exist)
    for entry, expected in compare:
        assert entry['num_messages_exist'] == expected['num_messages_exist']
        assert abs(entry['time_stamp'] - expected['time_stamp']) < MAX_TIME_DIFF

@pytest.fixture(autouse=True)
def reset_data():
    clear()

@pytest.fixture
def user1():
    return auth_register(
        "realemail_812@outlook.edu.au", "Password1", "John", "Smith"
    )

@pytest.fixture
def user2():
    return auth_register(
        "realemail_127@outlook.edu.au", "Password1", "Smith", "John"
    )

@pytest.fixture
def user3():
    return auth_register(
        "realemail_312@outlook.edu.au", "Password1", "John2", "Smith"
    )

def test_initial_users_stats(user1):
    workspace_sim = workspace_stats()
    workspace_statistics = users_stats(user1['token'])
    compare_users_stats(workspace_statistics, workspace_sim)


def test_valid_users_stats(user1, user2):
    workspace_sim = workspace_stats()

    channel_id = channels_create(user1['token'], "Channel1", True)['channel_id']
    workspace_sim.add_channel()
    time.sleep(TIME_STEP)

    dm_create(user1['token'], [user2['auth_user_id']])
    workspace_sim.add_dm()
    time.sleep(TIME_STEP)

    message_send(user1['token'], channel_id, "hi")
    workspace_sim.add_message()

    workspace_statistics = users_stats(user1['token'])
    compare_users_stats(workspace_statistics, workspace_sim)
    assert workspace_statistics['utilization_rate'] == 1

def test_multiple_users_users_stats(user1, user2, user3):
    workspace_sim = workspace_stats()

    channel_id = channels_create(user1['token'], "Channel1", True)['channel_id']
    workspace_sim.add_channel()
    time.sleep(TIME_STEP)

    dm_id = dm_create(user1['token'], [user2['auth_user_id']])['dm_id']
    workspace_sim.add_dm()
    time.sleep(TIME_STEP)

    message_send(user1['token'], channel_id, "hi")
    workspace_sim.add_message()
    time.sleep(TIME_STEP)

    channels_create(user2['token'], "Channel1", True)
    workspace_sim.add_channel()
    time.sleep(TIME_STEP)

    message_senddm(user2['token'], dm_id, "hi")
    workspace_sim.add_message()
    time.sleep(TIME_STEP)

    workspace_statistics = users_stats(user2['token'])
    compare_users_stats(workspace_statistics, workspace_sim)
    assert workspace_statistics['utilization_rate'] == 2/3

def test_invalid_token_users_stats():
    with pytest.raises(AccessError):
        users_stats("invalid_token")