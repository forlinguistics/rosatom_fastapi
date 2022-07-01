# rosatom_fastapi
to POST I used multipart/form-data requests with key 'images' like
```
curl --location --request POST 'http://127.0.0.1:8000/frames/' \
--form 'images=@"/image1.jpg"' \
--form 'images=@"image2.jpg"'
```

