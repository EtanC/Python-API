channels_create_v1 assumptions: 
* channel name can contain any char as long as it is within character range 

user/profile/setname/v1: 
* don't need to raise errors if first and last name are changed to be the same as the old one 

user/profile/setemail/v1: 
* don't need to raise errors if email is changed to be the same as before 

user/profile/sethandle/v1: 
* don't need to raise errors if handle is changed to be the same as before 