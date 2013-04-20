
import pickle,os

def pickle_dump(obj, file_path, rewrite=True):
    file_path = os.path.abspath(file_path)
    if not rewrite and os.path.exists(file_path):
        raise Exception,"file %s exists" %file_path
    _dir = os.path.dirname(file_path)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    with open(file_path, "wb") as fp:
        pickle.dump(obj, fp)
    pass
    

def pickle_load(file_path):
    #with open
    with open(file_path, "rb") as fp:
        return pickle.load(fp)
    pass


if __name__ == "__main__":
    pickle_dump([1,2,3], "./tmp/tmp", True)
    print pickle_load("./tmp/tmp")
