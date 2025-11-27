# Offline-Chatbot-for-Secondary-School-Physics

An offline, retrieval-based Physics chatbot designed to help students from **Class 8 to Class 12** understand NCERT physics concepts.  
The application runs completely offline, uses TF-IDF–based semantic retrieval, and provides quick, concept-level answers along with topic and class filtering.

---

## 🚀 Features

### ✅ **Completely Offline**
No internet connection required — all data and models are stored locally.

### ✅ **NCERT-Aligned Content**
Includes curated explanations for key topics from Classes 8–12:
- Motion  
- Force & Laws of Motion  
- Work, Energy & Power  
- Gravitation  
- Electricity  
- Magnetism  
- Light  
- Waves  
- Modern Physics  
and more.

### ✅ **Intelligent Retrieval Engine**
Uses:
- **TF-IDF vectorization**
- **Cosine similarity**
- **Topic & class-level filtering**
- **Similarity thresholds** to avoid wrong answers

This ensures only relevant responses are shown, and the chatbot avoids random guessing.

### ✅ **Simple & Clean GUI**
Built using Python’s `tkinter`:
- Dropdown filters for **class** and **topic**
- Chat-style interface
- “Show topics info” helper popup
- Scrollable conversation area

### ✅ **Expandable Knowledge Base**
All physics concepts are stored in a single JSON file:
```
data/physics_knowledge.json
```
You can easily add more entries or modify existing ones.

---

## 🧠 How It Works

### 1. **Knowledge Base (KB)**
Physics concepts are stored in structured JSON entries containing:
- class level  
- topic & subtopic  
- question (representation)  
- answer (main content)  
- type (concept, comparison, etc.)  

### 2. **Model Building**
Running `build_model.py`:
- Loads the KB  
- Creates TF-IDF vectors  
- Generates a similarity matrix  
- Saves three model files:
  - `vectorizer.pkl`
  - `knowledge_matrix.npz`
  - `knowledge_index.json`

### 3. **Chat Engine**
When the user asks a question:
- TF-IDF vector is created
- Cosine similarity finds closest KB entries
- Topic/class filters refine the results
- A threshold prevents irrelevant answers
- Best match is shown along with optional related topics

### 4. **User Interface**
The GUI interacts with the engine:
- Displays responses
- Handles class & topic selection
- Accepts user questions
- Shows fallback messages if no suitable answer is found

---

## 📂 Project Structure

```
project/
│
├── app.py                 # GUI application
├── engine.py              # ChatEngine orchestrator
├── model.py               # TF-IDF model logic
├── data_loader.py         # Paths & data loading utilities
├── build_model.py         # Builds and saves TF-IDF model
│
├── data/
│   ├── physics_knowledge.json   # Main knowledge base
│   ├── vectorizer.pkl           # TF-IDF vectorizer
│   ├── knowledge_matrix.npz     # TF-IDF matrix
│   └── knowledge_index.json     # Indexed KB
│
└── requirements.txt       # Dependencies
```

---

## 🛠️ Installation & Setup

1. **Create a virtual environment**
```
python -m venv .venv
```

2. **Activate it**
- Windows:
```
.\.venv\Scripts\activate
```

3. **Install dependencies**
```
pip install -r requirements.txt
```

4. **Build the model**
```
python build_model.py
```

5. **Run the application**
```
python app.py
```

---

## ✨ Customizing the Knowledge Base

Open:

```
data/physics_knowledge.json
```

Each entry follows this structure:

```json
{
  "id": 37,
  "class_level": 12,
  "topic": "Modern Physics",
  "subtopic": "Photoelectric effect",
  "type": "concept",
  "difficulty": "medium",
  "question": "What is the photoelectric effect?",
  "answer": "The photoelectric effect is ..."
}
```

Simply add more entries or modify existing ones, then re-run:

```
python build_model.py
```

---

## 📦 Packaging (Optional)

You can convert this project into a standalone `.exe` using:
```
pyinstaller --onefile app.py
```

(Ensure the `data/` folder stays alongside the build or bundle it in.)

---

## 📝 License
This project is for educational and non-commercial use.  
All NCERT content belongs to their respective owners.

---

## 🤝 Contributions
Feel free to extend the knowledge base or improve the retrieval logic.
