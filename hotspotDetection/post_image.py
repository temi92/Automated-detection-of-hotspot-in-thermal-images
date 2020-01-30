import requests
addr = 'http://localhost:5000'
URL = addr + '/predict_image'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}


def post_image(img_file):
    """ post image and return the response """
    files = {"image":open(img_file, 'rb')}
    r = requests.post(URL,files=files)
    return r

response = post_image("image.jpg")
print (response.status_code)
