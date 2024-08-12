# links and stuffs

## picocss

https://www.youtube.com/watch?v=-n84EMKIXQM

https://picocss.com/docs

## sveltekit

https://kit.svelte.dev/docs/integrations

## storing images

https://understandingdata.com/posts/how-to-easily-resize-compress-your-images-in-python/

```python
res = requests.get(url)
    if res == 200 and 'jpeg' in res.headers['content-type']:
        img_arr = np.array(Image.open(BytesIO(res.content)))
        return img_arr
image_file = StringIO(open("test.jpg",'rb').read())

Binary_image_file = Binary(image_file) #pymongo libary #and then send it to Binary(image_file) type in pymongo
```

Then do a normal insert in mongo.

To read. do a normal find(). Then load the value from key and convert the data stored to image as:

```python
image_data = StringIO.StringIO(Stringio_image_file)
image = Image.open(image_data)

## typescript goods

https://payton.codes/2022/01/08/common-typescript-errors-and-how-to-fix-them/

https://www.linkedin.com/pulse/working-typescript-express-tim-kent/

## other apis

https://github.com/miramo/senscritique-api/blob/master/src/settings.ts

https://developer.themoviedb.org/docs/getting-started

## deployment

https://medium.com/@malekrizwan08/how-to-deploy-expressjs-mongodb-application-for-free-ce032b29a0e1

https://www.youtube.com/watch?v=i1wAQCg2iWU


