import torch.nn as nn
from torch.autograd import Variable
###To Do
###Deep Encoder and Decoder Network
class VAE_C(nn.Module):

    def __init__(self):
        super(VAE_C, self).__init__()
        # encoding layers
        self.e1 = nn.Sequential(nn.Conv2d(3, 32, 4, 2, 1),
                                nn.BatchNorm2d(32),
                                nn.ReLU())
        self.e2 = nn.Sequential(nn.Conv2d(32, 32, 4, 2, 1),
                                nn.BatchNorm2d(32),
                                nn.ReLU())
        self.e3 = nn.Sequential(nn.Conv2d(32, 64, 4, 2, 1),
                                nn.BatchNorm2d(64),
                                nn.ReLU())
        self.e4 = nn.Sequential(nn.Conv2d(64, 64, 4, 2, 1),
                                nn.BatchNorm2d(64),
                                nn.ReLU())
        self.fc = nn.Sequential(nn.Linear(64 * 4 * 4, 512),
                                nn.ReLU())
        self.e2m = nn.Linear(512, 128)
        self.e2s = nn.Linear(512, 128)
        # decode layers
        self.d1 = nn.Linear(128, 512)
        self.d2 = nn.Sequential(nn.Linear(512, 64 * 4 * 4),
                                nn.ReLU())
        self.d3 = nn.Sequential(nn.ConvTranspose2d(64, 64, 4, 2, 1),
                                nn.BatchNorm2d(64),
                                nn.ReLU())
        self.d4 = nn.Sequential(nn.ConvTranspose2d(64, 32, 4, 2, 1),
                                nn.BatchNorm2d(32),
                                nn.ReLU())
        self.d5 = nn.Sequential(nn.ConvTranspose2d(32, 32, 4, 2, 1),
                                nn.BatchNorm2d(32),
                                nn.ReLU())
        self.d6 = nn.Sequential(nn.ConvTranspose2d(32, 3, 4, 2, 1),
                                nn.Tanh())

    def encode(self, x):
        h1 = self.e1(x)
        h2 = self.e2(h1)
        h3 = self.e3(h2)
        h4 = self.e4(h3)
        h4 = h4.view(h4.size(0), -1)
        h5 = self.fc(h4)
        return self.e2m(h5), self.e2s(h5)

    def reparameterize(self, mu, logvar):
        std = logvar.mul(0.5).exp_()
        eps = Variable(std.data.new(std.size()).normal_())
        return eps.mul(std).add_(mu)

    '''
    def reparametrize(self, mu, logvar):
        std = logvar.mul(0.5).exp_()
        #print(std.size(), mu.size())
        eps = Variable(torch.randn(mu.size(0), mu.size(1)).cuda())
        return mu + std.mul(eps)
    '''
    def decode(self, z):
        h1 = self.d1(z)
        h2 = self.d2(h1)
        h2 = h2.view(h2.size(0), -1, 4, 4)
        h3 = self.d3(h2)
        h4 = self.d4(h3)
        h5 = self.d5(h4)
        return self.d6(h5)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar

