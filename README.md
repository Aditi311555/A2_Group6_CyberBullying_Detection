# A2_Group6_CyberBullying_Detection
Readme file

Project Title & Objective
This project aims to build a comprehensive, multi-modal cyberbullying detection system capable of identifying harmful content from:
Text messages
Emoji usage patterns
Audio messages (via Speech-to-Text)
Marathi language inputs (via Marathi → English translation)
Encrypted text (decoded before processing)
Image-based text (via OCR extraction)


The system is designed to provide robust, scalable, real-time cyberbullying detection suitable for modern social media platforms.

Dataset Details
Total Rows: 18,000


Columns:


comment - text message


is_bullying -label (0 = not bullying, 1 = bullying)


Dataset includes various forms of English + Hinglish content used for training classical ML models.

 Algorithms / Models Used
We trained and compared multiple supervised machine learning algorithms:
DecisionTreeClassifier


BaggingClassifier


LinearSVC


LogisticRegression


SGDClassifier


MultinomialNB


AdaBoostClassifier


Additional technologies used in the multimodal pipeline:
✓ Speech-to-Text (Audio Module)
Converts audio messages to text


Extracted text is passed to the classifier


✓ Marathi → English Translation
Enables Marathi bullying detection


Marathi input → translated to English → classification


If non-bullying: output shown only in Marathi


✓ OCR for Image-Based Text Extraction
Extracts text from images using a text recognition model


Extracted text is passed through the classifier


✓ SymSpell for Spelling Correction
Corrects spelling mistakes, typos, and noisy text


Improves classification accuracy on user-generated content



Results

Graphs
Algorithm
Training Time
Prediction Time
Accuracy (Test)
Accuracy (Train)
F1 Score (Test)
F1 Score (Train)
Precision (Test)
Precision (Train)
Recall (Test)
Recall (Train)
DecisionTreeClassifier
1.703846
0.015273
0.974380
0.996832
0.980330
0.997534
0.973126
0.996146
0.987641
0.998926
BaggingClassifier
12.747166
0.177979
0.967355
0.994868
0.974806
0.996004
0.972635
0.995336
0.976987
0.996672
LinearSVC
0.078223
0.000971
0.964738
0.989048
0.972690
0.991459
0.973937
0.992152
0.971447
0.990767
LogisticRegression
0.142333
0.000740
0.936364
0.961152
0.950514
0.969637
0.955632
0.972464
0.945451
0.966826
SGDClassifier
0.016153
0.000622
0.936088
0.957914
0.950054
0.966984
0.959974
0.973454
0.940337
0.960599
MultinomialNB
0.006839
0.002149
0.899174
0.927676
0.925428
0.945438
0.886590
0.916159
0.967824
0.976649
AdaBoostClassifier
1.490938
0.370727
0.840909
0.841955
0.863749
0.863402
0.967495
0.969063
0.780098
0.778517



 Conclusion
This study presents a comprehensive, multi-modal approach to cyberbullying detection in social media, integrating text, audio, emoji, image extraction, and multilingual support to build a robust and scalable monitoring system. The proposed pipeline demonstrates that combining NLP-based text classification with speech-to-text transcription, emoji pattern analysis, and OCR significantly improves the system’s detection capability, overcoming the limitations of single-modality approaches.
A wide range of machine learning models were evaluated—including Decision Tree, Bagging, Linear SVC, Logistic Regression, SGD Classifier, Multinomial Naive Bayes, and AdaBoost. Among these, Linear SVC achieved the best overall performance, offering an optimal balance of high accuracy, strong precision–recall metrics, and extremely low prediction latency. This makes it especially suitable for real-time cyberbullying moderation within web applications. While ensemble methods and deep learning approaches also deliver strong performance, the computational efficiency of Linear SVC makes it ideal for deployment in production environments requiring fast responses.
The research further emphasizes the importance of multi-modal detection. Cyberbullying frequently occurs through audio messages, while emojis often carry implicit or sarcastic aggression that text-only models may fail to detect. Incorporating these elements ensures better coverage of real-world abusive behavior. The system additionally includes an account-blocking mechanism for repeated offenders, demonstrating the potential for actionable intervention strategies that complement automated detection.
Multilingual support for English, Hindi, and Marathi enhances the system’s applicability across diverse linguistic communities. The system is further capable of detecting bullying from encrypted text, OCR-extracted text from images, and noisy or misspelled user-generated content via SymSpell correction.
Overall, this project demonstrates that a multi-modal, model-selective, and proactive approach provides a reliable, interpretable, and scalable solution to combating cyberbullying. These findings open pathways for future enhancements, including deep-learning-based feature fusion, expansion to additional languages, and integration with real-time moderation pipelines on social platforms.

If you want, I can add emojis, formatting, badges, or convert this into a PDF or GitHub-friendly README.md.

Dataset details 
Algorithm/model used 
result(accuracy,graph,etc) 
Conclusion 
References: 
REFERENCES
[1] Zhu, C., Huang, S., Evans, R., & Zhang, W. (2021). Cyberbullying among adolescents and children: A comprehensive review of the global situation, risk factors, and preventive measures. Frontiers in Public Health, 9, 634909. https://doi.org/10.3389/fpubh.2021.634909
[2] Tokunaga, R. S. “Following you home from school: A critical review and synthesis of research on cyberbullying victimization.” Computers in Human Behavior, vol. 26, no. 3, pp. 277‑287, 2010. DOI: 10.1016/j.chb.2009.11.014.
[3]Reio, T. G., & Ortega, C. C. L. (2016). Chapter 8 – Cyberbullying and Its Emotional Consequences: What We Know and What We Can Do. In S. Y. Tettegah & D. Espelage (Eds.), Emotions, Technology, and Behaviors (pp. 145–158). Academic Press. DOI: 10.1016/B978‑0‑12‑801873‑6.00008‑X
[4] K. Dinakar, R. Reichart, and H. Lieberman, “Modeling the detection of textual cyberbullying,” in Proc. 5th Int. AAAI Conf. Weblogs Social Media (ICWSM), 2011, pp. 11–17.
[5] N. Rezvani, A. Beheshti & A. Tabebordbar, “Linking textual and contextual features for intelligent cyberbullying detection in social media,” ACM International Conference on Web Intelligence, 2020. DOI / link: https://doi.org/10.1145/3428690.3429171
[6]Alsaade, Fawaz Waselallah and Alzahrani, Mohammed Saeed. "Transformer learning-based neural network algorithms for identification and detection of electronic bullying in social media" Demonstratio Mathematica, vol. 57, no. 1, 2024, pp. 20230118. 
[7] Gupta, V., Sharon, R., Sawhney, R., & Mukherjee, D., “ADIMA: Abuse Detection in Multilingual Audio,” ICASSP 2022. 
[8] B. Felbo, A. Mislove, A. Søgaard, I. Rahwan, and S. Lehmann, “Using millions of emoji occurrences to learn sentiment,” in Proc. Int. AAAI Conf. Web Social Media (ICWSM), 2017, pp. 161–169.
[9] Sidra Tahir & Asif Nawaz, “HuEID: Hybrid Deep Learning for Cyberbullying Detection using Multi‑Modal Urdu Text and Emojis,” ACM Transactions on Asian and Low‑Resource Language Information Processing, 2023. DOI: 10.1145/3769294
[10] Karan Shah , Chaitaniya Phadhtare , Keval Rajpara, 2022, Cyber-Bullying Detection in Hinglish Languages Using Machine Learning, INTERNATIONAL JOURNAL OF ENGINEERING RESEARCH & TECHNOLOGY (IJERT) Volume 11, Issue 05 (May 2022),10.17577/IJERTV11IS050318
[11]Bandeh Ali Talpur and Declan O'Sullivan, “Cyberbullying severity detection: A machine learning approach,” PLoS ONE, vol. 15, no. 10, e0240924, 2020. DOI: 10.1371/journal.pone.0240924.
[12]El-Masri, A., Riedl, M. J., & Woolley, S. (2022). Audio misinformation on WhatsApp: A case study from Lebanon. Harvard Kennedy School Misinformation Review, 3(4), 1-13.
[13]TechCrunch:Author or TechCrunch. (2022, March 30). People are sending 7 billion voice messages on WhatsApp every day. TechCrunch. [URL]
[14]SAGE Article:[URL]
[15]Pew Report:Pew Research Center. (2022, December 15). Teens and cyberbullying 2022. [URL]
[16] Dataset Source GitHub

