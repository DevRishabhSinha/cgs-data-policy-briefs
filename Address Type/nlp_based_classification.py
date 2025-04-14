import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def classify_with_nlp(df, reference_categories):
    """
    Classifies ambiguous cases using NLP and cosine similarity.
    
    Parameters:
        df: DataFrame containing ambiguous cases.
        reference_categories: Dictionary with reference texts for each category.
        
    Returns:
        DataFrame with NLP-based classifications.
    """
    # Combine location name and address into a single text column
    df['CombinedText'] = df['LocName'] + " " + df['address']
    
    # Generate TF-IDF embeddings for all texts
    vectorizer = TfidfVectorizer(stop_words='english')
    text_embeddings = vectorizer.fit_transform(df['CombinedText'])
    
    # Generate embeddings for reference categories
    reference_texts = list(reference_categories.values())
    reference_embeddings = vectorizer.transform(reference_texts)
    
    # Compute cosine similarity between each text and reference categories
    similarity_scores = cosine_similarity(text_embeddings, reference_embeddings)
    
    # Assign category with highest similarity score
    df['NLPClassification'] = similarity_scores.argmax(axis=1).apply(
        lambda idx: list(reference_categories.keys())[idx]
    )
    
    return df

# Example usage
reference_categories = {
    'EV Charging Station': "Electric vehicle charging station",
    'Hotel/Lodging': "Hotel or lodging facility",
    'Shopping Center': "Shopping mall or plaza",
}
df_ambiguous = pd.read_csv("ambiguous_cases.csv")  # Replace with your CSV file path
classified_df = classify_with_nlp(df_ambiguous, reference_categories)
