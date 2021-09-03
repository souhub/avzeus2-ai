import numpy as np
import pandas as pd
from PIL import Image
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN

def recommend_from_img_path(img_path: str) -> list:
    
    with torch.no_grad():
        
        mtcnn = MTCNN(image_size = 160, margin = 10).eval()
        img = Image.open(img_path)
        img = mtcnn(img, img_path)
        del mtcnn
    
        if str(img) == 'None':
        
            return [False, []]
    
        else:
            
            resnet = InceptionResnetV1(pretrained = 'vggface2').eval()
            img_vec = np.array(resnet(img.unsqueeze(0)).flatten())
            del resnet
            ids = pd.read_csv('input/actress_data.csv')['id'].tolist()
            vecs = np.load('input/actress_vecs.npy', allow_pickle = True)
            rec_actress_id = []
            
            for index in np.argsort(np.square(vecs - img_vec).sum(axis = 1))[:10]:
                
                rec_actress_id.append(str(ids[index]))
                
            return [True, rec_actress_id]
