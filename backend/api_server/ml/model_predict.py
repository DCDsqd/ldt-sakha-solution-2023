import torch
from torch.nn.functional import softmax


def universal_predict(model, model_is_bert, input_data_text, tokenizer, multi_label_binarizer):
    if model_is_bert:
        inputs = tokenizer(input_data_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = model(**inputs)
        probs = softmax(outputs.logits, dim=1)
        predicted_probabilities, predicted_classes = torch.max(probs, dim=1)
        predicted_labels = [multi_label_binarizer.classes_[idx] for idx in predicted_classes.cpu().numpy()]

        return predicted_labels, predicted_probabilities
    else:
        predicted_probabilities = model.predict_proba([input_data_text])[0]

        threshold = 0
        filtered_predictions = [(label, prob) for label, prob
                                in zip(multi_label_binarizer.classes_, predicted_probabilities)
                                if prob >= threshold]

        predictions_classes = [label for label, _ in filtered_predictions]
        predictions_score = [prob for _, prob in filtered_predictions]

        return predictions_classes, predictions_score
