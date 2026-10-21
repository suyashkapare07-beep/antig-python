"""
config.py – Central configuration for the Placement Intelligence System.
All thresholds, skill dictionaries, and job-role definitions live here.
"""

# ── File upload limits ────────────────────────────────────────────────────────
MAX_UPLOAD_SIZE_MB = 5
ALLOWED_EXTENSIONS = {".pdf", ".docx"}

# ── Academic eligibility thresholds (configurable per company tier) ───────────
ELIGIBILITY_TIERS = {
    "Tier 1 (FAANG / Top MNC)": {
        "min_cgpa": 8.0,
        "max_backlogs": 0,
        "min_aptitude": 80,
        "min_projects": 2,
    },
    "Tier 2 (Mid-size MNC)": {
        "min_cgpa": 7.0,
        "max_backlogs": 1,
        "min_aptitude": 65,
        "min_projects": 1,
    },
    "Tier 3 (Startups / SME)": {
        "min_cgpa": 6.0,
        "max_backlogs": 2,
        "min_aptitude": 50,
        "min_projects": 0,
    },
    "Government / PSU": {
        "min_cgpa": 6.5,
        "max_backlogs": 0,
        "min_aptitude": 60,
        "min_projects": 0,
    },
}

# ── Job roles and their required skills ──────────────────────────────────────
JOB_ROLES = {
    "Software Developer": {
        "skills": [
            "python", "java", "c++", "data structures", "algorithms",
            "git", "sql", "rest api", "object oriented programming",
            "javascript", "html", "css", "problem solving",
        ],
        "nice_to_have": ["react", "node.js", "docker", "aws", "system design"],
        "min_projects": 2,
        "description": (
            "Build and maintain software applications. Requires strong "
            "programming fundamentals, data structures, and version control."
        ),
    },
    "Data Analyst": {
        "skills": [
            "python", "sql", "excel", "data visualization", "statistics",
            "pandas", "numpy", "tableau", "power bi", "data cleaning",
        ],
        "nice_to_have": ["machine learning", "r", "matplotlib", "seaborn", "etl"],
        "min_projects": 1,
        "description": (
            "Analyze data to support business decisions. Requires SQL, "
            "Python/R, and data visualization skills."
        ),
    },
    "Machine Learning Engineer": {
        "skills": [
            "python", "machine learning", "deep learning", "scikit-learn",
            "tensorflow", "pytorch", "numpy", "pandas", "statistics",
            "data preprocessing", "model evaluation",
        ],
        "nice_to_have": ["nlp", "computer vision", "mlops", "docker", "cloud"],
        "min_projects": 2,
        "description": (
            "Design and deploy ML models. Requires strong Python, ML libraries, "
            "and a solid statistics foundation."
        ),
    },
    "Web Developer": {
        "skills": [
            "html", "css", "javascript", "react", "node.js",
            "git", "rest api", "responsive design", "sql",
        ],
        "nice_to_have": ["typescript", "next.js", "docker", "mongodb", "figma"],
        "min_projects": 2,
        "description": (
            "Build web applications. Requires front-end and back-end skills, "
            "version control, and API integration."
        ),
    },
    "Cloud / DevOps Engineer": {
        "skills": [
            "linux", "git", "docker", "aws", "ci/cd",
            "python", "bash scripting", "networking basics",
        ],
        "nice_to_have": ["kubernetes", "terraform", "azure", "gcp", "ansible"],
        "min_projects": 1,
        "description": (
            "Manage cloud infrastructure and deployment pipelines. "
            "Requires Linux, containers, and cloud platform knowledge."
        ),
    },
    "Cybersecurity Analyst": {
        "skills": [
            "networking", "linux", "ethical hacking", "cryptography",
            "security protocols", "python", "firewalls", "siem",
        ],
        "nice_to_have": ["penetration testing", "wireshark", "kali linux", "ceh", "cissp"],
        "min_projects": 1,
        "description": (
            "Identify and mitigate security vulnerabilities. Requires networking, "
            "OS, and security tool knowledge."
        ),
    },
    "Business Analyst": {
        "skills": [
            "communication", "sql", "excel", "requirement gathering",
            "data analysis", "ms office", "presentation skills",
        ],
        "nice_to_have": ["power bi", "jira", "agile", "crm", "tableau"],
        "min_projects": 1,
        "description": (
            "Bridge business and technology. Requires analytical thinking, "
            "communication, and domain knowledge."
        ),
    },
}

# ── Comprehensive skill dictionary for resume extraction ─────────────────────
ALL_SKILLS = {
    # Programming Languages
    "programming_languages": [
        "python", "java", "c", "c++", "c#", "javascript", "typescript",
        "kotlin", "swift", "go", "rust", "r", "scala", "ruby", "php",
        "matlab", "dart", "perl", "bash", "powershell",
    ],
    # Web Technologies
    "web": [
        "html", "css", "react", "angular", "vue", "node.js", "express",
        "django", "flask", "fastapi", "spring boot", "next.js", "tailwind",
        "bootstrap", "jquery", "rest api", "graphql", "websocket",
    ],
    # Databases
    "databases": [
        "sql", "mysql", "postgresql", "mongodb", "sqlite", "redis",
        "oracle", "firebase", "dynamodb", "cassandra", "elasticsearch",
        "neo4j", "nosql",
    ],
    # ML / Data Science
    "ml_data": [
        "machine learning", "deep learning", "scikit-learn", "tensorflow",
        "pytorch", "keras", "pandas", "numpy", "matplotlib", "seaborn",
        "nlp", "computer vision", "data preprocessing", "feature engineering",
        "model evaluation", "xgboost", "lightgbm", "hugging face",
        "statistics", "data visualization", "tableau", "power bi",
    ],
    # Cloud / DevOps
    "cloud_devops": [
        "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd",
        "jenkins", "github actions", "terraform", "ansible", "linux",
        "bash scripting", "networking", "nginx", "apache",
    ],
    # Tools & Practices
    "tools": [
        "git", "github", "gitlab", "jira", "confluence", "vs code",
        "intellij", "postman", "figma", "agile", "scrum", "tdd",
        "unit testing", "selenium", "cypress",
    ],
    # CS Fundamentals
    "cs_fundamentals": [
        "data structures", "algorithms", "object oriented programming",
        "system design", "operating systems", "computer networks",
        "dbms", "software engineering", "design patterns",
        "problem solving", "competitive programming",
    ],
    # Soft Skills
    "soft_skills": [
        "communication", "teamwork", "leadership", "presentation skills",
        "time management", "critical thinking", "adaptability",
        "project management", "requirement gathering",
    ],
    # Security
    "security": [
        "cybersecurity", "ethical hacking", "penetration testing",
        "cryptography", "firewalls", "siem", "security protocols",
        "wireshark", "kali linux", "ceh",
    ],
}

# Flat skill list for fast matching
FLAT_SKILL_LIST = sorted(
    {skill for skills in ALL_SKILLS.values() for skill in skills}
)

# ── Resume section keywords ───────────────────────────────────────────────────
SECTION_KEYWORDS = {
    "education": ["education", "academic", "university", "college", "degree",
                  "b.tech", "bca", "mca", "b.sc", "m.tech", "cgpa", "gpa"],
    "experience": ["experience", "internship", "work history", "employment",
                   "worked at", "job", "role", "position"],
    "projects": ["project", "built", "developed", "created", "implemented",
                 "capstone", "portfolio"],
    "certifications": ["certification", "certified", "certificate", "course",
                       "udemy", "coursera", "nptel", "aws certified", "google"],
    "skills": ["skills", "technical skills", "technologies", "tools",
               "programming languages", "competencies"],
    "achievements": ["achievement", "award", "honor", "won", "rank", "topper",
                     "scholarship", "recognition"],
}

# ── Model feature columns (must match training schema) ───────────────────────
MODEL_FEATURES = [
    "cgpa",
    "aptitude_score",
    "num_projects",
    "num_internships",
    "num_certifications",
    "num_workshops",
    "communication_skills",
    "technical_skills_score",
    "backlogs",
]

# ── Readiness scoring weights (heuristic — distinct from ML prediction) ───────
READINESS_WEIGHTS = {
    "cgpa": 0.20,
    "aptitude_score": 0.20,
    "technical_skills_score": 0.20,
    "num_projects": 0.15,
    "num_internships": 0.10,
    "num_certifications": 0.08,
    "communication_skills": 0.07,
}

# ── CGPA normalization range ──────────────────────────────────────────────────
CGPA_MIN = 0.0
CGPA_MAX = 10.0
