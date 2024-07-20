import numpy as np
from src.model.activation_functions import sigmoid, sigmoid_gradient
from src.model.initialization_functons import INIT_TYPE, deep_xavier_normal_distribution
import copy


class DeepNeuralNet:
    def __init__(self, input_count: int, hidden_layers: list, output_count: int, activation: callable,
                 initialization: callable = None, learning_rate: np.float32 = 0.1):
        self.input_count = input_count
        self.hidden_layers = hidden_layers
        self.output_count = output_count
        self.activation = activation
        self.learning_rate = learning_rate

        # Initialize weights and biases
        self.weights = []
        self.biases = []

        # Input to first hidden layer
        self.weights.append(np.random.randn(hidden_layers[0], input_count))
        self.biases.append(np.zeros(hidden_layers[0]))

        # Hidden layers
        for i in range(1, len(hidden_layers)):
            self.weights.append(np.random.randn(hidden_layers[i], hidden_layers[i - 1]))
            self.biases.append(np.zeros(hidden_layers[i]))

        # Last hidden layer to output layer
        self.weights.append(np.random.randn(output_count, hidden_layers[-1]))
        self.biases.append(np.zeros(output_count))

        # Apply custom initialization if provided
        if initialization is not None:
            initialization(input_count, hidden_layers, output_count, self.weights, self.biases)

        print(f'Initialized weights: {self.weights}')
        print(f'Initialized biases: {self.biases}')

    def clone_and_mutate(self, mutation_rate: np.float32):
        # Clone the current neural network
        cloned_net = copy.deepcopy(self)

        # Apply mutation to the weights and biases
        def mutate(array: np.ndarray, rate: np.float32):
            mutation = np.random.randn(*array.shape) * rate
            array += mutation

        for w in cloned_net.weights:
            mutate(w, mutation_rate)
        for b in cloned_net.biases:
            mutate(b, mutation_rate)

        return cloned_net

    def feed_forward(self, inputs: np.ndarray) -> np.ndarray:
        current_output = inputs
        # print(f'Input: {inputs}')

        for hidden_l_index in range(len(self.hidden_layers)):
            current_output = np.matmul(current_output, self.weights[hidden_l_index].T)
            current_output += self.biases[hidden_l_index]
            current_output = self.activation(current_output)
            # print(f'Layer {i} activation: {current_output}')

        # Output layer
        current_output = np.matmul(current_output, self.weights[-1].T)
        current_output += self.biases[-1]
        current_output = self.activation(current_output)
        # print(f'Output activation: {current_output}')

        return current_output

    def back_propagation(self, inputs: np.ndarray, targets: np.ndarray):
        # Forward pass
        activations = [inputs]
        current_output = inputs

        for hidden_index in range(len(self.hidden_layers)):
            current_output = np.matmul(current_output, self.weights[hidden_index].T)
            current_output += self.biases[hidden_index]
            current_output = self.activation(current_output)
            activations.append(current_output)

        # Output layer
        current_output = np.matmul(current_output, self.weights[-1].T)
        current_output += self.biases[-1]
        outputs = self.activation(current_output)
        activations.append(outputs)

        # Calculate output error
        output_errors = targets - outputs
        output_gradients = sigmoid_gradient(outputs) * output_errors
        output_gradients *= self.learning_rate

        # Update weights and biases for the output layer
        self.weights[-1] += np.outer(output_gradients, activations[-2])
        self.biases[-1] += output_gradients

        # Debug prints for gradients and weight updates
        # print(f'Output errors: {output_errors}')
        # print(f'Output gradients: {output_gradients}')
        # print(f'Updated output weights: {self.weights[-1]}')
        # print(f'Updated output biases: {self.biases[-1]}')

        # Backpropagate through hidden layers
        next_gradients = output_gradients
        for hidden_index in range(len(self.hidden_layers) - 1, -1, -1):
            hidden_errors = np.dot(next_gradients, self.weights[hidden_index + 1])
            hidden_gradients = sigmoid_gradient(activations[hidden_index + 1]) * hidden_errors
            hidden_gradients *= self.learning_rate

            self.weights[hidden_index] += np.outer(hidden_gradients, activations[hidden_index])
            self.biases[hidden_index] += hidden_gradients

            next_gradients = hidden_gradients

            # Debug prints for hidden gradients and weight updates
            # print(f'Layer {i} errors: {hidden_errors}')
            # print(f'Layer {i} gradients: {hidden_gradients}')
            # print(f'Updated weights layer {i}: {self.weights[i]}')
            # print(f'Updated biases layer {i}: {self.biases[i]}')


if __name__ == '__main__':
    # XOR TEST
    xor_training_data = [
        {'inputs': np.array([0, 0]), 'targets': np.array([0])},
        {'inputs': np.array([1, 1]), 'targets': np.array([0])},
        {'inputs': np.array([1, 0]), 'targets': np.array([1])},
        {'inputs': np.array([0, 1]), 'targets': np.array([1])},
    ]

    nn = DeepNeuralNet(2, [3, 3, 3, 3], 1,
                       initialization=deep_xavier_normal_distribution,
                       activation=sigmoid,
                       learning_rate=np.float32(.1))

    print('UN-trained output ....')
    print(nn.feed_forward(np.array([0, 0])))
    print(nn.feed_forward(np.array([1, 1])))
    print(nn.feed_forward(np.array([1, 0])))
    print(nn.feed_forward(np.array([0, 1])))

    for epoch in range(980 * 1000):
        for data in xor_training_data:
            nn.back_propagation(data.get('inputs'), data.get('targets'))

    print('Trained output ....')
    for i in range(9):
        print(f'{i}.......')
        print(nn.feed_forward(np.array([0, 0])))
        print(nn.feed_forward(np.array([1, 1])))
        print(nn.feed_forward(np.array([1, 0])))
        print(nn.feed_forward(np.array([0, 1])))