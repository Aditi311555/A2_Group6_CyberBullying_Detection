# A2_Group6_CyberBullying_Detection
Readme file

Here's a **clean and professional README file** for your project, formatted in Markdown and designed to be GitHub-ready. You can copy-paste this into `README.md` directly.

---

# 🚨 Multi-Modal Cyberbullying Detection System

## 🎯 Project Objective

This project aims to build a comprehensive **multi-modal cyberbullying detection system**, designed to detect harmful or offensive content from a variety of input formats:

* 📝 **Text messages**
* 😊 **Emoji usage patterns**
* 🎤 **Audio messages** (via Speech-to-Text)
* 🌐 **Marathi message detection** (via Marathi → English translation)
* 🔐 **Encrypted or obfuscated text detection** (e.g., `f**k`, `f*k`)
* 🖼️ **Image-based text detection** (via OCR extraction)

The system is built to be **real-time, scalable, and practical for modern social media platforms**.

---

## 📊 Dataset Details

* **Total Rows:** 18,000
* **Features:**

  * `comment`: Text message (English + Hinglish)
  * `is_bullying`: Binary label

    * `0 = Not Bullying`
    * `1 = Bullying`

Dataset includes real-world, noisy, multilingual, and code-mixed text to improve model robustness.

---

## 🤖 Machine Learning Models Used

We trained and compared the following algorithms:

* `DecisionTreeClassifier`
* `BaggingClassifier`
* `LinearSVC` ← **Final model**
* `LogisticRegression`
* `SGDClassifier`
* `MultinomialNB`
* `AdaBoostClassifier`

---

## 🧠 Multi-Modal Pipeline Components

### 🎤 Speech-to-Text

* Converts audio messages to text
* Text sent to classifier for bullying detection

### 🌐 Marathi → English Translation

* Supports Marathi bullying detection
* Marathi input → translated to English → classified
* If result is benign, output is shown in Marathi

### 🖼️ OCR for Image-Based Text

* Extracts text from images using OCR
* Text is classified and flagged if abusive

### ✍️ SymSpell Spell Correction

* Corrects typos, noisy inputs, obfuscated text
* Improves accuracy for user-generated content

---

## 📈 Results

| Model                  | Train Time | Predict Time | Test Acc   | Train Acc  | Test F1    | Train F1   | Test Precision | Train Precision | Test Recall | Train Recall |
| ---------------------- | ---------- | ------------ | ---------- | ---------- | ---------- | ---------- | -------------- | --------------- | ----------- | ------------ |
| DecisionTreeClassifier | 1.70s      | 0.015s       | 97.43%     | 99.68%     | 98.03%     | 99.75%     | 97.31%         | 99.61%          | 98.76%      | 99.89%       |
| BaggingClassifier      | 12.74s     | 0.177s       | 96.74%     | 99.48%     | 97.48%     | 99.60%     | 97.26%         | 99.53%          | 97.69%      | 99.66%       |
| **LinearSVC**          | **0.078s** | **0.0009s**  | **96.47%** | **98.90%** | **97.26%** | **99.14%** | **97.39%**     | **99.21%**      | **97.14%**  | **99.07%**   |
| LogisticRegression     | 0.142s     | 0.0007s      | 93.63%     | 96.11%     | 95.05%     | 96.96%     | 95.56%         | 97.24%          | 94.54%      | 96.68%       |
| SGDClassifier          | 0.016s     | 0.0006s      | 93.60%     | 95.79%     | 95.00%     | 96.69%     | 95.99%         | 97.34%          | 94.03%      | 96.05%       |
| MultinomialNB          | 0.006s     | 0.0021s      | 89.91%     | 92.76%     | 92.54%     | 94.54%     | 88.66%         | 91.61%          | 96.78%      | 97.66%       |
| AdaBoostClassifier     | 1.49s      | 0.3707s      | 84.09%     | 84.19%     | 86.37%     | 86.34%     | 96.74%         | 96.90%          | 78.01%      | 77.85%       |

🟢 **LinearSVC** achieved the best result with excellent accuracy, precision, recall, and extremely low latency — making it ideal for real-time deployment.

---

## 🧩 Conclusion

This project demonstrates a **multi-modal cyberbullying detection pipeline** that effectively integrates:

* Text-based NLP
* Audio message interpretation
* Image-to-text extraction
* Emoji analysis
* Multilingual support
* Encrypted text normalization

By combining several modalities and preprocessing strategies (spell correction, OCR, translation), the system overcomes weaknesses of traditional text-only models and provides reliable, real-time moderation for social media platforms.

🔍 The system also includes support for **blocking repeated offenders**, demonstrating practical intervention potential.

🌍 Multilingual support across **English, Hindi, Marathi**, combined with detection from **encrypted / obfuscated text**, maximizes real-world applicability.

---

## 📚 References

1. Zhu, C., Huang, S., Evans, R., & Zhang, W. (2021). Cyberbullying among adolescents and children: A comprehensive review… *Frontiers in Public Health*, 9, 634909.
2. Tokunaga, R. S. (2010). Following you home from school: A critical review… *Computers in Human Behavior*, 26(3), 277-287.
3. Reio, T.G., & Ortega, C.C.L (2016). Cyberbullying and Its Emotional Consequences… *Emotions, Technology, and Behaviors*.
4. Dinakar, K., Reichart, R., & Lieberman, H. (2011). Modeling Textual Cyberbullying… ICWSM.
5. Rezvani, N., Beheshti, A., & Tabebordbar, A. (2020). Linking textual and contextual features for intelligent cyberbullying detection… *ACM Web Intelligence*.
6. Alsaade, F. W., & Alzahrani, M. S. (2024). Transformer learning-based algorithms for electronic bullying detection… *Demonstratio Mathematica*.
7. Gupta, V., Sharon, R., Sawhney, R., & Mukherjee, D. (2022). ADIMA: Abuse Detection in Multilingual Audio… ICASSP.
8. Felbo, B., Mislove, A., Søgaard, A., Rahwan, I., & Lehmann, S. (2017). Using millions of emoji occurrences… ICWSM.
9. Tahir, S., & Nawaz, A. (2023). HuEID: Hybrid Deep Learning for Cyberbullying Detection… ACM TALLIP.
10. Shah, K., Phadhtare, C., Rajpara, K. (2022). Cyber-Bullying Detection in Hinglish Using ML. *IJERT, 11(05)*.
11. Talpur, B. A., & O'Sullivan, D. (2020). Cyberbullying severity detection: A machine learning approach. *PLOS ONE*.
12. El-Masri, A. et al. (2022). Audio misinformation on WhatsApp… *Harvard Kennedy School Misinformation Review*.
13. TechCrunch (2022). People are sending 7 billion voice messages daily…
14. SAGE Article: [URL]
15. Pew Research Center (2022). Teens and cyberbullying 2022.
16. Dataset Source: GitHub.

---

💡 If you'd like:

* 🖼️ Images
* 📈 Plots
* 🔖 Badges
* 📄 PDF export
* 🧩 Code block examples

Just let me know — I’ll update this accordingly!
 Center. (2022, December 15). Teens and cyberbullying 2022. [URL]
[16] Dataset Source GitHub

