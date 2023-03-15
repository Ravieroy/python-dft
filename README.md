# Iterative solution to Kohn-Sham equations for a harmonic oscillator
This is a python code to solve Kohn-Sham equations for a 1D harmonic oscillator using LDA approximation as outlined in  [Write a simple 1D DFT code in Python](http://dcwww.camd.dtu.dk/~askhl/files/python-dft-exercises.pdf) by Ask Hjorth Larsen and Keenan Lyon. I have tried to solve all the exercises in as much pedagogical way as possible.

We will be solving the following hamiltonian and calculate Kohn-Sham wavefunctions, the density and each of the potentials required to represent the Hamiltonian. 

$$\hat{H} = \hat{T} = -\frac12 \frac{d^2}{dx^2} + x^2 + v_{Ha}(x) + v_X^{LDA}(x)$$
### Directory Tree
python-dft
├── notebooks
│   ├── 1-differential-operators.ipynb
│   ├── 2-non-interacting-electrons.ipynb
│   ├── 3-harmonic-oscillator.ipynb
│   ├── 4-density-HO.ipynb
│   ├── 5-exchange-energy-HO.ipynb
│   ├── 6-coulomb-potential-HO.ipynb
│   └── 7-self-consistent-DFT-HO.ipynb
├── python-dft-exercises.pdf
└── utils.py