# ibe_lbme_img_proc_back
This repository defines and to publish the backend components. It has a development branch using the secrets of the development Github environment to authenticate against the Container repository and publishes the Docker images that contain the source files and serve the applications with hypercorn server. There are two folders within this:
image_api: An API written with FAST API, This component creates the images and retrieves the images information

* `GET    /images` : retrieve the public images
* `GET    /images/user/{user_id}` : retrieve the images filtered by user id
* `POST /images` : upload a new image
* `POST /images/{image_id}/publish` : add an image to public bucket
