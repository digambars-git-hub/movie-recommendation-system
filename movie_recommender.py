from __future__ import annotations

import difflib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SELECTED_FEATURES = ["genres", "keywords", "tagline", "cast", "director"]
REQUIRED_COLUMNS = {"title", *SELECTED_FEATURES}


@dataclass
class MovieRecommender:
    movies_data: pd.DataFrame
    similarity_matrix: List[List[float]]

    def recommend_movies(self, movie_name: str, top_n: int = 10) -> Tuple[str, List[Dict[str, float]]]:
        """
        Notebook-aligned recommendation function.
        Returns:
        - close_match: best fuzzy title match from dataset
        - recommendations: list of {title, score}
        """
        cleaned_input = (movie_name or "").strip()
        if not cleaned_input:
            raise ValueError("Please enter a movie name.")

        list_of_all_titles = self.movies_data["title"].tolist()
        find_close_match = difflib.get_close_matches(cleaned_input, list_of_all_titles, n=1, cutoff=0.4)
        if not find_close_match:
            raise ValueError("No close movie match found. Try another title.")

        close_match = find_close_match[0]

        # Use row index to avoid dependence on dataset's 'index' column values.
        row_index = self.movies_data[self.movies_data["title"] == close_match].index[0]
        similarity_score = list(enumerate(self.similarity_matrix[row_index]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

        recommendations: List[Dict[str, float]] = []
        for candidate_index, score in sorted_similar_movies:
            title_from_index = self.movies_data.iloc[candidate_index]["title"]

            # Skip the same movie and duplicate titles.
            if title_from_index == close_match:
                continue
            if any(item["title"] == title_from_index for item in recommendations):
                continue

            recommendations.append({"title": title_from_index, "score": float(score)})
            if len(recommendations) >= top_n:
                break

        return close_match, recommendations


def resolve_dataset_path() -> Path:
    load_dotenv()
    configured_path = os.getenv("FILE_PATH")
    if configured_path:
        normalized = configured_path.strip().strip("\"'")
        return Path(normalized).expanduser()
    return Path(__file__).resolve().parent / "movies.csv"


def run_preflight_checks(dataset_path: Path) -> List[str]:
    issues: List[str] = []

    if not dataset_path.exists():
        issues.append(f"Dataset not found at: {dataset_path}")
        return issues

    try:
        head_df = pd.read_csv(dataset_path, nrows=10)
    except Exception as exc:  # pragma: no cover
        issues.append(f"Could not read dataset: {exc}")
        return issues

    missing_columns = sorted(REQUIRED_COLUMNS - set(head_df.columns))
    if missing_columns:
        issues.append(f"Dataset is missing required columns: {', '.join(missing_columns)}")

    return issues


def build_recommender(dataset_path: Path) -> MovieRecommender:
    movies_data = pd.read_csv(dataset_path)

    for feature in SELECTED_FEATURES:
        movies_data[feature] = movies_data[feature].fillna("")

    combined_features = (
        movies_data["genres"]
        + " "
        + movies_data["keywords"]
        + " "
        + movies_data["tagline"]
        + " "
        + movies_data["cast"]
        + " "
        + movies_data["director"]
    )

    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)

    return MovieRecommender(movies_data=movies_data, similarity_matrix=similarity)
