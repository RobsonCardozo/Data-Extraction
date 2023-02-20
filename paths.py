import sys
import os

# adiciona o caminho absoluto do diretório 'scripts' ao sys.path
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, 'scripts'))
