# python-utils
Simple and useful codes for AI/DL python researches

### Pickle loader
Pickle loader shows load status progress bar through tqdm.  
Performs the same function as `pickle.load(f)`.

How to use:  
```python
from utils.loaders import load_pickle

data = load_pickle('./path_to_pickle/file.pkl', 'My pickle')
```

### Torch weight loader
Torch weight loader shows load status progress bar through tqdm.  
Performs the same function as `torch.load()`.

How to use:  
```python
from utils.loaders import load_model

state_dict = load_model('./path_to_torch_weight/file.pth', 'My model')
```