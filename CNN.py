'''
    2. CNN schätzt für uns die heuristik, also wie wichtig ein block für unseren weg ist - könnte man mit manhatten vergleichen
'''

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class HeuristikNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1,16,3,padding=1)
        self.conv2 = nn.Conv2d(16,32,3,padding=1)
        self.fc1 = nn.Linear(32*20*20, 64)
        self.fc2 = nn.Linear(64,1)

        def forward(self, x):
            x = F.relu(self.conv1(x))
            x = F.relu(self.conv2(x))
            x = F.view(x.size(0), -1)
            x = F.relu(self.fc1(x))
            return self.fc2(x)


