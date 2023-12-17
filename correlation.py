import numpy as np


def correlate(base: object, kernel: object, expected: object=None) -> np.ndarray:
    if expected is None:
        expected = np.sum(np.abs(kernel))
    transform_down = np.zeros((base.shape[0], base.shape[0]))
    for i in range(1, base.shape[0]):
        transform_down[i, i - 1] = 1

    transform_up = np.zeros((base.shape[0], base.shape[0]))
    for i in range(1, base.shape[0]):
        transform_up[i - 1, i] = 1

    filter_matrixes = [np.zeros((base.shape[1], base.shape[1])) for _ in range(kernel.shape[1])]

    correlation = np.zeros_like(base)
    for idx, filter_matrix in enumerate(filter_matrixes):
        for i in range(base.shape[1]):
            filter_matrix[
            max(0, i - kernel.shape[0] // 2):min(base.shape[1], i + kernel.shape[0] - kernel.shape[0] // 2),
            i] = kernel[
                 max(0, (kernel.shape[0] // 2) - i): min(kernel.shape[0], base.shape[1] - i + kernel.shape[0] // 2),
                 idx]
        base_shifted = base
        if idx < kernel.shape[1] // 2:
            for i in range((kernel.shape[1] // 2) - idx):
                base_shifted = transform_down.dot(base_shifted)
        else:
            for i in range(idx - (kernel.shape[1] // 2)):
                base_shifted = transform_up.dot(base_shifted)
        correlation = correlation + base_shifted.dot(filter_matrix)

    return 1 * (correlation == expected)


def correlate_rotated(base, kernel, expected_value=None):
    return (1 * ((correlate(base, kernel, expected_value) +
                  correlate(base, np.fliplr(kernel), expected_value) +
                  correlate(base, np.flipud(kernel), expected_value) +
                  correlate(base, np.fliplr(np.flipud(kernel)), expected_value) +
                  correlate(base, kernel.transpose(), expected_value) +
                  correlate(base, np.fliplr(kernel.transpose()), expected_value) +
                  correlate(base, np.flipud(kernel.transpose()), expected_value) +
                  correlate(base, np.fliplr(np.flipud(kernel.transpose())), expected_value)) > 0))


if __name__ == '__main__':
    size = 10
    base = np.zeros((size, size))

    base[3, 2] = 1
    base[3, 3] = 1
    base[2, 3] = 1
    kernel = np.array([[1, 1, 0],
                       [1, 0, 0],
                       [0, 0, 0]])

    expected_value = 3
