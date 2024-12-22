from qiskit import Aer, execute

class Simulator:
    """
    Simulates quantum circuits using Qiskit's Aer backend.
    """
    def __init__(self, circuit):
        self.circuit = circuit

    def simulate(self, shots=1024):
        """
        Simulates the quantum circuit and returns the result counts.
        Args:
            shots: Number of shots for the simulation.
        Returns:
            A dictionary with quantum state counts.
        """
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(self.circuit, simulator, shots=shots).result()
        return result.get_counts()

    def get_statevector(self):
        """
        Returns the statevector of the quantum circuit.
        Useful for debugging and visualizing quantum states.
        Returns:
            A list of complex amplitudes representing the statevector.
        """
        simulator = Aer.get_backend('statevector_simulator')
        result = execute(self.circuit, simulator).result()
        return result.get_statevector()

    def get_unitary(self):
        """
        Returns the unitary matrix of the quantum circuit.
        Useful for verifying circuit transformations.
        Returns:
            A unitary matrix as a 2D list.
        """
        simulator = Aer.get_backend('unitary_simulator')
        result = execute(self.circuit, simulator).result()
        return result.get_unitary()