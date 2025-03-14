import os
from transformers import pipeline

# Sample explanations for different profiles
data_profiles = {
    "English_Executive": "Digital transformation helps businesses stay competitive by adopting new technologies.",
    "English_Technical": "Digital transformation involves integrating cloud computing, AI, and automation into business workflows, requiring API-based architectures and scalable data solutions.",
    
    "French_Executive": "La transformation numérique aide les entreprises à rester compétitives en adoptant de nouvelles technologies.",
    "French_Technical": "La transformation numérique implique l'intégration de l'informatique en nuage, de l'intelligence artificielle et de l'automatisation dans les flux de travail de l'entreprise, nécessitant des architectures basées sur les API et des solutions de données évolutives.",

    "Spanish_Executive": "La transformación digital ayuda a las empresas a mantenerse competitivas adoptando nuevas tecnologías.",
    "Spanish_Technical": "La transformación digital implica la integración de la computación en la nube, la inteligencia artificial y la automatización en los flujos de trabajo empresariales, lo que requiere arquitecturas basadas en API y soluciones de datos escalables."
}

# Function to generate audio using espeak-ng
def text_to_speech(text, filename, lang="en"):
    command = f'espeak-ng -v {lang} -w {filename} "{text}"'
    os.system(command)
    print(f"Generated: {filename}")

# Loop through profiles and generate audio files
for profile, text in data_profiles.items():
    lang_code = "en" if "English" in profile else "fr" if "French" in profile else "es"
    filename = f"{profile}.wav"
    text_to_speech(text, filename, lang_code)




summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
text = "Full concatenated policy text for country AFG :  Sporadic Five-year plan Five-year plan Afghanistan (2014) Country Afghanistan Target, Renewable energy target, Political & non-binding renewable energy target Electricity and heat, Renewables 500 megawatts of power is to be generated from renewable sources by 2020 in keeping with the five-year plan. Renewables Ended 2014 2020 Unknown Energy security, Mitigation, Energy access https://www.globalissues.org/news/2014/02/13/18230 | Sporadic Intended Nationally Determined Contribution - INDC Intended Nationally Determined Contribution - INDC Afghanistan (2015) Country Afghanistan Target, GHG reduction target, Political & non-binding GHG reduction target General There will be a 13.6% reduction in GHG emissions by 2030 compared to a business"
summary_output = summarizer(text)
print(summary_output)

