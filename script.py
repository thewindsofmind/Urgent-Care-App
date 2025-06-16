import math
import random

def calculate_similarity(user_symptoms, disease_symptoms):
    """Calculates the Jaccard similarity between two sets of symptoms."""
    user_set = set(user_symptoms)
    disease_set = set(disease_symptoms)
    intersection = len(user_set.intersection(disease_set))
    union = len(user_set.union(disease_set))
    if union == 0:
        return 0.0
    return intersection / union

def calculate_weighted_similarity(user_symptoms, disease_symptoms, symptom_weights):
    """Calculates weighted similarity, giving more importance to specific symptoms."""
    weighted_intersection = 0.0
    weighted_union = 0.0
    user_set = set(user_symptoms)
    disease_set = set(disease_symptoms)

    for symptom in user_set.intersection(disease_set):
        weighted_intersection += symptom_weights.get(symptom, 1.0) #Default weight 1 if not specified
    for symptom in user_set.union(disease_set):
        weighted_union += symptom_weights.get(symptom, 1.0)

    if weighted_union == 0:
        return 0.0
    return weighted_intersection / weighted_union

def bayesian_probability(prior_probability, likelihood, evidence):
    """Calculates the posterior probability using Bayes' theorem."""
    if evidence == 0:
      return 0.0
    return (likelihood * prior_probability) / evidence

def diagnose(user_symptoms, disease_data, symptom_weights, prior_probabilities):
    """Diagnoses the user based on symptoms and disease data."""
    results = []
    total_evidence = 0.0
    likelihoods = {}

    for disease, symptoms in disease_data.items():
        likelihoods[disease] = calculate_weighted_similarity(user_symptoms, symptoms, symptom_weights)
        total_evidence += likelihoods[disease]

    for disease, symptoms in disease_data.items():
        prior = prior_probabilities.get(disease, 0.01) #default prior 0.01 if not given
        posterior = bayesian_probability(prior, likelihoods[disease], total_evidence)
        results.append((disease, posterior))

    results.sort(key=lambda x: x[1], reverse=True)
    return results

def get_symptom_weights(disease_data):
    """Simple weighting example based on frequency of symptoms across diseases."""
    all_symptoms = []
    for symptoms in disease_data.values():
        all_symptoms.extend(symptoms)
    symptom_counts = {}
    for symptom in all_symptoms:
        symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
    symptom_weights = {}
    for symptom, count in symptom_counts.items():
        symptom_weights[symptom] = 1.0 / math.sqrt(count) #Less frequent symptoms get higher weights
    return symptom_weights

def get_prior_probabilities(disease_data):
    """Simulates prior probabilities based on disease prevalence (very basic)."""
    priors = {}
    total_diseases = len(disease_data)
    for disease in disease_data:
        priors[disease] = random.uniform(0.001, 0.1) #Simulates varying prevalence
    return priors

# Example disease data (replace with a comprehensive database)
disease_data = {
    "Common Cold": ["sore throat", "runny nose", "cough", "sneezing", "headache"],
    "Flu": ["fever", "body aches", "cough", "fatigue", "sore throat", "headache"],
    "Allergies": ["sneezing", "runny nose", "itchy eyes", "cough"],
    "Migraine": ["headache", "nausea", "sensitivity to light", "sensitivity to sound"],
    "Appendicitis": ["abdominal pain", "nausea", "vomiting", "fever"],
    "Pneumonia": ["cough", "fever", "chest pain", "shortness of breath", "fatigue"],
    # ... add many more diseases and symptoms here ...
}

# Get symptom weights and prior probabilities
symptom_weights = get_symptom_weights(disease_data)
prior_probabilities = get_prior_probabilities(disease_data)

# User input
user_input = input("Enter your symptoms (comma-separated): ")
user_symptoms = [s.strip().lower() for s in user_input.split(",")]

# Diagnosis
results = diagnose(user_symptoms, disease_data, symptom_weights, prior_probabilities)

# Output
print("\nPossible Diagnoses:")
for disease, probability in results[:5]:  # Display top 5 results
    print(f"{disease}: {probability:.4f}")

print("\nDisclaimer: This is not a substitute for professional medical advice. Consult a doctor for accurate diagnosis and treatment.")

