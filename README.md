# gaze-detection
Detects what direction a person is looking at from their photo 

#####NOTES ON HOW TO START THE SERVER AND CALL THE IMAGE-CLASSIFICATION API


- run app.py to start the server
- http API endpoint for image classidier : <server-ip-address>:10000/classify-image
    - (no need to provide port number, if you are using a reverse proxy such as nginx)
- request type : POST
- in your POST request, include the image file to be classifed as 'face_img'.
- (if you are using python in front end, you can refer to the code in gaze_detection/api_caller.py to make a POST request)
