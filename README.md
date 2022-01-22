# Convolutional neural network api
[![CodeFactor](https://www.codefactor.io/repository/github/eduardoferrari01/convolutional-neural-network-api/badge/main)](https://www.codefactor.io/repository/github/eduardoferrari01/convolutional-neural-network-api/overview/main)

Rede neural que classifica os animais

# Pré-requisitos para ambiente dev

Instalar as dependências: pip install -r requirements-dev.txt

# Rodando ambiente com Docker

docker build -t cnn-api .

docker run -d -p 8000:8000 --name cnn-api cnn-api
