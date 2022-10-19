import yaml


def load_file(filename):
    f = open("./sample/" + filename, 'r', encoding='utf-8')
    file = f.read()
    key = yaml.safe_load(file)
    return key
