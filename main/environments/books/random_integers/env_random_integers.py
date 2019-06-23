import numpy as np

def get_data():
    data = []
    for i in range(100):
        data.append(i)
    data = np.asarray(data)
    return {'input_integers':data, 'output_integers':data}
