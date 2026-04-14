import csv
from dataclasses import dataclass
from datetime import datetime

TIME_FORMAT="%Y-%m-%d %H:%M:%S"
AC_STATUS="AC"

@dataclass
class Submission:
    submission_id:str
    team_id:str
    team_name:str
    problem_id:str
    problem_name:str
    status:str
    submit_time:datetime

# 加载csv表格数据
def load_submissions(csv_path: str) -> list[Submission]:
    submissions:list[Submission]=[]
    with open(csv_path,"r",encoding="utf-8-sig",newline="") as file:
        reader=csv.DictReader(file)
        required_files={
            "submission_id",
            "team_id",
            "team_name",
            "problem_id",
            "problem_name",
            "status",
            "submit_time"
        }

        if not reader.fieldnames or not required_files.issubset(set(reader.fieldnames)): # 判断调用者（required_fields）是否是参数（set(reader.fieldnames)）的子集
            raise ValueError("CSV 缺少必要字段，请检查表头是否完整")
        
        for row in reader:
            submissions.append(
                Submission(
                    submission_id=row['submission_id'].strip(),
                    team_id=row['team_id'].strip(),
                    team_name=row['team_name'].strip(),
                    problem_id=row['problem_id'].strip(),
                    problem_name=row['problem_name'].strip(),
                    status=row['status'].strip().upper(),
                    submit_time=datetime.strptime(row['submit_time'].strip(),TIME_FORMAT)
                )
            )
    return sorted(submissions, key=lambda item: item.submit_time)

# 设计统计函数，统计每题提交数目
def count_problem_submissions(submissions:list[Submission]) -> dict[str,dict[str,int]]:
    result={}
    for item in submissions:
        problem_id=item.problem_id

        if problem_id not in result:
            result[problem_id]=0
        result[problem_id]+=1
    return result

# 统计每队的提交数目
def count_team_submissions(submissions:list[Submission]) -> dict[str,int]:
    result={}

    for item in submissions:
        team_id=item.team_id

        if team_id not in result:
            result[team_id]=0
        
        result[team_id]+=1
    return result

# 统计每个题目的AC个数
def count_problem_accepted(submissions:list[Submission]) -> dict[str,int]:
    result ={}

    for item in submissions:
        problem_id=item.problem_id

        if item.status!="AC":
            continue

        if problem_id not in result:
            result[problem_id]=0

        result[problem_id]+=1
    return result

# 统计每个队伍通过的题数：
def count_team_solved_problem(submissions:list[Submission])  -> dict[str,int]:
    result={}

    for item in submissions:
        if item.team_name not in result:
            result[item.team_name]=0
        else:
            if item.status=="AC":
                result[item.team_name]+=1
    return result

# 统计首次通过时间
def count_first_ac_time(submissions:list[Submission]) -> dict[str,datetime]:
    result={}

    submissions=sorted(submissions,key=lambda item:item.submit_time) #再次处理，以防万一

    for item in submissions:
        if item.status!="AC":
            continue

        if item.problem_id not in result:
            result[item.problem_id]=item.submit_time
    return result

#汇总成总分析函数:
def analyze_submissions(submissions:list[Submission]) -> dict:
    result={}

    result['problem_counts']=count_problem_submissions(submissions)
    result['problem_accepted']=count_problem_accepted(submissions)
    result['first_ac_time']=count_first_ac_time(submissions)
    result['team_counts']=count_team_submissions(submissions)
    result['team_solved']=count_team_solved_problem(submissions)

    return result

# 打印题目统计，格式更改
def print_problem_status(result:dict) -> None:
    print("====题目统计====")

    problem_counts=result['problem_counts']
    problem_accepted=result['problem_accepted']
    first_ac_time=result['first_ac_time']

    for problem_id in problem_counts:
        submit_count=problem_counts.get(problem_id,0)
        accepted_count=problem_accepted.get(problem_id,0)
        first_time = first_ac_time.get(problem_id)

        if first_time is None:
            first_time_text="暂无通过"
        else:
            first_time_text=first_time.strftime(TIME_FORMAT)
        print(
            f"题目 {problem_id}: 提交 {submit_count} 次，"
            f"通过 {accepted_count} 次，"
            f"首次通过时间 {first_time_text}"
        )

#打印队伍统计
def print_team_stats(result:dict) -> None:
    print("==队伍统计==")

    team_counts = result["team_counts"]
    team_solved = result["team_solved"]

    for team_id in team_counts:
        submit_count=team_counts.get(team_id,0)
        solved_count = team_solved.get(team_id, 0)

        print(f"队伍 {team_id}: 提交 {submit_count} 次，通过题数 {solved_count}")


def main():
    submissions=load_submissions("sample_data/submissions.csv")
    
    result=analyze_submissions(submissions)
    
    print_problem_status(result)
    print()
    print_team_stats(result)

if __name__=="__main__":
    main()
