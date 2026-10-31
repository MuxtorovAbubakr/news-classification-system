import torch.nn as nn
import torch

class NewsClassifier(nn.Module):
    def __init__(
            self,
            input_size: int = 100_000,
            hidden_size: int = 128,
            num_classes: int = 4
    ):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_classes)
        )

    def forward(self, x):
        return self.network(x)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


model = NewsClassifier(
    input_size=100_000,
    hidden_size=128,
    num_classes=4
)

model.load_state_dict(
    torch.load(
        "models/fnn_weights.pth",
        map_location=device,
        weights_only=True
    )
)

model.to(device)
model.eval()