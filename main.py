import csv
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict

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

#加载csv表格数据
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

#设计统计函数，统计每题提交数{题目ID:{题目的具体信息，名称，提交次数，通过次数等}}
def count_problem_submissions(submissions:list[Submission]) -> dict[str,dict[str,int]]:
    result={}
    for item in submissions:
        problem_id=item.problem_id

        if problem_id not in result:
            result[problem_id]=0
        
        result[problem_id]+=1
    return result

# 统计每队的提交数目
def count_team_submissions(submissions: list[Submission]) -> dict[str, int]:
    result = {}

    for item in submissions:
        team_id = item.team_id

        if team_id not in result:
            result[team_id] = 0

        result[team_id] += 1

    return result

#统计每个题目的AC个数
def count_problem_accepted(submissions: list[Submission]) -> dict[str, int]:
    result = {}

    for item in submissions:
        if item.status != "AC":
            continue

        problem_id = item.problem_id

        if problem_id not in result:
            result[problem_id] = 0

        result[problem_id] += 1

    return result

#统计每个队伍通过的题数：
def count_team_solved_problem(submissions:list[Submission]) -> dict[str,int]:
    solved_map={}

    for item in submissions:
        if item.status!="AC":
            continue
        
        team_id=item.team_id
        problem_id=item.team_id

        if team_id not in solved_map:
            solved_map[team_id]=set()
        
        solved_map[team_id].add(problem_id)
    
    result={}
    for team_id,solved_set in solved_map.items(): #如果不用.items，那么遍历得到的知识键的值
        result[team_id]=len(solved_set)
    
    return result

#统计“首次通过时间”
def count_first_ac_time(submissions:list[Submission]) -> dict[str,datetime]:
    result ={}

    submissions=sorted(submissions,key=lambda item:item.submit_time)

    for item in submissions:
        if item.status!="AC":
            continue
        
        if item.problem_id not in result:
            result[item.problem_id]=item.submit_time
    return result

#汇总成总分析函数
# def analyze_submissions(submissions: list[Submission]) -> dict:
#     result = {}

#     result["problem_counts"] = count_problem_submissions(submissions)
#     result["problem_accepted"] = count_problem_accepted(submissions)
#     result["first_ac_time"] = count_first_ac_time(submissions)
#     result["team_counts"] = count_team_submissions(submissions)
#     result["team_solved"] = count_team_solved_problem(submissions)

#     return result

def analyze_submissions(submissions:list[Submission]) -> dict:
    problem_stats:dict[str,dict[str,object]]={} # 存每题统计
    team_stats:dict[str,dict[str,object]]={} # 存每队统计
    first_ac_records:dict[str,Submission]={} # 直接存“首个 AC 的那条提交记录”
    team_problem_solved:dict[str,set[str]]=defaultdict(set) #用来去重，避免同一队伍同一题重复算通过题数

    for submission in submissions:
        problem_key=submission.problem_id

        if problem_key not in problem_stats:
            problem_stats[problem_key]={
                "problem_name":submission.problem_name,
                "submission_count":0,
                "accepted_count":0,
                "first_accepted_time":None
            }
        
        if submission.team_id not in team_stats:
            team_stats[submission.team_id]={
                "team_name":submission.team_name,
                "submission_count":0,
                "accepted_count":0,
                "solved_count":0
            }
        
        problem_stats[problem_key]['submission_count']+=1
        team_stats[submission.team_id]['submission_count']+=1

        if submission.status=="AC":
            problem_stats[problem_key]["accepted_count"]+=1
            team_stats[submission.team_id]['accepted_count']+=1

            if problem_stats[problem_key]["first_accepted_time"] is None:
                problem_stats[problem_key]["first_accepted_time"] = submission.submit_time
                first_ac_records[problem_key] = submission
            
            if problem_key not in team_problem_solved[submission.team_id]:
                team_problem_solved[submission.team_id].add(problem_key)
                team_stats[submission.team_id]["solved_count"] += 1
    return {
        "problem_stats": problem_stats,
        "team_stats": team_stats,
        "first_ac_records": first_ac_records,
    }

#打印题目统计（格式更改，变得更好看了）
# def print_problem_stats(result:dict) -> None:
#     print("==题目统计==")

#     problem_counts = result["problem_counts"]
#     problem_accepted = result["problem_accepted"]
#     first_ac_time = result["first_ac_time"]

#     for problem_id in problem_counts:
#         submit_count=problem_counts.get(problem_id,0)
#         accepted_count=problem_accepted.get(problem_id,0)
#         first_time = first_ac_time.get(problem_id)

#         if first_time is None:
#             first_time_text="暂无通过"
#         else:
#             first_time_text=first_time.strftime(TIME_FORMAT)
#         print(
#             f"题目 {problem_id}: 提交 {submit_count} 次，"
#             f"通过 {accepted_count} 次，"
#             f"首次通过时间 {first_time_text}"
#         )

def print_problem_stats(problem_stats: dict[str, dict[str, object]]) -> None:
    print("=== 题目统计 ===")

    for problem_id, stats in sorted(problem_stats.items()): #按照题目的序号排序
        first_time = stats["first_accepted_time"]

        if first_time is None:
            first_time_text = "暂无通过"
        else:
            first_time_text = first_time.strftime(TIME_FORMAT)

        print(
            f"题目 {problem_id} ({stats['problem_name']}): "
            f"提交 {stats['submission_count']} 次, "
            f"通过 {stats['accepted_count']} 次, "
            f"首次通过时间 {first_time_text}"
        )


#打印队伍统计
# def print_team_stats(result:dict) -> None:
#     print("==队伍统计==")

#     team_counts = result["team_counts"]
#     team_solved = result["team_solved"]

#     for team_id in team_counts:
#         submit_count=team_counts.get(team_id,0)
#         solved_count = team_solved.get(team_id, 0)

#         print(f"队伍 {team_id}: 提交 {submit_count} 次，通过题数 {solved_count}")

def print_team_stats(team_stats: dict[str, dict[str, object]]) -> None:
    print("\n=== 队伍统计 ===")

    for team_id, stats in sorted(team_stats.items()):
        print(
            f"队伍 {team_id} ({stats['team_name']}): "
            f"提交 {stats['submission_count']} 次, "
            f"通过记录 {stats['accepted_count']} 次, "
            f"通过题数 {stats['solved_count']}"
        )

# 首个“AC”队伍输出
def print_first_ac_records(first_ac_records: dict[str, Submission]) -> None:
    print("\n=== 首次通过记录 ===")

    if not first_ac_records:
        print("暂无 AC 记录")
        return

    for problem_id, submission in sorted(first_ac_records.items()):
        print(
            f"题目 {problem_id} 首次通过: "
            f"{submission.team_name} 于 {submission.submit_time.strftime(TIME_FORMAT)} 提交通过"
        )

def main():
    submissions=load_submissions("sample_data/submissions.csv")
    result=analyze_submissions(submissions)
    
    # print_problem_stats(result)
    # print()
    # print_team_stats(result)

    print_problem_stats(result["problem_stats"])
    print_team_stats(result["team_stats"])
    print_first_ac_records(result["first_ac_records"])

if __name__=="__main__":
    main()
    
#思想：
#数据读取层
#业务统计层
#结果展示层