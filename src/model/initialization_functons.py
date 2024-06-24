import numpy as np

# todo: look for how to setup complex types properly
INIT_TYPE = (
    int,
    int,
    int,
    np.ndarray,
    np.ndarray
 )


def xavier_normal_distribution(
        input_count: int,
        hidden_count: int,
        output_count: int,
        weights_inputs2hidden_ref: np.ndarray,
        weights_hidden2output_ref: np.ndarray,
):
    standard_deviation_hidden = np.sqrt(1. / hidden_count)
    weights_inputs2hidden_ref[:] = np.random.randn(hidden_count, input_count) * standard_deviation_hidden

    standard_deviation_output = np.sqrt(1. / output_count)
    weights_hidden2output_ref[:] = np.random.randn(hidden_count, output_count) * standard_deviation_output


def deep_xavier_normal_distribution(input_count: int, hidden_layers: list, output_count: int, weights: list, biases: list):
    # Initialize input to first hidden layer
    standard_deviation_hidden = np.sqrt(1. / input_count)
    weights[0][:] = np.random.randn(hidden_layers[0], input_count) * standard_deviation_hidden

    # Initialize hidden layers
    for i in range(1, len(hidden_layers)):
        standard_deviation_hidden = np.sqrt(1. / hidden_layers[i - 1])
        weights[i][:] = np.random.randn(hidden_layers[i], hidden_layers[i - 1]) * standard_deviation_hidden

    # Initialize last hidden layer to output layer
    standard_deviation_output = np.sqrt(1. / hidden_layers[-1])
    weights[-1][:] = np.random.randn(output_count, hidden_layers[-1]) * standard_deviation_output


def xavier_uniform_distribution(
        input_count: int,
        hidden_count: int,
        output_count: int,
        weights_inputs2hidden_ref: np.ndarray,
        weights_hidden2output_ref: np.ndarray,
):
    limit_hidden = np.sqrt(6 / (input_count + hidden_count))
    limit_output = np.sqrt(6 / (hidden_count + output_count))

    weights_inputs2hidden_ref[:] = np.random.uniform(-limit_hidden, limit_hidden, (hidden_count, input_count))
    weights_hidden2output_ref[:] = np.random.uniform(-limit_output, limit_output, (hidden_count, output_count))
