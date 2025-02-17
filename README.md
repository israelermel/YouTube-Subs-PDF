# YouTube Subtitles to PDF

To run the Docker image, use the following command:

```sh
docker run -p 5000:5000 israelermel/youtube-subs-pdf
```
The application will be accessible at `http://localhost:5000`.

### Running with Docker Compose

If you prefer, you can use Docker Compose to run the project. The `docker-compose.yml` file is available in the repository. To start the project with Docker Compose, execute:

```sh
docker-compose up
```
This will build and start the application, making it accessible at `http://localhost:5000`.

## How to Obtain the IDs

### Video ID

The `video_id`  is the value that comes after `v=` in the video URL. For example:
```
https://www.youtube.com/watch?v=<nmas_zbcMeU>
```
In this case, the `video_id` is `nmas_zbcMeU`.

### Playlist ID

The `playlist_id` is the value that comes after `list=` in the playlist URL. For example:
```
https://www.youtube.com/watch?list=<PLBSIqODyO5BE_8nhD3MyOrX4D40jRwVIp>
```
In this case, `the playlist_id` is `PLBSIqODyO5BE_8nhD3MyOrX4D40jRwVIp`.

## Environment Variables

The project uses environment variables for configuration. You can set these variables in a `.env` file. An example `.env` file is provided below:
```
ENVIRONMENT=DEBUG
```

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request.

---

This project was developed to facilitate the extraction of YouTube video subtitles and their conversion to PDF, helping developers work with multimedia content more efficiently.