from __future__ import annotations

import csv
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
AC_STATUS = "AC"


@dataclass
class Submission:
    submission_id: str
    team_id: str
    team_name: str
    problem_id: str
    problem_name: str
    status: str
    submit_time: datetime


def load_submissions(csv_path: Path) -> list[Submission]:
    submissions: list[Submission] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required_fields = {
            "submission_id",
            "team_id",
            "team_name",
            "problem_id",
            "problem_name",
            "status",
            "submit_time",
        }
        if not reader.fieldnames or not required_fields.issubset(set(reader.fieldnames)):
            raise ValueError("CSV 缺少必要字段，请检查表头是否完整。")

        for row in reader:
            submissions.append(
                Submission(
                    submission_id=row["submission_id"].strip(),
                    team_id=row["team_id"].strip(),
                    team_name=row["team_name"].strip(),
                    problem_id=row["problem_id"].strip(),
                    problem_name=row["problem_name"].strip(),
                    status=row["status"].strip().upper(),
                    submit_time=datetime.strptime(row["submit_time"].strip(), TIME_FORMAT),
                )
            )
    return sorted(submissions, key=lambda item: item.submit_time)


def analyze_submissions(submissions: list[Submission]) -> dict[str, object]:
    problem_stats: dict[str, dict[str, object]] = {}
    team_stats: dict[str, dict[str, object]] = {}
    first_ac_records: dict[str, Submission] = {}
    team_problem_solved: dict[str, set[str]] = defaultdict(set)

    for submission in submissions:
        problem_key = submission.problem_id
        if problem_key not in problem_stats:
            problem_stats[problem_key] = {
                "problem_name": submission.problem_name,
                "submission_count": 0,
                "accepted_count": 0,
                "first_accepted_time": None,
            }
        if submission.team_id not in team_stats:
            team_stats[submission.team_id] = {
                "team_name": submission.team_name,
                "submission_count": 0,
                "accepted_count": 0,
                "solved_count": 0,
            }

        problem_stats[problem_key]["submission_count"] += 1
        team_stats[submission.team_id]["submission_count"] += 1

        if submission.status == AC_STATUS:
            problem_stats[problem_key]["accepted_count"] += 1
            team_stats[submission.team_id]["accepted_count"] += 1

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


def print_problem_stats(problem_stats: dict[str, dict[str, object]]) -> None:
    print("=== 题目统计 ===")
    for problem_id, stats in sorted(problem_stats.items()):
        first_time = stats["first_accepted_time"]
        first_time_text = first_time.strftime(TIME_FORMAT) if first_time else "暂无通过"
        print(
            f"题目 {problem_id} ({stats['problem_name']}): "
            f"提交 {stats['submission_count']} 次, "
            f"通过 {stats['accepted_count']} 次, "
            f"首次通过时间 {first_time_text}"
        )


def print_team_stats(team_stats: dict[str, dict[str, object]]) -> None:
    print("\n=== 队伍统计 ===")
    for team_id, stats in sorted(team_stats.items()):
        print(
            f"队伍 {team_id} ({stats['team_name']}): "
            f"提交 {stats['submission_count']} 次, "
            f"通过记录 {stats['accepted_count']} 次, "
            f"通过题数 {stats['solved_count']}"
        )


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


def main() -> None:
    if len(sys.argv) != 2:
        print("用法: python main.py <csv文件路径>")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"文件不存在: {csv_path}")
        sys.exit(1)

    submissions = load_submissions(csv_path)
    result = analyze_submissions(submissions)
    print_problem_stats(result["problem_stats"])
    print_team_stats(result["team_stats"])
    print_first_ac_records(result["first_ac_records"])


if __name__ == "__main__":
    main()
