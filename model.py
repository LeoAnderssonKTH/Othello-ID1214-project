import torch
import torch.nn as nn
import torch.optim as optim
import os

class QNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, move, reward, next_state, done):
        
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        move = torch.tensor(move, dtype=torch.long)  
        reward = torch.tensor(reward, dtype=torch.float)
        
        # if state is in a [8, 8] format unsqueeze into [1, 8, 8] to allow flattening in next step
        if len(state.shape) == 2:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            move = torch.unsqueeze(move, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        
        # flatten state to feed the state and next_state to the model
        state = state.view(state.size(0), -1)
        next_state = next_state.view(next_state.size(0), -1)
        
        
        #print("Flattened State:", state)
        #print("Flattened State Shape:", state.shape)  
        
       
        pred = self.model(state) 
        
        
        target = pred.clone()

      
        for idx in range(len(done)):
            Q_new = reward[idx]  
            if not done[idx]: 
                Q_new += self.gamma * torch.max(self.model(next_state[idx]))  

            
            target[idx][move[idx]] = Q_new
        
        self.optimizer.zero_grad()  
        loss = self.criterion(target, pred)  
        #print(f"Training Loss: {loss.item()}")
        loss.backward() 

        self.optimizer.step() 
