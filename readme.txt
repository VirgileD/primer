https://www.youtube.com/watch?v=-n84EMKIXQM

https://picocss.com/docs

https://kit.svelte.dev/docs/integrations


https://understandingdata.com/posts/how-to-easily-resize-compress-your-images-in-python/

res = requests.get(url)
    if res == 200 and 'jpeg' in res.headers['content-type']:
        img_arr = np.array(Image.open(BytesIO(res.content)))
        return img_arr

image_file = StringIO(open("test.jpg",'rb').read())

and then send it to Binary(image_file) type in pymongo

Binary_image_file = Binary(image_file) #pymongo libary

Then do a normal insert in mongo.

To read. do a normal find(). Then load the value from key and convert the data stored to image as:

image_data = StringIO.StringIO(Stringio_image_file)
image = Image.open(image_data)


https://payton.codes/2022/01/08/common-typescript-errors-and-how-to-fix-them/