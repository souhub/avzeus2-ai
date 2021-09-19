'''
Copyright (c) 2019 Timothy Esler
Released under the MIT license
https://github.com/timesler/facenet-pytorch/blob/master/LICENSE.md
'''

from io import BytesIO
import base64

import numpy as np
from PIL import Image
import torch
from facenet_pytorch import MTCNN

from .my_resenet import MyInceptionResnetV1

INPUTS_PATH='/opt/ml/inputs/'

def recommend_from_img_path(img_body,write_path: str) -> list:

    with torch.no_grad():

        mtcnn = MTCNN(image_size = 160, margin = 10).eval()
        # img = Image.open(read_path)
        img = Image.open(BytesIO(base64.b64decode(img_body)))
        img = mtcnn(img, write_path)
        del mtcnn

        if str(img) == 'None':

            return False, []

        else:

            #resnet = InceptionResnetV1(pretrained = 'vggface2').eval()
            resnet = MyInceptionResnetV1(pretrained = 'vggface2').eval()
            # resnet.load_state_dict(torch.load('inputs/resnet'))
            resnet.load_state_dict(torch.load(INPUTS_PATH+'resnet'))
            img_vec = np.array(resnet(img.unsqueeze(0)).flatten())
            del resnet
            ids = np.load(INPUTS_PATH+'id.npy')
            vecs = np.load(INPUTS_PATH+'actress_vecs.npy', allow_pickle = True)
            rec_actress_id = []

            for index in np.argsort(np.square(vecs - img_vec).sum(axis = 1))[:10]:

                rec_actress_id.append(str(ids[index]))

            return True, rec_actress_id

