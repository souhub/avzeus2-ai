import numpy as np
import pandas as pd
import torch
from torch import tensor
from torch.nn import Module, Parameter
from torch.optim import Adam

#INPUTS_PATH = '/opt/ml/inputs/'
INPUTS_PATH = '../inputs/'


class minus_log_likelihood(Module):

    def __init__(self, x, y):

        super(minus_log_likelihood, self).__init__()

        self.theta1 = Parameter(torch.Tensor([1.0]))
        self.theta2 = Parameter(torch.Tensor([1.0]))
        self.theta3 = Parameter(torch.Tensor([1.0]))
        self.theta4 = Parameter(torch.Tensor([1.0]))
        self.theta5 = Parameter(torch.Tensor([1.0]))
        x = np.array(x).reshape((len(x), -1))
        self.l = tensor(np.dot(x, x.T))
        x = x.reshape((1, len(x), -1))
        x_ = x.transpose((2, 1, 0))
        x__ = x.transpose((2, 0, 1))
        r = ((x_-x__) ** 2).sum(axis=0)
        self.delta = tensor(np.where(r == 0, 1, 0), dtype=float)
        self.r = tensor(r, dtype=float)
        self.y = tensor(np.array(y).reshape(-1, 1), dtype=float)

    def forward(self):

        K = self.theta1 * torch.exp(- self.r / self.theta2) + \
            self.theta3 * self.l + self.theta4 + self.theta5 * self.delta
        yTK_inv = torch.mm(self.y.reshape(1, -1), K.inverse())

        return torch.log(K.det()) + torch.mm(yTK_inv, self.y).reshape(-1)

    def theta(self):

        return [
            np.array(self.theta1.detach())[0],
            np.array(self.theta2.detach())[0],
            np.array(self.theta3.detach())[0],
            np.array(self.theta4.detach())[0],
            np.array(self.theta5.detach())[0]
        ]


def best_theta(data_x, data_y, n=50):

    mll = minus_log_likelihood(data_x, data_y)
    optim = Adam(mll.parameters(), lr=0.01)
    for i in range(n):

        optim.zero_grad()
        loss = mll()
        loss.backward()
        optim.step()

    return mll.theta()


def kernel(data_x, data_x_prime, theta1, theta2, theta3, theta4, theta5):
    data_x = np.array(data_x).reshape((len(data_x), -1))
    data_x_prime = np.array(data_x_prime).reshape((len(data_x_prime), -1))
    l = np.dot(data_x, data_x_prime.T)
    data_x = np.array(data_x).reshape((1, len(data_x), -1))
    data_x_prime = np.array(data_x_prime).reshape((1, len(data_x_prime), -1))
    data_x = data_x.transpose((2, 1, 0))
    data_x_prime = data_x_prime.transpose((2, 0, 1))
    r = ((data_x-data_x_prime) ** 2).sum(axis=0)
    delta = np.where(r == 0, 1, 0)

    return theta1 * np.exp(- r / theta2) + theta3 * l + theta4 + theta5 * delta
    # return np.exp(- np.sqrt(r) / theta2)
    # return np.exp(theta1 * np.cos(np.sqrt(r) / theta2))


def gaussian_regression_f(data_x, data_y, domain_x, theta1, theta2, theta3, theta4, theta5):

    K = kernel(data_x.copy(), data_x.copy(), theta1, theta2, theta3,
               theta4, theta5)  # + sig_y * np.eye(len(data_x))
    k_ = kernel(data_x.copy(), domain_x.copy(),
                theta1, theta2, theta3, theta4, theta5)
    kTKinv = k_.T @ np.linalg.inv(K)

    return (kTKinv @ np.array(data_y).reshape((len(data_y), 1))).reshape(-1)


def recommend_from_score_dict(score_dict: dict) -> list:

    df = pd.read_csv(INPUTS_PATH+'actress_data.csv')
    domain_x = df[['elem']].values.tolist()
    df['id'] = df['id'].map(lambda x: str(x))
    ids = df['id'].tolist()
    #names = df['name'].tolist()
    keys = list(score_dict.keys())
    data_y = np.array(list(score_dict.values()))
    data_y = data_y - data_y.mean()
    data_x = []
    for id_ in keys:

        data_x.append(
            df.loc[df['id'] == id_, 'elem'].values.flatten().tolist())
    data_x = np.array(data_x).reshape(-1)
    theta1, theta2, theta3, theta4, theta5 = best_theta(data_x, data_y, n=50)
    #theta1 = 0
    #theta2 = 1
    theta3 = 0
    theta4 = 0
    theta5 = 0
    z = gaussian_regression_f(data_x, data_y, domain_x,
                              theta1, theta2, theta3, theta4, theta5)
    sort_list = np.argsort(z)[::-1]
    rec_list = []
    i = 0
    while len(rec_list) < 10:

        if not ids[sort_list[i]] in keys:

            rec_list.append(ids[sort_list[i]])

        i += 1

    return rec_list


'''sample'''
score_dict = {'1043077': 0.1,
              '1064775': 0.3,
              '1052094': 0.1,
              '1038230': 0.1,
              '1027944': 0.1,
              '1038466': 0.1,
              #'1061347': 0.1,
              }
output = recommend_from_score_dict(score_dict)
print(output)
