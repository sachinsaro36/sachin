try:
    import numpy, pandas, matplotlib, seaborn, sklearn, nltk, spacy, flask, streamlit, joblib, requests
    print("All libraries are installed and working!")
except ImportError as e:
    print("Missing library:",e.name)