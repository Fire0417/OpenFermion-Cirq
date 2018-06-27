#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from typing import List, Optional, Tuple

import numpy

import cirq
from cirq import abc


class VariationalAnsatz(metaclass=abc.ABCMeta):
    """A variational ansatz.

    A variational ansatz is a parameterized circuit. The VariationalAnsatz class
    stores parameters as instances of the Symbol class. A Symbol is simply a
    named object that can be used in a circuit and whose numerical value is
    determined at run time. The Symbols are stored in a dictionary whose keys
    are the names of the corresponding parameters. For instance, the Symbol
    corresponding to the parameter 'theta_0' would be obtained with the
    expression `self.params['theta_0']`.

    Attributes:
        params: A dictionary storing the parameters by name. Key is the
            string name of a parameter and the corresponding value is a Symbol
            with the same name.
        circuit: The ansatz circuit.
        qubits: A list containing the qubits used by the ansatz circuit.
    """
    # TODO use metaclass to enforce existence of attributes

    def __init__(self):
        # Populate the params dictionary based on the output of param_names
        self.params = {param_name: cirq.Symbol(param_name)
                       for param_name in self.param_names()}
        # Generate the ansatz circuit
        self.circuit = self.generate_circuit()

    @abc.abstractmethod
    def param_names(self) -> List[str]:
        """The names of the parameters of the ansatz."""
        pass

    def param_bounds(self) -> Optional[List[Tuple[float, float]]]:
        """Optional bounds on the parameters.

        Returns a list of tuples of the form (low, high), where low and high
        are lower and upper bounds on a parameter. The order of the tuples
        corresponds to the order of the parameters in the list returned by
        the param_names method.
        """
        return None

    @abc.abstractmethod
    def generate_circuit(self) -> cirq.Circuit:
        """Produce the ansatz circuit.

        The circuit should act on the qubits stored in `self.qubits` and use
        Symbols stored in `self.params`. To access the Symbol associated with
        the parameter named 'some_parameter_name', use the expression
        `self.params['some_parameter_name']`.
        """
        pass

    def param_resolver(self, param_values: numpy.ndarray) -> cirq.ParamResolver:
        """Interprets parameters input as an array of real numbers."""
        # Default: leave the parameters unchanged
        return cirq.ParamResolver(dict(zip(self.param_names(), param_values)))

    def default_initial_params(self) -> numpy.ndarray:
        """Suggested initial parameter settings."""
        # Default: zeros
        return numpy.zeros(len(self.params))