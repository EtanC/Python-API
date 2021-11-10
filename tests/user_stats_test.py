import pytest
from src.error import InputError, AccessError
from fake.other import clear
from fake.auth import auth_register
from fake.channels import channels_create
from fake.dm import dm_create
from fake.message import message_send, message_senddm
from fake.channel import channel_join, channel_addowner, channel_details
from fake.user import user_stats
from datetime import datetime, timezone
from json import dumps
import time

TIME_STEP = 1
MAX_TIME_DIFF = 2

class user_sim:
    '''
    The user_stats class is an over-simplified solution of user_stats.
    It can keep track of statistics such as when the number of channels joined,
    dms_joined or messages sent changes, as well as record these time stamps

    This class aids in checking the expected results from the user/stats/v1
    route
    '''
    def __init__(self):
        '''
        Initialises stats to their respective initial values, which are
        all currently 0. Also records the time_stamps of these stats
        '''
        curr_timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        self.channels_joined = [{
            'num_channels_joined' : 0,
            'time_stamp' : curr_timestamp,
        }]
        self.dms_joined = [{
            'num_dms_joined' : 0,
            'time_stamp' : curr_timestamp,
        }]
        self.messages_sent = [{
            'num_messages_sent' : 0,
            'time_stamp' : curr_timestamp,
        }]
    def joined_channel(self):
        '''
        Updates the number of channels joined, creating another entry
        with this new number and its time_stamp in self.channels_joined
        '''
        curr_timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        num_channels_joined = self.channels_joined[-1]['num_channels_joined']
        self.channels_joined.append({
            'num_channels_joined' : num_channels_joined + 1,
            'time_stamp' : curr_timestamp,
        })
    def joined_dm(self):
        '''
        Updates the number of dms joined, creating another entry
        with this new number and its time_stamp in self.dms_joined
        '''
        curr_timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        num_dms_joined = self.dms_joined[-1]['num_dms_joined']
        self.dms_joined.append({
            'num_dms_joined' : num_dms_joined + 1,
            'time_stamp' : curr_timestamp,
        })
    def sent_message(self):
        '''
        Updates the number of messages sent by user, creating another entry
        with this new number and its time_stamp in self.messages_sent
        '''
        curr_timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        num_messages_sent = self.messages_sent[-1]['num_messages_sent']
        self.messages_sent.append({
            'num_messages_sent' : num_messages_sent + 1,
            'time_stamp' : curr_timestamp,
        })
    def __str__(self):
        '''
        For use in debugging, returns all the data stored in user_stats as
        string in an easy to read format
        '''
        return dumps({'user_stats' : {
            'channels_joined' : self.channels_joined,
            'dms_joined' : self.dms_joined,
            'messages_sent' : self.messages_sent,
        }}, indent=4)

def compare_user_stats(user_stats_return, user_stats_expected):
    '''
    Compares an instance of a "user_stats" dictionary to a user_stats class
    '''
    assert len(user_stats_return['channels_joined']) == \
            len(user_stats_expected.channels_joined)
    compare = zip(user_stats_return['channels_joined'],
                  user_stats_expected.channels_joined)
    for entry, expected in compare:
        assert entry['num_channels_joined'] == expected['num_channels_joined']
        assert abs(entry['time_stamp'] - expected['time_stamp']) < MAX_TIME_DIFF
    assert len(user_stats_return['dms_joined']) == \
            len(user_stats_expected.dms_joined)
    compare = zip(user_stats_return['dms_joined'],
                  user_stats_expected.dms_joined)
    for entry, expected in compare:
        assert entry['num_dms_joined'] == expected['num_dms_joined']
        assert abs(entry['time_stamp'] - expected['time_stamp']) < MAX_TIME_DIFF
    assert len(user_stats_return['messages_sent']) == \
            len(user_stats_expected.messages_sent)
    compare = zip(user_stats_return['messages_sent'],
                  user_stats_expected.messages_sent)
    for entry, expected in compare:
        assert entry['num_messages_sent'] == expected['num_messages_sent']
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

def test_initial_stats_user_stats(user1):
    user_statistics = user_stats(user1['token'])
    user1_sim = user_sim()
    compare_user_stats(user_statistics, user1_sim)
    assert user_statistics['involvement_rate'] == 0

def test_valid_user_stats(user1):
    # Keep track of time stamps with simplified version of user/stats/v1
    user1_sim = user_sim()

    # Sleeping to test different, changing time stamps
    channel_id = channels_create(user1['token'], "Channel1", True)['channel_id']
    user1_sim.joined_channel()
    time.sleep(TIME_STEP)

    channels_create(user1['token'], "Channel1", True)
    user1_sim.joined_channel()
    time.sleep(TIME_STEP)

    dm_id = dm_create(user1['token'], [])['dm_id']
    user1_sim.joined_dm()
    time.sleep(TIME_STEP)

    dm_create(user1['token'], [])
    user1_sim.joined_dm()
    time.sleep(TIME_STEP)

    message_send(user1['token'], channel_id, "Hi")
    user1_sim.sent_message()
    time.sleep(TIME_STEP)
    # Send dm, record time stamp
    message_senddm(user1['token'], dm_id, "Hi")
    user1_sim.sent_message()

    user_statistics = user_stats(user1['token'])
    # Sorting lists by time_stamp as they are not guarranteed to be in order
    user_statistics['channels_joined'].sort(key=lambda x: x['time_stamp'])
    user_statistics['dms_joined'].sort(key=lambda x: x['time_stamp'])
    user_statistics['messages_sent'].sort(key=lambda x: x['time_stamp'])
    # Check if statistics are recorded correctly
    compare_user_stats(user_statistics, user1_sim)
    assert user_statistics['involvement_rate'] == 1

def test_two_users_user_stats(user1, user2):
    user1_sim = user_sim()
    user2_sim = user_sim()

    channel_id = channels_create(user1['token'], "Channel1", True)['channel_id']
    user1_sim.joined_channel()
    time.sleep(TIME_STEP)

    channel_join(user2['token'], channel_id)
    user2_sim.joined_channel()
    time.sleep(TIME_STEP)

    dm_id = dm_create(user1['token'], [user2['auth_user_id']])['dm_id']
    user1_sim.joined_dm()
    user2_sim.joined_dm()
    time.sleep(TIME_STEP)

    message_send(user1['token'], channel_id, "Hi")
    user1_sim.sent_message()
    time.sleep(TIME_STEP)

    message_senddm(user1['token'], dm_id, "Hi")
    user1_sim.sent_message()
    time.sleep(TIME_STEP)

    message_senddm(user2['token'], dm_id, "Hi")
    user2_sim.sent_message()

    user_statistics = user_stats(user1['token'])
    # Sorting lists by time_stamp as they are not guarranteed to be in order
    user_statistics['channels_joined'].sort(key=lambda x: x['time_stamp'])
    user_statistics['dms_joined'].sort(key=lambda x: x['time_stamp'])
    user_statistics['messages_sent'].sort(key=lambda x: x['time_stamp'])
    # Check if statistics are recorded correctly
    compare_user_stats(user_statistics, user1_sim)
    # Calculated involvement rate by hand
    assert user_statistics['involvement_rate'] == 0.8

    user_statistics = user_stats(user2['token'])
    # Sorting lists by time_stamp as they are not guarranteed to be in order
    user_statistics['channels_joined'].sort(key=lambda x: x['time_stamp'])
    user_statistics['dms_joined'].sort(key=lambda x: x['time_stamp'])
    user_statistics['messages_sent'].sort(key=lambda x: x['time_stamp'])
    # Check if statistics are recorded correctly
    compare_user_stats(user_statistics, user2_sim)

    assert user_statistics['involvement_rate'] == 0.6
