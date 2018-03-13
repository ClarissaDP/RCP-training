Auxílio ao treinamento de reanimação cardiopulmonar (RCP)
---------------------------------------------------------

Criar um algoritmo para auxiliar o treinamento de RCP,
a partir da observação de imagens em vídeo, centrada na posição e
no movimento dos braços do agente operador do procedimento e na
alternância entre compressões e ventilações na técnica.

******************************************

[Proposta de projeto](https://pt.sharelatex.com/project/597f1c819b5fee58a6c87121)

******************************************

#### Próximos passos: ####

* [X] Escolher melhor ângulo para avaliar as tecnicalidades do processo

* [X] Avaliar a possibilidade de adotar mecanismos para identificar a posição dos braços do agente (marker)

* [X] Implementar mecanismo para calibrar tamanho no vídeo, para poder calcular a distância que um objeto (marker) se moveu

* [ ] Calcular a distância que um objeto (marker) se moveu

* [ ] Calcular a velocidade que um objeto (marker) se moveu

#### Detalhes: ####

- Saída de arquivos será direcionada para o diretório `../outputs_rcp`


******************************************

#### Linux ####

*Requisitos:*

- Python 2.7
- OpenCV > 3.0
- Imutils

*How to run:*

```sh
python main.py -h
```

******************************************

#### Windows ####

*Requisitos:*

- Python 2.7 -> [MSI installer](https://www.python.org/downloads/release/python-2714/)
- Opencv > 3.0 -> `"C:\Python27\Scripts\pip" install opencv-python`
- Imutils -> `"C:\Python27\Scripts\pip" install imutils`

*How to run:*

```sh
"C:\Python27\python.exe" "main.py" -h
```

__OBS.:__ Atualmente só funciona para vídeos, não com a webcam.

******************************************
###### Clarissa Dreischerf Pereira ######
