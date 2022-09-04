import torch
from torch.autograd import Variable
from torchvision import transforms, models
import torch.nn as nn
from pathlib import Path
from api.core.cnn.labels import Labels

error = {"label": "unknown"}

labels = Labels()


def get_transforms():
    return transforms.Compose([transforms.Resize(256),
                               transforms.CenterCrop(224),
                               transforms.ToTensor(),
                               transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])


class CnnModel:

    def __init__(self):
        self.test_transforms = get_transforms()
        self.classes = labels.get()
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
        image.thumbnail((250, 250))
        image_tensor = self.test_transforms(image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        input_img = Variable(image_tensor)
        input_img = input_img.to(self.device)
        output = self.cnn_model(input_img)
        max_v, idx_max = torch.max(output, 1)

        print('Valor maximo: {}'.format(max_v.item()))
        print('Id: {}'.format(idx_max))
        print(output)
        if max_v > 2.5:
            animal = self.classes[idx_max]
            print('Animal: {}'.format(animal))
            return {"label": animal}

        print('Animal unknown')
        return error

    def get_class_names(self):
        return self.classes
