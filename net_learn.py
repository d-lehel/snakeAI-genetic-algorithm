# amennyiben kisebb mint 0 akkor nem aktivalom
def relu(x):
    return max(0, x)

def forward_propagation(inputs, weights1, biases1, weights2, biases2):
    hidden_layer = [relu(inputs[0] * weights1[0][0] + inputs[1] * weights1[1][0] + biases1[0]),
                    relu(inputs[0] * weights1[0][1] + inputs[1] * weights1[1][1] + biases1[1]),
                    relu(inputs[0] * weights1[0][2] + inputs[1] * weights1[1][2] + biases1[2])
                    ]

    outputs = [hidden_layer[0] * weights2[0][0] + hidden_layer[1] * weights2[1][0] + hidden_layer[2] * weights2[2][0] + biases2[0],
               hidden_layer[0] * weights2[0][1] + hidden_layer[1] * weights2[1][1] + hidden_layer[2] * weights2[2][1] + biases2[1]]

    return outputs

weights1 = [[1, -1, 0.5], [-0.5, 1, -1]]
biases1 = [-1, 0, 1] # annak merese hogy mennyire aktivalhato a neuron - neuron erzekenysege
weights2 = [[1, 0.5], [-1, 1], [0, -1]]
biases2 = [0, 1] # annak merese hogy egy bizonyos imput mennyire probalja aktivalni a kov node-ot

print(forward_propagation([2, 3], weights1, biases1, weights2, biases2))


