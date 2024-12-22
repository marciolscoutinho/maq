### File: `shors_algorithm.py`

import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit.library import QFT
from dask.distributed import Client, wait
import tracemalloc

def gcd(a, b):
    """Computes the greatest common divisor using Euclid's algorithm."""
    while b != 0:
        a, b = b, a % b
    return a

def modular_exponentiation(a, x, N):
    """Performs modular exponentiation a^x % N."""
    return pow(a, x, N)

def apply_modular_exp(circuit, base, power, N, num_qubits):
    """
    Applies modular exponentiation to the circuit.
    Args:
        circuit: QuantumCircuit object.
        base: Base of the modular exponentiation.
        power: Exponent value.
        N: Modulus.
        num_qubits: Number of qubits in the computational register.
    """
    for i in range(power):
        circuit.append(modular_multiplier(base, N, num_qubits), range(num_qubits))

def modular_multiplier(base, N, num_qubits):
    """
    Creates a modular multiplication circuit.
    Args:
        base: Base value.
        N: Modulus.
        num_qubits: Number of qubits.
    """
    multiplier = QuantumCircuit(num_qubits)
    for i in range(num_qubits):
        multiplier.cx(i, (i + base) % num_qubits)
    return multiplier.to_gate()

def quantum_order_finding(a, N):
    """
    Quantum order-finding circuit to compute the order 'r' of 'a' modulo 'N'.
    """
    # Determine number of qubits needed
    num_qubits = int(np.ceil(np.log2(N)))
    num_ancilla_qubits = num_qubits + 1

    # Create quantum circuit
    circuit = QuantumCircuit(num_qubits + num_ancilla_qubits, num_qubits)

    # Apply Hadamard to the control qubits
    for i in range(num_qubits):
        circuit.h(i)

    # Apply modular exponentiation
    apply_modular_exp(circuit, a, 2**num_qubits, N, num_qubits)

    # Apply Quantum Fourier Transform (QFT) on control qubits
    circuit.append(QFT(num_qubits, do_swaps=True).to_gate(), range(num_qubits))

    # Measure control qubits
    circuit.measure(range(num_qubits), range(num_qubits))

    return circuit

def classical_postprocessing(measurements, a, N):
    """
    Processes quantum results to find the order.
    """
    counts = measurements.get_counts()
    most_common_state = max(counts, key=counts.get)

    # Convert binary measurement to integer
    measured_value = int(most_common_state, 2)
    q = 2 ** len(most_common_state)

    # Find the order using continued fractions
    frac = measured_value / q
    numerator, denominator = approximate_fraction(frac)

    return denominator

def approximate_fraction(decimal, max_denominator=1000):
    """Finds the closest fraction to a given decimal."""
    n, d = 0, 1
    for i in range(1, max_denominator + 1):
        test_d = round(i * decimal)
        test_n = i
        if abs(test_d - decimal * test_n) < 1e-10:
            n, d = test_d, test_n
    return n, d

def shor_distributed(N, client):
    """
    Distributed implementation of Shor's Algorithm.
    Args:
        N: Integer to be factored.
        client: Dask client for distributed computation.
    """
    tracemalloc.start()

    # Step 1: Choose a random integer a such that gcd(a, N) = 1
    a = np.random.randint(2, N)
    while gcd(a, N) != 1:
        a = np.random.randint(2, N)

    print(f"Random a chosen: {a}")

    # Step 2: Quantum order finding
    def build_circuit():
        circuit = quantum_order_finding(a, N)
        backend = Aer.get_backend("qasm_simulator")
        result = execute(circuit, backend, shots=1024).result()
        return result.get_counts()

    # Submit task to Dask cluster
    future = client.submit(build_circuit)
    result = client.gather(future)

    # Memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Memory usage: Current = {current / 10**6:.2f} MB, Peak = {peak / 10**6:.2f} MB")

    # Step 3: Classical postprocessing
    order = classical_postprocessing(result, a, N)
    print(f"Order found: {order}")

    # Step 4: Check if the order gives factors of N
    if order % 2 == 1 or pow(a, order // 2, N) == -1:
        print("Order did not yield factors. Retrying...")
        return shor_distributed(N, client)

    # Compute factors
    factor1 = gcd(pow(a, order // 2) - 1, N)
    factor2 = gcd(pow(a, order // 2) + 1, N)

    return factor1, factor2

# Example Usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python shors_algorithm.py <number_to_factor>")
        sys.exit(1)

    try:
        N = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid integer.")
        sys.exit(1)

    if N <= 1:
        print("Number must be greater than 1.")
        sys.exit(1)

    print(f"Attempting to factorize: {N}")

    # Initialize Dask client
    client = Client()

    factors = shor_distributed(N, client)
    print(f"Factors of {N}: {factors}")
