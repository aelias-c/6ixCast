#%%
from datetime import datetime, timezone
import torch
from torch.utils.tensorboard import SummaryWriter
from torchvision import datasets
from torchvision.transforms import v2
sys.path.insert(0, '/Users/lfl/google_drive/phd/journal_club/')
from sixcast.training.train_test_mod import train, test
from sixcast.vae.vae import VAE

#%%
learning_rate = 1e-3
weight_decay = 1e-2
num_epochs = 20
latent_dim = 2
hidden_dim = 512


batch_size = 128
transform = v2.Compose([
    v2.ToImage(),
    v2.ToDtype(torch.float32, scale=True),
    v2.Lambda(lambda x: x.view(-1) - 0.5),
])

# Download and load the training data
train_data = datasets.MNIST(
    '~/.pytorch/MNIST_data/',
    download=True,
    train=True,
    transform=transform,
)
# Download and load the test data
test_data = datasets.MNIST(
    '~/.pytorch/MNIST_data/',
    download=True,
    train=False,
    transform=transform,
)

# Create data loaders
train_loader = torch.utils.data.DataLoader(
    train_data,
    batch_size=batch_size,
    shuffle=True,
)
test_loader = torch.utils.data.DataLoader(
    test_data,
    batch_size=batch_size,
    shuffle=False,
)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = (
    VAE(input_dim=784, hidden_dim=hidden_dim, latent_dim=latent_dim).to(device)
    )
optimizer = torch.optim.AdamW(
    model.parameters(), lr=learning_rate, weight_decay=weight_decay)
writer = SummaryWriter(
    'runs/mnist/VAE_{datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")}')

prev_updates = 0
for epoch in range(num_epochs):
    print(f'Epoch {epoch+1}/{num_epochs}')
    prev_updates = train(
        model, batch_size, train_loader, optimizer, prev_updates,
        device=device, writer=writer)
    test(
        model, test_loader, prev_updates, latent_dim, device=device,
        writer=writer)
