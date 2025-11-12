from braket.devices import LocalSimulator
from braket.circuits import Circuit

device = LocalSimulator()
circ = Circuit().h(0).measure(0)

result = device.run(circ, shots=200).result()
print("Measurement counts:", dict(result.measurement_counts))
