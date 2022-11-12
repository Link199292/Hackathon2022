## Streaming video data analyzer for customer behavior analytics.


The main goal is to extract customers metadata from cameras. 

In our scenario there are different cameras around the shop, one of which is in the entrance.

Cameras are connected to an encrypted WiFi. Our system collects, in streaming, all the images coming from the cameras, then it extracts the faces, and analyze them in order to obtain the metadata. 

The extracted data is saved in a MongoDB collection ("customers" in our case). Each rows contains data about a single face. In particular, it consists on a timestamp (when the frame was taken), gender, age, and emotion of the face.

When necessary, data can be easily extracted from the DB, and then analyzed.

##
#### Structure

    main.py: connects to camera through provided url of WiFi camera, save the frame, and call get_first_faces

    get_faces.py: 
        * detects and extracts faces, align them in order to enhance the performances. 
        * compare_face is called, which keeps comparing each new detect faces with the already stored ones. 
          If it is new, it saves it a temporary folder.

    data_extraction.py: 
        * extracts metadata from images in temporary file (time, age, gender, emotion)
        * save metadata into a MongoDB collection ("customers")

    NB: main.py and data_extraction.py run in parallel



