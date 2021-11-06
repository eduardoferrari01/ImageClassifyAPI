from torch.autograd import Variable
from torchvision import transforms, models
import torch
import torch.nn as nn
from pathlib import Path

error = {"label": "unknown"}


def get_transforms():
    return transforms.Compose([transforms.RandomResizedCrop(224),
                               transforms.RandomHorizontalFlip(),
                               transforms.ToTensor(),
                               transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])


def get_classes():
    return [{
        "description": "Bothrops Alternatus",
        "label": "bothrops-alternatus"},
        {
            "description": "Crotalus Durissus",
            "label": "crotalus-durissus"
        },
        {
            "description": "Lachesis muta",
            "label": "lachesis-muta"
        }]


class CnnModel:

    def __init__(self):
        self.test_transforms = get_transforms()
        self.classes = get_classes()
        self.device = torch.device('cpu')
        self.cnn_model = self.load()
        self.error = {"label": "unknown"}

    def load(self):
        mod_path = Path(__file__).parent
        path_model = (mod_path / 'model/snake').resolve()

        model_ft = models.resnet18(pretrained=True)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs, len(self.classes))
        model_ft.load_state_dict(torch.load(path_model, map_location=self.device))
        model_ft.eval()
        return model_ft

    def classify(self, image):
        image_tensor = self.test_transforms(image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        input_img = Variable(image_tensor)
        input_img = input_img.to(self.device)
        output = self.cnn_model(input_img)
        max_v, idx_max = torch.max(output, 1)

        print('Valor maximo: {}'.format(max_v.item()))
        print('Id: {}'.format(idx_max.item()))

        if max_v > 3.0:
            animal = self.classes[idx_max]
            print('Animal: {}'.format(animal))
            return animal

        print('Animal unknown')
        return error

    def get_classes(self):
        return self.classes
