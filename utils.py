from scipy.sparse import diags
import numpy as np
from scipy.integrate import simps


def derivative(f, a=0, h=0.01):
    '''
    Returns the first-derivative of function f using forward difference method

            Parameters:
                    f (array): function
                    a (float): initial value
                    h (float): step size

            Returns:
                    first-derivative of function f(array)
    '''
    return (f(a + h) - f(a))/(2*h)


def second_derivative(f, a=0, h=0.01):
    '''
    Returns the second-derivative of function f

            Parameters:
                    f (array): function
                    a (float): initial value
                    h (float): step size

            Returns:
                    secnd-derivative of function f(array)
    '''
    return (f(a - h) - 2*f(a) + f(a + h))/(h ** 2)


def D(x, N=100):
    '''
    Returns the operator form of first-derivative

            Parameters:
                    x (array): grid of 1D array
                    N (int): number of points on the grid

            Returns:
                    D (array): first-derivative operator
    '''
    h = x[1] - x[0]
    k = [np.ones(N-1), -np.ones(N-1)]
    offset = [1, -1]
    D = diags(k, offset).toarray()
    D = D/(2 * h)
    # # Boundary values where it is not well defined
    D[0, 0] = 0
    D[0, 1] = 0
    D[1, 0] = 0
    D[N-1, N-2] = 0
    D[N-2, N-1] = 0
    D[N-1, N-1] = 0
    return D


def D2(x, N=100):
    '''
    Returns the operator form of second-derivative

            Parameters:
                    x (array): grid of 1D array
                    N (int): number of points on the grid

            Returns:
                    D (array): first-derivative operator
    '''
    h = x[1] - x[0]
    k1 = [np.ones(N-1), -2*np.ones(N), np.ones(N-1)]
    offset = [-1, 0, 1]
    D2 = diags(k1, offset).toarray()
    D2 = D2/(h ** 2)
    # Boundary values where it is not well defined
    D2[0, 0] = 0
    D2[0, 1] = 0
    D2[1, 0] = 0
    D2[N-1, N-2] = 0
    D2[N-2, N-1] = 0
    D2[N-1, N-1] = 0
    return D2


def normalise_psi(psi, x):
    '''
    Normalises the given wavefunction

            Parameters:
                    psi (array): wavefunction psi
                    x (array): 1D grid of array

            Returns:
                    normalised psi
    '''
    int_psi_square = simps(abs(psi) ** 2, x)
    return psi/np.sqrt(int_psi_square)


def get_occupation_num(nElectron, maxElectron=2):
    '''
    Returns a list of occupation numbers for a given number of electrons

            Parameters:
                    nElectron (int): number of electrons
                    maxElectron (int): max number of allowed elecrons in one state

            Returns:
                    fn (array): occupation number
    '''
    nFloor = np.floor_divide(nElectron, 2)
    fn = maxElectron * np.ones(nFloor)
    if nElectron % 2:
        fn = np.append(fn, 1)
    return fn


def get_density(nElectron, psi, x):
    '''
    Returns electron density for a given number of electrona and wavefunction

            Parameters:
                    nElectron (int): number of electrons
                    psi (array): wavefunction
                    x (array): 1D grid of array

            Returns:
                    eDensity (array): electron density
    '''
    psiNorm = normalise_psi(psi, x)  # Normalisation
    fn = get_occupation_num(nElectron)
    eDensity = np.zeros(N)
    for f_n, psi in zip(fn, psiNorm.T):
        eDensity += f_n * (psi ** 2)
    return eDensity


def integrate(x, y):
    '''
    Returns the integration by simpson's method

            Parameters:
                    x (array): 1D grid of arra
                    y (array): integrand

            Returns:
                    result (float): result of the integration
    '''
    result = simps(y, x)
    return result


def calculate_exchange(eDensity, x):
    '''
    Returns exchange energy and potential for a given electron density

            Parameters:
                    eDensity (array): electron density
                    x (array): 1D grid of array

            Returns:
                    energy (float): exchange energy
                    potential (float): exchange potential
    '''
    energy = -3/4 * (3/np.pi) ** (1/3) * integrate(x, eDensity ** (4/3))
    potential = -(3/np.pi) ** (1/3) * eDensity ** (1/3)
    return energy, potential


def calculate_coulomb(eDensity, x, eps=0.1):
    '''
    Returns Coulomb/Hartree energy and potential for a given electron density

            Parameters:
                    eDensity (array): electron density
                    x (array): 1D grid of array

            Returns:
                    energy (float): Hartee energy
                    potential (float): Hartree potential
    '''
    h = x[1] - x[0]
    nx = eDensity[np.newaxis, :]
    nxp = eDensity[:, np.newaxis]
    w = x[np.newaxis, :]
    wp = x[:, np.newaxis]
    energy = 0.5 * np.sum(nx * nxp * h ** 2/np.sqrt((w - wp) ** 2 + eps))
    potential = np.sum((nx * h)/np.sqrt((w - wp) ** 2 + eps), axis=-1)
    return energy, potential