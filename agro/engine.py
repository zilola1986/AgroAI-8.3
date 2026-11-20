"""AgroAI 8.3: binary ResNet18 leaf health estimate."""
from functools import lru_cache
from pathlib import Path
import os
import tempfile

MODEL_ID = 'AgroAI 8.3 — ResNet18, sog‘lom / zararlangan (2 sinf)'
LABELS = ['Sog‘lom barg', 'Zararlangan barg']

@lru_cache(maxsize=1)
def classifier():
    import torch
    from torch import nn
    from torchvision import models
    path = Path(__file__).resolve().parent.parent / 'models' / 'AgroAI_v8_2_binary.pth'
    if not path.is_file():
        import gdown
        path.parent.mkdir(parents=True, exist_ok=True)
        file_id = os.environ.get('AGROAI_MODEL_FILE_ID', '1ZH3_1ifC8b78-a24rAdtAPf6NSHyWAwQ')
        # Temporary download prevents a partial file being treated as a valid model.
        with tempfile.NamedTemporaryFile(dir=path.parent, suffix='.pth', delete=False) as tmp:
            temporary = Path(tmp.name)
        try:
            result = gdown.download(id=file_id, output=str(temporary), quiet=False)
            if not result or not temporary.exists() or temporary.stat().st_size < 1_000_000:
                raise RuntimeError('Google Drive model faylini yuklab bo‘lmadi. Ulashish ruxsatini tekshiring.')
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    checkpoint = torch.load(path, map_location='cpu', weights_only=True)
    if not isinstance(checkpoint, dict):
        raise ValueError('Model fayli kutilgan checkpoint formatida emas.')
    state = checkpoint.get('model_state_dict', checkpoint.get('state_dict', checkpoint))
    if not isinstance(state, dict):
        raise ValueError('Checkpoint ichida model vaznlari topilmadi.')
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(state, strict=True)
    model.eval()
    return model, LABELS

def classify(image):
    import torch
    from torchvision import transforms
    model, labels = classifier()
    prep = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    with torch.inference_mode():
        probs = torch.softmax(model(prep(image.convert('RGB')).unsqueeze(0)), dim=1)[0]
    return [dict(plant='unknown', condition=labels[i], label=labels[i], score=float(probs[i]))
            for i in torch.argsort(probs, descending=True).tolist()]

def assess(rows, chosen=None):
    if not rows:
        return {'status': 'no_result'}
    ranked = sorted(rows, key=lambda x: x['score'], reverse=True)
    results = [dict(x, conditional_score=x['score']) for x in ranked]
    # Uncertain output is shown as uncertain, not forced into a disease diagnosis.
    status = 'estimate' if ranked[0]['score'] >= 0.70 else 'uncertain'
    return {'status': status, 'plant': 'unknown', 'top': results[0],
            'results': results, 'inferred': 'unknown'}
