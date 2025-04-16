# search.py - Search functionality
import psycopg2
from sentence_transformers import SentenceTransformer


class ResumeSearchEngine:
  def __init__(self, db_params):
    self.db_params = db_params
    self.model = SentenceTransformer('all-MiniLM-L6-v2')
    self.skill_graph = self._load_skill_graph()

  def _load_skill_graph(self):
    return {
        "python": ["numpy", "pandas", "scikit-learn"],
        "javascript": ["react", "node.js", "vue.js"],
        "marketing": ["advertising", "social media", "content marketing"],
        "hr": ["employee relations", "benefits", "recruiting"]
    }

  def expand_skills(self, skills):
    expanded = set(skills)

    for skill in skills:
      skill_lower = skill.lower()
      if skill_lower in self.skill_graph:
        expanded.update(self.skill_graph[skill_lower])

    lateral_equivalents = {
        "mysql": ["postgresql", "mariadb"],
        "react": ["vue", "angular"],
        "python": ["ruby", "perl"]
    }

    for skill in skills:
      skill_lower = skill.lower()
      if skill_lower in lateral_equivalents:
        expanded.update(lateral_equivalents[skill_lower])

    return list(expanded)

  def search(self, skills=None, experience=None, top_n=10):
    if skills is None:
      skills = []
    if experience is None:
      experience = []

    # Create a combined query for embedding
    combined_query = ", ".join(skills + experience)
    query_embedding = self.model.encode(
        combined_query).tolist() if combined_query else None

    print(combined_query)

    conn = psycopg2.connect(**self.db_params)
    cur = conn.cursor()

    skill_filter = ""
    experience_filter = ""
    params = []

    # Add embedding to params if we have a combined query
    if query_embedding:
      params.append(query_embedding)

    # Add skill filter if skills are provided
    if skills:
      placeholders = ','.join(['%s'] * len(skills))
      skill_filter = f"""
                AND c.candidate_id IN (
                    SELECT cs.candidate_id
                    FROM candidate_skills cs
                    JOIN skills s ON cs.skill_id = s.skill_id
                    WHERE s.skill_name IN ({placeholders})
                    GROUP BY cs.candidate_id
                    HAVING COUNT(DISTINCT cs.skill_id) >= 1
                )
                """
      params.extend(skills)

    # Add experience filter if experience terms are provided
    if experience:
      exp_placeholders = []
      for _ in experience:
        exp_placeholders.append("e.title ILIKE %s OR e.description ILIKE %s")

      experience_filter = f"""
                AND c.candidate_id IN (
                    SELECT e.candidate_id
                    FROM experience e
                    WHERE {" OR ".join(exp_placeholders)}
                )
                """
      # Add wildcard for partial matching for both title and description
      for exp in experience:
        params.extend([f"%{exp}%", f"%{exp}%"])

    similarity_clause = "1 - (se.skills_combined_embedding <=> %s::vector) AS skills_similarity" if query_embedding else "0.5 AS skills_similarity"

    query_sql = f"""
            WITH ranked_candidates AS (
                SELECT 
                    c.candidate_id,
                    c.category,
                    {similarity_clause}
                FROM 
                    candidates c
                JOIN 
                    skill_embeddings se ON c.candidate_id = se.candidate_id
                WHERE 
                    1=1
                    {skill_filter}
                    {experience_filter}
            )
            SELECT 
                rc.candidate_id,
                rc.category,
                rc.skills_similarity,
                array_agg(DISTINCT s.skill_name) AS skills,
                array_agg(DISTINCT e.description) AS education,
                array_agg(DISTINCT exp.description) AS experience
            FROM 
                ranked_candidates rc
            JOIN 
                candidate_skills cs ON rc.candidate_id = cs.candidate_id
            JOIN 
                skills s ON cs.skill_id = s.skill_id
            LEFT JOIN 
                education e ON rc.candidate_id = e.candidate_id
            LEFT JOIN 
                experience exp ON rc.candidate_id = exp.candidate_id
            GROUP BY 
                rc.candidate_id, rc.category, rc.skills_similarity
            ORDER BY 
                rc.skills_similarity DESC
            LIMIT %s
            """

    # Print the SQL and params for debugging
    print("SQL:", query_sql)
    print("Params:", params)

    params.append(top_n)

    try:
      cur.execute(query_sql, params)
      results = []
      for row in cur.fetchall():
        results.append({
            "id": row[0],
            "category": row[1],
            "similarity_score": float(row[2]),
            "skills": row[3],
            "education": row[4],
            "experience": row[5]
        })
      return results
    except Exception as e:
      print(f"Search error: {str(e)}")
      return []
    finally:
      cur.close()
      conn.close()
