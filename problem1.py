import torch
import matplotlib.pyplot as plt
import numpy as np
import torch.nn as nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.optim as optim

class regression(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Sequential(
            nn.Linear(1, 5),
            nn.ReLU(),
            nn.Linear(5, 10),
            nn.ReLU(),
            nn.Linear(10, 5),
            nn.ReLU(),
            nn.Linear(5, 1)
        )
        self.reset_parameters()

    def forward(self,x):
        x = self.linear(x)
        return x
    def reset_parameters(self):
        for layer in self.linear:
            if isinstance(layer, nn.Linear):
                nn.init.xavier_normal_(layer.weight)
                nn.init.zeros_(layer.bias)

class dataset(Dataset):
    def __init__(self, data : list):
        self.data = data
    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        x = torch.tensor(data[idx][0],dtype=torch.float32).reshape(-1,1)
        y = torch.tensor(data[idx][1],dtype=torch.float32).reshape(-1,1)
        return x, y

def normalize(data: np.array):
    return (data - data.mean()) / data.std()

def plot(data,model):
    # plot the mormalized data
    plt.scatter(data[:,0], data[:,1],c='r')
    # plot the predicted data
    # get the max input and min input
    max_input = data.max()
    min_input = data.min()
    # get the predicted data
    x = torch.linspace(min_input, max_input, 100).reshape(-1,1)
    y = model(x)
    # plot the predicted data
    plt.plot(x.detach().numpy(), y.detach().numpy())
    plt.savefig('plot.png')



if __name__ == '__main__':
    data = [[1, 2], [3, 4], [5, 3], [7, 4], [9, 6]]
    data = np.array(data)
    data = normalize(data)
    
    dataset = dataset(data)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)
    model = regression()
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=1e-3)
    for epoch in range(10000):
        for x,y in dataloader:
            optimizer.zero_grad()
            output = model(x)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()
            print(loss.item())

    plot(data,model)
