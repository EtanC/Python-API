import pytest
from fake.standup import standup_start, standup_send, standup_active
from fake.auth import auth_register
from fake.channels import channels_create
from fake.other import clear
from src.error import InputError, AccessError
import time


