# rosatom_fastapi
to POST I used multipart/form-data requests like
multipart/form-data
```
curl --location --request POST 'http://127.0.0.1:8000/frames/' \
--form 'images=@"/C:/Users/Michael/Pictures/ml presentation/iris2.jpg"' \
--form 'images=@"/C:/Users/Michael/Pictures/ml presentation/iris3.jpg"'
```

