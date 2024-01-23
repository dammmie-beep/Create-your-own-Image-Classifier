# -*- coding: utf-8 -*-
"""model_data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1seQa8PTtyYIzzzp5CxspT2_JeimTNjHA
"""

import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn, optim
from torch.autograd import Variable
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
from collections import OrderedDict
import json
from PIL import Image
import utils

def neural_network(the_model = 'vgg16', dropout=0.1, hidden_units=512, lr=0.0001,weight_decay=1e-3 ,device='cuda'):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if the_model == 'vgg16':
        model = models.vgg16(pretrained=True)
    elif the_model == 'alexnet':
        model = models.alexnet(pretrained=True)

    for para in model.parameters():
        para.requires_grad = False

    model.classifier = nn.Sequential(nn.Linear(model.classifier[0].in_features , hidden_units),
                                     nn.ReLU(),
                                     nn.Dropout(dropout),
                                     nn.Linear(hidden_units, 102),
                                     nn.LogSoftmax(dim=1))
    print(model)
    model = model.to(device)
    criterion = nn.NLLLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr)


    return model, criterion, optimizer


def save_checkpoint(model, optimizer, epochs, train_data, path='checkpoint.pth'):

    model.class_to_idx = train_data.class_to_idx

    checkpoint = {
        'input_size': model.input_size,
        'output_size': 102,
        'structure': "vgg16",
        'learning_rate': optimizer.param_groups[0]['lr'],
        'classifier': model.classifier,
        'epochs': epochs,
        'optimizer_state_dict': optimizer.state_dict(),
        'model_state_dict': model.state_dict(),
        'class_to_idx': model.class_to_idx
    }

    torch.save(checkpoint, path)


def loaded_model(path):
    checkpoint = torch.load('checkpoint.pth')
    structure = checkpoint['structure']
    model,_,_ = neural_network()
    model.class_to_idx = checkpoint['class_to_idx']
    model.load_state_dict(checkpoint['state_dict'])
    return model


def predict(image_path, model, topk=5, device = 'cuda'):

    image = process_image(image_path)

    image_tensor = torch.from_numpy(image).type(torch.FloatTensor)

    image_tensor = image_tensor.unsqueeze(0).to(device)

    model.to(device)
    model.eval()

    with torch.no_grad():
        output = model(image_tensor)
        ps = torch.exp(output)

    idx_to_class = {v: k for k, v in model.class_to_idx.items()}

    top_ps, top_idxs = ps.topk(topk, dim=1)
    top_classes = [idx_to_class[idx] for idx in top_idxs[0].cpu().numpy()]

    return top_ps[0].cpu().numpy().tolist(), top_classes



def process_image(image_path= "flowers/test/10/image_07090.jpg"):

    image = Image.open(image_path)

    if image.width > image.height:
        image.thumbnail((10000, 256))
    else:
        image.thumbnail((256, 10000))

    left_margin = (image.width - 224) / 2
    bottom_margin = (image.height - 224) / 2
    right_margin = left_margin + 224
    top_margin = bottom_margin + 224
    image = image.crop((left_margin, bottom_margin, right_margin, top_margin))

    np_image = np.array(image) / 255

    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    np_image = (np_image - mean) / std

    np_image = np_image.transpose((2, 0, 1))

    return np_image

"""Reference

https://github.com/vishalnarnaware/Create-your-own-Image-Classifier/blob/master/fmodel.py

"""
