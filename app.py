import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
import pandas as pd
import os
import asyncio
import nest_asyncio
import tempfile
import spacy
import warnings
warnings.filterwarnings('ignore')

# Handle async
try:
    nest_asyncio.apply()
except Exception:
    pass

if not asyncio._get_running_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Load models
@st.cache_resource
def load_spacy():
    try:
        return spacy.load("en_core_web_sm")
    except:
        st.warning("Downloading language model...")
        os.system("python -m spacy download en_core_web_sm")
        return spacy.load("en_core_web_sm")

@st.cache_resource
def load_model():
    try:
        return SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

nlp = load_spacy()
model = load_model()
if model is None:
    st.stop()

st.title("CV Analysis & Matching System")

def safe_load_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        return " ".join(page.extract_text() for page in reader.pages)
    except Exception as e:
        st.error(f"Error loading PDF: {str(e)}")
        return None

def extract_skills_and_keywords(text):
    doc = nlp(text.lower())
    skills = set()
    
    # Get noun phrases
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) <= 3:
            skills.add(chunk.text.strip())
    
    # Add named entities
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
            skills.add(ent.text.strip())
    
    # Technical keywords
    technical_keywords = ['Python programming', 'R programming', 'SQL', 'Relational databases (e.g., MySQL, PostgreSQL)', 
                          'Non-relational databases (e.g., MongoDB, Cassandra)', 'Scikit-learn', 
                          'TensorFlow', 'Keras', 'Tableau', 'Power BI', 'Matplotlib', 'Seaborn', 'Statistical analysis and modeling', 
                          'Data visualization', 'Machine learning', 'Data science methodologies', 'Analytical problem-solving', 
                          'English communication (verbal and written)']

    
    for keyword in technical_keywords:
        if keyword in text.lower():
            skills.add(keyword)
    
    return list(skills)

def analyze_improvement_areas(job_text, cv_text):
    job_skills = set(extract_skills_and_keywords(job_text))
    cv_skills = set(extract_skills_and_keywords(cv_text))
    
    missing_skills = job_skills - cv_skills
    matching_skills = job_skills.intersection(cv_skills)
    
    skill_match_percentage = (len(matching_skills) / len(job_skills) * 100) if job_skills else 0
    
    return {
        'missing_skills': list(missing_skills),
        'matching_skills': list(matching_skills),
        'skill_match_percentage': skill_match_percentage
    }


def display_analysis_results(analysis_results):
    """Display a focused analysis of skills."""
    st.subheader("Skills Analysis")
    
    # Display match percentage
    skill_match = analysis_results['skill_match_percentage']
    st.metric("Technical Skills Match", f"{skill_match:.1f}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Current Technical Skills**")
        matching_skills = sorted(list(set(analysis_results['matching_skills'])))[:10]
        if matching_skills:
            for skill in matching_skills:
                st.write(f"• {skill}")
        else:
            st.write("No matching technical skills found")
    
    with col2:
        st.write("**Required Technical Skills to Develop**")
        missing_skills = sorted(list(set(analysis_results['missing_skills'])))[:10]
        if missing_skills:
            for skill in missing_skills:
                st.write(f"• {skill}")
        else:
            st.write("No skill gaps identified")
    
    # Add concise recommendation
    if missing_skills:
        st.write("\n**Recommendation:**")
        st.write(f"To increase your job match potential, focus on developing expertise in: {', '.join(missing_skills[:5])}. "
                "Consider taking relevant courses or working on projects that utilize these technologies.")

# Create tabs
tab1, tab2 = st.tabs(["Upload Job Description", "Analyze CV"])

# Tab 1: Job Description
with tab1:
    st.header("Upload Job Description")
    uploaded_job = st.file_uploader("Upload Job Description (PDF format)", type="pdf", key="job_description_uploader")
    
    if uploaded_job:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_job.getvalue())
            job_path = tmp_file.name
        
        st.success("Job description uploaded successfully!")
        job_text = safe_load_pdf(job_path)
        if job_text:
            with st.expander("Preview Job Description"):
                st.text(job_text[:500] + "...")

# Tab 2: CV Analysis
with tab2:
    st.header("Upload and Analyze CV")
    
    if 'job_path' not in locals():
        st.warning("Please upload a job description first.")
        st.stop()
    
    uploaded_cv = st.file_uploader("Upload CV (PDF format)", type="pdf", key="cv_document_uploader")
    
    if uploaded_cv:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_cv.getvalue())
            cv_path = tmp_file.name

        cv_text = safe_load_pdf(cv_path)
        os.unlink(cv_path)

        if cv_text and st.button("Analyze CV"):
            try:
                with st.spinner("Analyzing CV..."):
                    job_text = safe_load_pdf(job_path)
                    
                    if job_text:
                        # Calculate similarity score
                        job_embedding = model.encode(job_text, convert_to_tensor=False)
                        cv_embedding = model.encode(cv_text, convert_to_tensor=False)
                        score = float(cosine_similarity([job_embedding], [cv_embedding])[0][0])
                        match_percentage = round(score * 100, 2)

                        # Display results
                        st.subheader("Overall Match Results")
                        st.markdown(f"**Match Score: {match_percentage}%**")
                        st.progress(score)
                        
                        # Skills analysis
                        analysis_results = analyze_improvement_areas(job_text, cv_text)
                        display_analysis_results(analysis_results)
                        
                        # Generate report
                        report_data = {
                            "CV Name": [uploaded_cv.name],
                            "Overall Match (%)": [match_percentage],
                            "Skills Match (%)": [analysis_results['skill_match_percentage']],
                            "Matching Skills": [", ".join(analysis_results['matching_skills'])],
                            "Missing Skills": [", ".join(analysis_results['missing_skills'])]
                        }
                        df = pd.DataFrame(report_data)
                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "Download Report",
                            csv,
                            file_name="cv_analysis_report.csv",
                            mime="text/csv"
                        )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Cleanup
if 'job_path' in locals():
    try:
        os.unlink(job_path)
    except:
        pass

st.markdown("---")
st.markdown("Everyday Is a Learning Day. LoC IN!!--Eunice")
