import os
from global_test_5m import main
from tqdm import tqdm

folders = os.listdir('docs')

for folder in tqdm(folders):
    main(folder)