
# YouTube Sentiment Analysis of Prakash Saput’s Audience

**Prakash Saput** is a celebrated Nepali singer and social influencer with over **2.51 million YouTube subscribers**. His work blends **music with activism**, tackling critical societal issues in Nepal. Recently, he faced public controversy for expressing support for PM KP Oli, leading to polarized sentiments online.

This project analyzes **YouTube audience sentiment** on his videos using **Natural Language Processing (NLP)** techniques.

---

## About the Artist (In His Own Words)

> “I'm Prakash Saput, and my life is a story of dreams, music, and a deep commitment to social change. Growing up in Nepal, I found solace in music, beginning as a radio jockey and later releasing songs that addressed critical issues. I've transformed from a village dreamer into a singer, composer, model, actor, and advocate for change. Nepal is my muse, and I'm dedicated to using my voice and art for its positive transformation.”

---

## Dataset Summary

- **Total Comments:** 244,722
- **Columns:** `video_id`, `author`, `comment`
- **Language Mix:**
  - Nepali (Devanagari script)
  - English
  - Romanized Nepali (Nepali written in Latin script)
  - Unknown/symbolic content

---

## Models and Methods

### 1. **TextBlob**
- Pros: Fast and intuitive for English sentiment analysis.
- Features: Tokenization, POS tagging, spelling correction, polarity & subjectivity scoring.
- Limitations:
  - Fails on **Nepali** and **Romanized Nepali**.
  - Returns near-zero sentiment scores for clearly positive local comments like:
    - `Dherai ramro song chha ❤❤`
    - `Music compose मा Jhuma limbu jiu koi name...`

**Example:**
```python
from textblob import TextBlob
text = TextBlob("Songs are really nice heart touching plz we need other songs as well plzzz 🙏🙏")
print(text.sentiment)
# Sentiment(polarity=0.24375, subjectivity=0.71875)
```

## 2. **Multilingual BERT via Hugging Face Transformers**
- Supports: Neplai (Devnagari), English, and several South Asian and European languages
- Limitations: Doesnot handel Romanize Nepali well

**Example**
```python
rom transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
results = sentiment_pipeline(["मलाई यो गीत धेरै राम्रो लाग्यो।", "I hated this movie."])
print(results)
# [{'label': '5 stars', 'score': 0.5550}, {'label': '1 star', 'score': 0.7954}]
```

**Failure case**
-Input: "Dherai ramro song chha ❤❤"
-Output: {'label': '1 star', 'score': 0.28}
-This is Romanized Nepali comment with very positive rating but BERT fails to capture
**Processing steps**
- Dropped Romanized Nepali and unknown/symbolic comments
- Retained only Nepali and English comments
- Truncated long comments to 512 characters (BERT's max input length)
- Final cleaned dataset: 120, 539 comments are obtained

**Key Takeways**
- TexBlob works well for English but fails on mixed scripts and local expressions
- Multilingual BERT performs better for Nepali and English but has limitations on Romanized Nepali
- Preprocessing and language filtering are critical for effective multilingual sentiment analysis
- Over 100,000 valid comments were sucessfully processed with transformer-based sentiment models

