import numpy as np

def sample_with_temperature(predictions, temperature=1.0):
    predictions = np.asarray(predictions).astype('float64')
    predictions = np.log(predictions + 1e-8) / temperature
    exp_preds = np.exp(predictions)
    predictions = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, predictions, 1)
    return np.argmax(probas)


def generate_notes(model, seed_sequence, int_to_note, n_vocab,
                    num_notes=200, temperature=0.8):
    pattern = list(seed_sequence)
    prediction_output = []

    for _ in range(num_notes):
        input_seq = np.reshape(pattern, (1, len(pattern), 1))
        input_seq = input_seq / float(n_vocab)

        prediction = model.predict(input_seq, verbose=0)[0]
        index = sample_with_temperature(prediction, temperature)

        prediction_output.append(int_to_note[index])
        pattern.append(index)
        pattern = pattern[1:]

    return prediction_output