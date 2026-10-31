import joblib
import torch

from pathlib import Path

from src.models import NewsClassifier
from src.preprocessing import preprocess_text

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Model artifact paths
VECTORIZER_PATH = PROJECT_ROOT / "models" / "tfidf_vectorizer.joblib"
MODEL_PATH = PROJECT_ROOT / "models" / "fnn_weights.pth"

# Automatically select GPU if available, otherwise CPU
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CLASS_NAMES = ["World", "Sports", "Business", "Sci/Tech"]


# Load TF-IDF vectorizer
vectorizer = joblib.load(VECTORIZER_PATH)

# Recreate the FNN architecture
model = NewsClassifier(
    input_size=100_000,
    hidden_size=128,
    num_classes=4
)

# Load trained weights
state_dict = torch.load(
    MODEL_PATH,
    map_location=DEVICE,
    weights_only=True
)

model.load_state_dict(state_dict)

# Move model to selected device
model.to(DEVICE)

# Set evaluation mode
model.eval()




def predict_category(article: str) -> str:
    # 1. Clean the article
    cleaned_article = preprocess_text(article)

    # 2. Convert text into TF-IDF features
    features = vectorizer.transform([cleaned_article])

    # 3. Convert sparse TF-IDF matrix into a dense PyTorch tensor
    features = torch.tensor(
        features.toarray(),
        dtype=torch.float32,
        device=DEVICE
    )

    # 4. Make prediction
    with torch.no_grad():
        logits = model(features)

    # 5. Get predicted class index
    predicted_index = logits.argmax(dim=1).item()

    # 6. Convert index into category name
    return CLASS_NAMES[predicted_index]