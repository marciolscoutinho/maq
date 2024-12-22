from dask.distributed import Client
from qiskit import QuantumCircuit, Aer, execute

# Initialize Dask client
client = Client()

def create_circuit(start, end):
    """Creates a quantum circuit for a block of qubits."""
    circuit = QuantumCircuit(end - start)
    for qubit in range(start, end):
        circuit.h(qubit - start)  # Apply Hadamard to each qubit
    circuit.measure_all()  # Measure all qubits
    return circuit

def simulate_circuit(start, end):
    """Simulates a circuit for a given range of qubits."""
    circuit = create_circuit(start, end)
    simulator = Aer.get_backend("qasm_simulator")
    result = execute(circuit, simulator, shots=1024).result()
    return result.get_counts()

# Divide simulation into blocks
num_qubits = 100000
block_size = 1000
blocks = [(i, i + block_size) for i in range(0, num_qubits, block_size)]

# Submit tasks to the Dask client
futures = [client.submit(simulate_circuit, start, end) for start, end in blocks]
results = client.gather(futures)

# Aggregate results
final_counts = {}
for result in results:
    for state, count in result.items():
        final_counts[state] = final_counts.get(state, 0) + count

# Print results
print("Final counts:", final_counts)
