import numpy as np
from keras.preprocessing import image
from keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity

model = ResNet50(weights='imagenet', include_top=False)

def prep_image(path):
    img = image.load_img(path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

def compare(target, others):
    # load and preocess the target image
    target_image = prep_image(f"./scraped/{target}.png")
    # get the embedding of the target image
    target_embedding = model.predict(target_image)
    # get the embeddings of the other images
    images = [{"img":prep_image(f'./scraped/{x}.png'), "name": f'./scraped/{x}.png'} for x in others]
    embeddings = []
    for img in images:
        img["embedding"] = model.predict(img["img"])
        img["distance"] = cosine_similarity(img["embedding"].reshape(1, -1), target_embedding.reshape(1, -1))[0][0]
        embeddings.append(img)
    # compare embeddings
    for x in embeddings:
        print(x["distance"], x["name"])
    return embeddings