
# CV Analysis & Matching System

## Overview
The CV Analysis & Matching System is a Streamlit-based web application that analyzes CVs against job descriptions using natural language processing and machine learning techniques. It provides skill matching, recommendations, and generates detailed reports for job seekers.

## Use Cases
- **Job Seekers:** Evaluate how well your CV matches specific job descriptions and get actionable recommendations to improve your chances.
- **Career Coaches:** Help clients identify gaps between their resumes and industry/job requirements.
- **Recruiters & HR Teams:** Quickly assess applicant suitability based on skill match and similarity scoring.
- **Learning & Development:** Identify trending or required technical skills and tailor upskilling plans for individuals or teams.
- **Academic Institutions:** Guide students in preparing industry-aligned CVs and recommend relevant courses for bridging skill gaps.

## Features
- PDF document processing for both CVs and job descriptions  
- Technical skill extraction and matching  
- Similarity scoring between CV and job requirements  
- Detailed skills gap analysis  
- Downloadable analysis reports  
- Real-time recommendations for skill development  

## Technical Requirements
```python
streamlit
sentence-transformers
scikit-learn
pandas
pypdf
langchain-community
python-magic-bin; sys_platform == 'win32'
nest-asyncio
spacy
```

## Installation

Clone the repository:
```bash
git clone [repository-url]
cd cv-analysis-system
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install required packages:
```bash
pip install -r requirements.txt
```

Download the required spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

Access the application through your browser (typically http://localhost:8501)

### Upload Process:
1. Upload a job description (PDF format)  
2. Upload one or more CVs (PDF format)  
3. Click **"Analyze CV"** to get results  

---

## Features in Detail

### Document Processing
- Supports PDF format for both CVs and job descriptions  
- Extracts text content while maintaining document structure  
- Handles multi-page documents  

### Skills Analysis
- Extracts technical skills from both documents  
- Identifies matching and missing skills  
- Provides percentage match scoring  
- Lists top 10 current and required skills  

### Recommendations
- Provides targeted recommendations for skill development  
- Suggests top 5 priority skills to acquire  
- Offers actionable insights for improvement  

### Report Generation
- Creates downloadable CSV reports  
- Includes match percentages and detailed skill analysis  
- Provides comprehensive skill gap assessment  

---

## Project Structure
```
cv-analysis-system/
│
├── app.py                 # Main application file  
├── requirements.txt       # Project dependencies  
├── README.md              # Project documentation  
└── .gitignore             # Git ignore file
```

---

## Technical Implementation
- Uses `sentence-transformers` for semantic similarity matching  
- Implements `spaCy` for natural language processing  
- Utilizes `PyPDF` for PDF text extraction  
- Built with `Streamlit` for the web interface  
- Employs `scikit-learn` for similarity calculations  

---

## Limitations
- Currently supports PDF format only  
- Requires clear text extraction from PDFs  
- English language support only  
- Limited to technical skill analysis  

---

## Future Improvements
- Support for additional document formats  
- Multi-language support  
- Enhanced skill extraction algorithms  
- More detailed recommendation system  
- Interactive visualization features  

---

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## Author
**Eunice Muriithi**

---

## Acknowledgments
- [Streamlit](https://streamlit.io/) for the wonderful web framework  
- [Sentence-Transformers](https://www.sbert.net/) for powerful NLP capabilities  
- [SpaCy](https://spacy.io/) for excellent NLP tools  
