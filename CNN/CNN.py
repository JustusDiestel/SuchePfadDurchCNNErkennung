'''
    2. CNN schätzt für uns die heuristik, also wie wichtig ein block für unseren weg ist - könnte man mit manhatten vergleichen
'''

import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.utils.data import Dataset
import pandas as pd
import torch

class HeuristikNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1,16,3,padding=1)
        self.conv2 = nn.Conv2d(16,32,3,padding=1)
        self.conv3 = nn.Conv2d(32, 1, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = self.conv3(x)
        return x.mean(dim=[2,3]).squeeze(1)




class MazeDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        grid = np.load(row["maze"].replace(".png", ".npy"))
        grid = torch.tensor(grid).unsqueeze(0).float()  # [1,20,20]
        label = torch.tensor(row["path_length"], dtype=torch.float32)
        return grid, label

    def __len__(self):
        return len(self.data)