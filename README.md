# MAQ: Massive Quantum Programming Language

MAQ is a revolutionary quantum computing programming language designed to handle simulations and operations on a massive scale, with support for up to **150 trillion qubits**. This repository provides the compiler, runtime, and examples needed to explore the potential of MAQ.

---

## Features

- **Custom Quantum Compiler**: Tokenization, parsing, and transpilation to Qiskit circuits.
- **Distributed Simulations**: Leverages Dask for large-scale quantum simulations.
- **Predefined Quantum Algorithms**: Includes Shor's Algorithm, quantum teleportation, and more.
- **Interactive Visualizations**: Analyze results of quantum computations interactively using Streamlit and Plotly.

---

## Installation

### Clone the Repository
```bash
git clone https://github.com/marciolscoutinho/maq.git
cd maq
```

### Install Dependencies
Ensure you have Python 3.8+ installed. Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Verify Installation
Run the following command to ensure the setup works:
```bash
python cli/main.py examples/teleport.qp
```

---

## Usage

### Running MAQ Programs
Execute MAQ programs using the CLI:
```bash
python cli/main.py <path_to_file.qp>
```

Example:
```bash
python cli/main.py examples/teleport.qp
```

### Running Shor's Algorithm
Use the provided implementation of Shor's Algorithm:
```bash
python algorithms/shors_algorithm.py <number_to_factor>
```

Example:
```bash
python algorithms/shors_algorithm.py 15
```

---

## Examples

### Quantum Teleportation
The `examples/teleport.qp` file demonstrates quantum teleportation using MAQ:
```plaintext
H(0);
CNOT(0, 1);
MEASURE(0);
MEASURE(1);
IF(0) THEN X(2);
IF(1) THEN Z(2);
```
Run it with:
```bash
python cli/main.py examples/teleport.qp
```

### Distributed Simulation
The `examples/distributed_simulation.py` script showcases distributed simulation for large quantum circuits:
```bash
python examples/distributed_simulation.py
```

---

## Contributing

We welcome contributions to MAQ! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request on GitHub.

---

## License

MAQ is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgements

- Built using [Qiskit](https://qiskit.org/) for quantum circuit simulations.
- Inspired by advancements in quantum computing and scalable programming languages.

---
