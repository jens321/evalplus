import os
import subprocess
from tqdm import tqdm


DATA_DIR = '/home/t-jenstuyls/inference-rlhf/data/mbpp'

for root, dirs, files in tqdm(os.walk(DATA_DIR), desc='Evaluating folders ...'):
    for file in tqdm(files, desc='Evaluating files in folder ...'):
        if file.endswith('.jsonl') and 'raw' not in file:
            if os.path.exists(os.path.join(root, file.replace('.jsonl', '.eval_results.json'))):
                print('skipping', file)
                continue

            if 'prompt-idx-119' in file:
                continue
        
            print('root', root)
            print('file', file)
            subprocess.run(['docker', 'run', '--rm', '--pull=always', '-v', f'{root}:/app', '-v', '/home/t-jenstuyls/evalplus/evalplus:/app/evalplus', 'ganler/evalplus:latest', 'python3', '-m', 'evalplus.evaluate', '--dataset', 'mbpp', '--samples', f'/app/{file}', '--parallel', '80'])
            # kill evalplus.evaluate process
            os.system('sudo pkill -9 -f "evalplus.evaluate"')
            print('done')

