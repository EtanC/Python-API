from src import config
import requests
from PIL import Image
import pytest

@pytest.fixture
def reset(): 
    requests.delete(f"{config.url}clear/v1")

    data_register = { 
        'email': "realemail_812@outlook.edu.au",
        'password': "Password1",
        'name_first': "John",
        'name_last': "Smith",
    }

    response_register = requests.post(f"{config.url}auth/register/v2", json=data_register)

    return response_register.json()

'''
TEST FOR: 
* invalid token
* img_url returns HTTP status other than 200 
* x and y start / end not within image boundaries
* end < start
* image not a jpg 
* valid 
'''

def test_invalid_token(reset): 
    data_photo = {
        'token': 'invalid token',
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg',
        'x_start': 0, 
        'y_start': 0, 
        'x_end': 159, 
        'y_end': 200,
    }
    
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.status_code == 403 

def test_invalid_url(reset):
    data_photo = {
        'token': reset['token'], 
        'img_url': f"{config.url}", 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': 0, 
        'y_end': 0
    }
    
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.status_code == 400

def test_invalid_crop_dimensions(reset): 
    # image height = 200px, width = 159px
    data_photo = {
        'token': reset['token'], 
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg', 
        'x_start': -1, 
        'y_start': 0, 
        'x_end': 159, 
        'y_end': 200
    }
    
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.status_code == 400
    
    data_photo['x_start'] += 1 
    data_photo['y_start'] -= 1
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.status_code == 400
    
    data_photo['y_start'] += 1 
    data_photo['x_end'] += 1
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.status_code == 400
    
    data_photo['x_end'] -= 1 
    data_photo['y_end'] += 1 
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.status_code == 400
    
def test_invalid_start_end(reset): 
    data_photo = {
        'token': reset['token'], 
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg', 
        'x_start': 1, 
        'y_start': 1, 
        'x_end': 0, 
        'y_end': 0
    }
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.status_code == 400

def test_non_jpg(reset): 
    data_photo = {
        'token': reset['token'], 
        'img_url': 'http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png', 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': 159, 
        'y_end': 200
    }
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.status_code == 400

def test_valid_crop_nothing(reset): 
    # download image and get its dimensions
    # crop set exactly to image dimensions, so shouldn't crop anything
    img_url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    start_image = Image.open(requests.get(img_url, stream=True).raw)
    start_width, start_height = start_image.size
    
    data_photo = {
        'token': reset['token'], 
        'img_url': img_url, 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': start_width, 
        'y_end': start_height
    }
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.json() == {} 
    
    response_photo = requests.get(f"{config.url}user/profile/photo/{reset['auth_user_id']}.jpg", stream=True)
    
    assert response_photo.status_code == 200 

    # download image and check dimensions 
    image = Image.open(response_photo.raw)
    width, height = image.size
    assert width == start_width
    assert height == start_height 
    
def test_valid_crop(reset): 
    # crop the photo
    img_url = "http://cgi.cse.unsw.edu.au/~morri/morriphoto.jpg"
    
    data_photo = {
        'token': reset['token'], 
        'img_url': img_url, 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': 1800, 
        'y_end': 1500
    }
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.json() == {} 
    
    response_photo = requests.get(f"{config.url}user/profile/photo/{reset['auth_user_id']}.jpg", stream=True)
    
    assert response_photo.status_code == 200
    
    # download image and check dimensions 
    image = Image.open(response_photo.raw)
    width, height = image.size
    assert width == 1800
    assert height == 1500 
    

def test_valid_twice(reset): 
    # assuming that calling it the second time will overwrite teh first photo
    img_url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    start_image = Image.open(requests.get(img_url, stream=True).raw)
    start_width, start_height = start_image.size
    data_photo = {
        'token': reset['token'], 
        'img_url': img_url, 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': start_width, 
        'y_end': start_height
    }
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.json() == {} 
    
    response_photo = requests.get(f"{config.url}user/profile/photo/{reset['auth_user_id']}.jpg", stream=True)
    
    # check if you can get image through json 
    assert response_photo.status_code == 200 
    
    image = Image.open(response_photo.raw)
    width, height = image.size
    assert width == start_width
    assert height == start_height 
    
    # upload second photo, not croppign anything
    img_url2 = "http://cgi.cse.unsw.edu.au/~morri/morriphoto.jpg"
    start_image2 = Image.open(requests.get(img_url2, stream=True).raw)
    start_width2, start_height2 = start_image2.size
    
    data_photo = {
        'token': reset['token'], 
        'img_url': img_url2, 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': start_width2, 
        'y_end': start_height2
    }
    response_photo2 = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo2.json() == {} 
    
    response_photo2 = requests.get(f"{config.url}user/profile/photo/{reset['auth_user_id']}.jpg", stream=True)
    
    # check if you can get image through json 
    assert response_photo.status_code == 200
    image2 = Image.open(response_photo2.raw)
    width2, height2 = image2.size
    assert width2 == start_width2
    assert height2 == start_height2 

def test_valid_two_people(reset):
    # test two differnet people calling uploadphoto
    img_url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    start_image = Image.open(requests.get(img_url, stream=True).raw)
    start_width, start_height = start_image.size
    data_photo = {
        'token': reset['token'], 
        'img_url': img_url, 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': start_width, 
        'y_end': start_height
    }
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.json() == {} 
    
    response_photo = requests.get(f"{config.url}user/profile/photo/{reset['auth_user_id']}.jpg", stream=True)
    
    # check if you can get image through json 
    assert response_photo.status_code == 200 
    
    image = Image.open(response_photo.raw)
    width, height = image.size
    assert width == start_width
    assert height == start_height 
    
    data_register = { 
        'email': "realemail_813@outlook.edu.au",
        'password': "Password2",
        'name_first': "Jack",
        'name_last': "Smith",
    }

    response_register = requests.post(f"{config.url}auth/register/v2", json=data_register)

    img_url = "http://cgi.cse.unsw.edu.au/~morri/morriphoto.jpg"
    start_image = Image.open(requests.get(img_url, stream=True).raw)
    start_width, start_height = start_image.size
    data_photo = {
        'token': response_register.json()['token'], 
        'img_url': img_url, 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': start_width, 
        'y_end': start_height
    }
    response_photo = requests.post(f"{config.url}user/profile/uploadphoto/v1", json=data_photo)
    assert response_photo.json() == {} 
    
    response_photo = requests.get(f"{config.url}user/profile/photo/{response_register.json()['auth_user_id']}.jpg", stream=True)
    
    # check if you can get image through json 
    assert response_photo.status_code == 200 
    
    image = Image.open(response_photo.raw)
    width, height = image.size
    assert width == start_width
    assert height == start_height 
    
    