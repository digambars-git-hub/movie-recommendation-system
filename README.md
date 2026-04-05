# 🎬 Movie Recommendation App (Streamlit)

A content-based movie recommender built from your notebook pipeline and deployed with a Streamlit frontend.

It uses:
- 🧠 `TF-IDF` on movie metadata (`genres`, `keywords`, `tagline`, `cast`, `director`)
- 📐 `cosine similarity` to find related movies
- 🔎 fuzzy title matching (`difflib`) for user input

## 🌐 Live Demo

Streamlit App Link: **`[ADD_YOUR_STREAMLIT_LINK_HERE]`**

Example:
`https://your-app-name.streamlit.app`

## 📦 Dataset

Dataset Link: **`[ADD_YOUR_DATASET_LINK_HERE]`**

Example:
`https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata`

---

## 📁 Project Structure

```text
movie-recommendation/
├── app.py                 # Streamlit frontend
├── movie_recommender.py   # Recommender backend + checkpoints
├── movies.csv             # Dataset
├── recommender.ipynb      # Original notebook
├── requirements.txt       # Python dependencies
├── .env.example           # Sample env configuration
└── .env                   # Local environment config (ignored in git)
```

---

## ✅ Deployment Checkpoints (What is validated)

The app runs preflight checks before recommendations:

1. ✅ Dataset path resolves correctly (from `.env` or fallback)
2. ✅ Dataset file exists and is readable
3. ✅ Required columns exist:
   - `title`
   - `genres`
   - `keywords`
   - `tagline`
   - `cast`
   - `director`
4. ✅ Recommendation engine builds successfully

If any checkpoint fails, the app shows a clear error in the UI.

---

## ⚙️ Setup (Local)

### 1. Clone and open project

```bash
git clone <your-repo-url>
cd movie-recommendation
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

Create `.env` from sample:

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Then update `.env`:

```env
FILE_PATH=movies.csv
```

You can also use an absolute path:

```env
FILE_PATH=D:/SSD/Coding/movie-recommendation/movies.csv
```

---

## 🚀 Run the Streamlit App

```bash
streamlit run app.py
```

Then open the local URL shown in terminal (usually `http://localhost:8501`).

---

## 🧪 How to Use

1. Enter a movie title (example: `Avatar`, `Inception`, `The Dark Knight`).
2. Choose how many recommendations you want.
3. Click **Recommend Movies**.
4. The app shows:
   - 🎯 best-matched movie title
   - 🍿 recommended movies ranked by similarity

---

## 🔗 Notebook Function Mapping

Your last notebook function is:

```python
def recommend_movies(movie_name):
```

The backend keeps the same recommendation logic and exposes it for the Streamlit app through:

```python
recommender.recommend_movies(movie_name, top_n=10)
```

This makes the notebook logic reusable in a web app.

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push this project to GitHub.
2. Open [https://share.streamlit.io](https://share.streamlit.io).
3. Click **New app**.
4. Select your repo and branch.
5. Set entrypoint file as:
   - `app.py`
6. Add app secrets if needed (optional for this project).
7. Click **Deploy**.

After deploy, copy your app URL and replace this in README:

`[ADD_YOUR_STREAMLIT_LINK_HERE]`

---

## 🛠️ Troubleshooting

- ❗ `FILE_PATH not found in .env`
  - Add `FILE_PATH=movies.csv` in `.env`.

- ❗ Dataset not found
  - Confirm `movies.csv` exists in project root.
  - Or set absolute path in `.env`.

- ❗ No close movie match found
  - Try a more common movie title from dataset.

- ❗ Module not found errors
  - Run `pip install -r requirements.txt` again in active virtual environment.

---

## 🙌 Notes

- `.env` is in `.gitignore`, so local file paths stay private.
- For production, prefer relative path (`movies.csv`) when dataset is in repo.
