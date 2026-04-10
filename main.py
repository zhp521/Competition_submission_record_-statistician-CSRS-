import csv
from dataclasses import dataclass
from datetime import datetime

TIME_FORMAT="%Y-%m-%d %H:%M:%S"

@dataclass
class Submission:
    submission_id:str
    team_id:str
    team_name:str
    problem_id:str
    problem_name:str
    status:str
    submit_time:datetime

#设计统计函数，统计每题提交数{题目ID:{题目的具体信息，名称，提交次数，通过次数等}}
def count_problem_submissions(submissions:list[Submission]) -> dict[str,dict[str,int]]:
    result={}
    for item in submissions:
        problem_id=item.problem_id

        if problem_id not in result:
            result[problem_id]=0
        
        result[problem_id]+=1
    return result


def load_submissions(file_path:str) -> list[Submission]:
    submissions=[]
    with open(file_path,'r',encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)

        for row in reader:
            submission=Submission(
                submission_id=row["submission_id"],
                team_id=row["team_id"],
                team_name=row["team_name"],
                problem_id=row["problem_id"],
                problem_name=row["problem_name"],
                status=row["status"],
                submit_time=datetime.strptime(row["submit_time"],TIME_FORMAT)
            )
            submissions.append(submission)
    return submissions

def main():
    submissions=load_submissions("sample_data/submissions.csv")

    problem_counts=count_problem_submissions(submissions)
    print(problem_counts)
    
if __name__=="__main__":
    main()