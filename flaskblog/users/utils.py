import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import  mail




def save_picture(form_picture):
    random_hex=secrets.token_hex(8) # This line generates a random hexadecimal string using the secrets module. The token_hex function takes an integer argument that specifies the number of bytes to generate, and it returns a string that is twice as long (since each byte is represented by two hexadecimal characters). In this case, it generates a random string of 16 characters (8 bytes * 2).
    _, f_ext=os.path.splitext(form_picture.filename) # This line splits the filename of the uploaded picture into two parts: the base filename (f_name) and the file extension (f_ext). The os.path.splitext function takes a filename as input and returns a tuple containing the base filename and the file extension. For example, if the uploaded file is named "profile.jpg", f_name would be "profile" and f_ext would be ".jpg".
    picture_fn=random_hex + f_ext # This line creates a new filename for the uploaded picture
    picture_path=os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) # This line constructs the full file path where the uploaded picture will be saved on the server. It uses the os.path.join function to concatenate the root path of the application (app.root_path), the directory for profile pictures ('static/profile_pics'), and the new filename (picture_fn). This ensures that the uploaded picture is saved in the correct location within the application's static files.
    form_picture.save(picture_path) # This line saves the uploaded picture file to the specified location on the server. The save method of the form_picture object takes the file path as an argument and saves the file to that location.
    
    output_size=(125,125) # This line defines a tuple called output_size that specifies the desired dimensions (width and height) for the profile picture. In this case, it sets the output size to 125 pixels by 125 pixels.
    i=Image.open(form_picture) # This line opens the uploaded picture file using the PIL (Pillow) library. The Image.open function takes the uploaded file as an argument and returns an Image object that represents the opened image file.
    i.thumbnail(output_size) # This line resizes the opened image to fit within the specified output size while maintaining the aspect ratio. The thumbnail method of the Image object takes the output_size tuple as an argument and resizes the image accordingly. This ensures that the profile picture is not too large and fits within the desired dimensions.
    i.save(picture_path) # This line saves the resized image back to the specified file path on the server. The save method of the Image object takes the file path as an argument and saves the image to that location, overwriting the original uploaded file with the resized version. 
    
    return picture_fn


def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request ',sender=current_app.config['MAIL_USERNAME'],recipients=[user.email])
    msg.body=f''' To Reset your password , vistes the following linke:
{url_for('users.reset_token', token=token,_external=True)}
    
IF you did not make this rquest then simply ignore this email and no change will be made.
'''
    mail.send(msg)   