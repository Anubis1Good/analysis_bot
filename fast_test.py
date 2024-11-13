import os
from global_test import main
from tqdm import tqdm

folders = os.listdir('docs')

for folder in tqdm(folders):
    main(folder)