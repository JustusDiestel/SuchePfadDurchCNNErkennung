from torch.utils.data import DataLoader

from CNN.CNN import MazeDataset, HeuristikNN
import torch.nn as nn
import torch.optim as optim
import torch


def trainMyCNN():
    dataset = MazeDataset("../Data/dataset.csv")
    loader = DataLoader(dataset, batch_size=16, shuffle=True)

    model = HeuristikNN()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(10):
        total_loss = 0
        for x, y in loader:
            optimizer.zero_grad()
            output = model(x)
            y = y.view_as(output)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1} | Loss: {total_loss:.4f}")

    torch.save(model.state_dict(), "../CreateMazesAndTrainCNN/cnn_heuristik.pth")



if __name__ == "__main__":
    trainMyCNN()