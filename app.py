import streamlit as st
import pandas as pd
import json
import os

USE_GEMINI =False
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    USE_GEMINI=True
except ImportError:
    pass



st.sidebar.title("Upload Json File")
uploaded_file=st.sidebar.file_uploader("Choose form-submissions.json",type="json")

if uploaded_file:
    raw_data=json.load(uploaded_file)
    flat_rows=[]
    for entry in raw_data:
        name=entry.get("name","")
        email=entry.get("email","")
        location=entry.get("location","")
        availability=",".join(entry.get("work_availability",[]))
        salary=entry.get("annual_salary_expectation",{}).get("full-time","")
        experiences=entry.get("work_experiences",[])
        roles=[exp.get("roleName","") for exp in experiences if "roleName" in exp]
        companies=[exp.get("company","") for exp in experiences if "company" in exp]
        top_role=roles[0] if roles else""
        top_company=companies[0] if companies else ""
        experience_count = len(experiences)
        flat_rows.append({
            "name":name,
            "email":email,
            "location":location,
            "availability":availability,
            "salary_expectation":salary,
            "experience_count":experience_count,
            "top_role":top_role,
            "top_company":top_company,
            "roles":",".join(roles)

        })
    df=pd.DataFrame(flat_rows)
    st.subheader("Candidate Data Preview")
    st.dataframe(df.head(),use_container_width=True)

    st.sidebar.header("Filter Candidates")
    min_exp=st.sidebar.slider("Minimum Experience(Years)",0,20,2)
    keyword=st.sidebar.text_input("Must-have Skill(e.g., Python, React)")

    filtered_df=df[df['experience_count']>=min_exp]
    if keyword:
        filtered_df=filtered_df[filtered_df['skills'].str.contains(keyword, case=False,na=False)]

    def score_candidate(row):
        score=0
        if keyword and keyword.lower() in row['roles'].lower():
            score+=5
        if "python" in row['roles'].lower():
            score+=3
        if "react" in row['roles'].lower():
            score+=3
        score+=row['experience_count']
        return score
    
    filtered_df["score"]=filtered_df.apply(score_candidate, axis=1)
    filtered_df=filtered_df.sort_values(by="score",ascending=False).reset_index(drop=True)
    st.subheader("Ranked Candidates")
    st.dataframe(filtered_df[['name','email','location','roles','experience_count','score']], use_container_width=True)
    st.subheader("Select Top 5 Hires")
    top_names=filtered_df['name'].tolist()
    selected_names=st.multiselect("Pick exactly 5 candidates", top_names[:10])

    if len(selected_names)==5:
        final_df=filtered_df[filtered_df['name'].isin(selected_names)]
        st.success("Final 5 Hires")
        st.dataframe(final_df,use_container_width=True)
        if USE_GEMINI and st.button("Generate LLM Summaries"):
            st.subheader("LLM-Powered Candidate Summaries")
            model=genai.GenerativeModel("gemini-pro")
            for _, row in final_df.iterrows():
                prompt=f"Summarize this candidate's resume:\n\n{row['resume_text']}"
                try:
                    response=model.generate_content(prompt)
                    st.markdown(f"**{row['name']}**\n\n{response.text}")
                except Exception as e:
                    st.error(f"Error generating summary for {row['name']}: {e}")
        else:
            st.warning("Please select exactly 5 candidates")
    else:
        st.info("Upload the 'form-submissions.json' file to get started.")
    
