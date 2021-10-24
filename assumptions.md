channels_create_v1 assumptions: 
* channel name can contain any char as long as it is within character range 

user/profile/setname/v1: 
* don't need to raise errors if first and last name are changed to be the same as the old one 

user/profile/setemail/v1: 
* changing your email to the one you already had before will raise InputError 'email already in use' 

user/profile/sethandle/v1: 
* don't need to raise errors if handle is changed to be the same as before 

auth/login/v1:
* route can only be sent strings

Regarding all GET requests:
* the same key is not used twice in the same url to pass data. If it is, only 
  the first one will be accepted.