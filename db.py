# db.py - Database functionality
import psycopg2
from sentence_transformers import SentenceTransformer


class TalentMatchDB:
  def __init__(self, db_params):
    self.db_params = db_params
    self.model = SentenceTransformer('all-MiniLM-L6-v2')

  def connect(self):
    return psycopg2.connect(**self.db_params)

  def insert_resume(self, resume_data):
    conn = self.connect()
    cur = conn.cursor()

    try:
      cur.execute(
          "INSERT INTO candidates (candidate_id, category) VALUES (%s, %s)",
          (resume_data["id"], resume_data["category"])
      )

      for skill in resume_data["skills"]:
        cur.execute(
            "INSERT INTO skills (skill_name) VALUES (%s) ON CONFLICT (skill_name) DO NOTHING RETURNING skill_id",
            (skill,)
        )
        result = cur.fetchone()

        if result:
          skill_id = result[0]
        else:
          cur.execute(
              "SELECT skill_id FROM skills WHERE skill_name = %s", (skill,))
          skill_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO candidate_skills (candidate_id, skill_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (resume_data["id"], skill_id)
        )

      for edu in resume_data["education"]:
        parts = edu.split(',', 1)
        institution = parts[0].strip()
        degree = parts[1].strip() if len(parts) > 1 else ""
        embedding = self.model.encode(edu).tolist()

        cur.execute(
            "INSERT INTO education (candidate_id, institution, degree, description, embedding) VALUES (%s, %s, %s, %s, %s::vector)",
            (resume_data["id"], institution, degree, edu, embedding)
        )

      for exp in resume_data["experience"]:
        embedding = self.model.encode(exp).tolist()
        cur.execute(
            "INSERT INTO experience (candidate_id, title, company, description, embedding) VALUES (%s, %s, %s, %s, %s::vector)",
            (resume_data["id"], exp, "", exp, embedding)
        )

      skills_text = ", ".join(resume_data["skills"])
      skills_embedding = self.model.encode(skills_text).tolist()
      cur.execute(
          "INSERT INTO skill_embeddings (candidate_id, skills_combined_embedding) VALUES (%s, %s::vector)",
          (resume_data["id"], skills_embedding)
      )

      conn.commit()
      return True
    except Exception as e:
      conn.rollback()
      raise e
    finally:
      cur.close()
      conn.close()
