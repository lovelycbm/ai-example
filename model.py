import torch.nn as nn
import torch
from torch.utils.data import Dataset, DataLoader
import os
import glob
import json
from PIL import Image


# 모델 정의
class CropYieldModel(nn.Module):
    def __init__(self):
        super(CropYieldModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 28 * 28 + 5, 128)
        self.fc2 = nn.Linear(128, 1)
        self.relu = nn.ReLU()

    def forward(self, img, features):
        x = self.pool(self.relu(self.conv1(img)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = x.view(-1, 64 * 28 * 28)
        x = torch.cat((x, features), dim=1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    

# 데이터셋 정의
class CropDataset(Dataset):
    def __init__(self, json_dir, img_dir, transform=None):        
        print(f"{json_dir} 와 {img_dir} 로부터 데이터셋을 생성합니다.")
        self.json_dir = json_dir
        self.img_dir = img_dir
        self.transform = transform
        self.json_files = glob.glob(os.path.join(json_dir, "*.json"))
        self.data = []
        print(f"Found {len(self.json_files)} json files")
        for json_file in self.json_files:
            with open(json_file, 'r', encoding='utf-8-sig') as f:
                item = json.load(f)
                img_id = item['ID']
                img_path = os.path.join(self.img_dir, f"{img_id}.jpg")
                if os.path.exists(img_path):
                    self.data.append(item)
                else:
                    print(f"{json_file} 과 {img_path} 는 서로 매칭되지 않습니다. 이미지 파일이 없습니다.")        
        print(f"총 {len(self.data)}개의 샘플을 로드했습니다.")
        

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        img_id = item['ID']
        
        img_path = os.path.join(self.img_dir, f"{img_id}.jpg")
        
        
        if not os.path.exists(img_path):            
            raise FileNotFoundError(f"{img_id} 파일이 없습니다.")
        
        
        image = Image.open(img_path).convert('RGB')
        
        if self.transform:
            image = self.transform(image)

        features = torch.tensor([
            item['GSD'],
            item['LONG'],
            item['LAT'],
            item['GROWTH_1'],
            item['GROWTH_2']
        ], dtype=torch.float32)

        yield_ = torch.tensor(item['YIELD'], dtype=torch.float32)

        return image, features, yield_
