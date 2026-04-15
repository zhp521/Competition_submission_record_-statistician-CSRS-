#include <algorithm>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using namespace std;
struct Submission{
    string submission_id;
    string team_id;
    string team_name;
    string problem_id;
    string problem_name;
    string status;
    string submit_time;
};

//把一整行 CSV 文本，按逗号切开，变成字符串数组
vector<string> split_csv_line(const string &line)
{
    vector<string>result;
    string current;
    stringstream ss(line);

    while(getline(ss,current,',')){
        result.push_back(current);
    }
    return result;
}

//从 CSV 文件中读取所有提交记录，并返回一个 Submission 数组
vector<Submission> load_submissions(const string &file_path)
{
    vector<Submission>submissions;
    ifstream fin(file_path);

    if(!fin.is_open())
    {
        cerr<<"无法打开文件："<<file_path<<endl;
        return submissions;
    }

    string line;
    getline(fin,line);//跳过表头

    while(getline(fin,line))
    {
        vector<string>fields=split_csv_line(line);
        if (fields.size()!=7){
            continue;
        }

        Submission submission;
        submission.submission_id = fields[0];
        submission.team_id = fields[1];
        submission.team_name = fields[2];
        submission.problem_id = fields[3];
        submission.problem_name = fields[4];
        submission.status = fields[5];
        submission.submit_time = fields[6];

        submissions.push_back(submission);
    }

    sort(submissions.begin(),submissions.end(),[](const Submission &a,const Submission &b){return a.submit_time<b.submit_time;});
    return submissions;
}

//统计每道题一共被提交了多少次
map<string,int> count_problem_submissions(const vector<Submission> &submissions)
{
    map<string,int>result;
    for(const auto &item:submissions){
        result[item.problem_id]++;
    }
    return result;
}

//统计每道题目接受了多少次
map<string,int> count_problem_accepted(const vector<Submission>&submissions)
{
    map<string,int>result;
    for(const auto &item:submissions)
    {
        if(item.status!="AC")continue;
        result[item.problem_id]++;
    }
    return result;
}

//统计每一道题目首次通过时间
map<string,string> count_first_ac_time(const vector<Submission>& submissions)
{
    map<string,string>result;
    for(const auto &item:submissions)
    {
        if(item.status!="AC")continue;
        if(result.find(item.problem_id)==result.end())
        {
            result[item.problem_id]=item.submit_time;
        }
    }
    return result;
}

//统计每个队伍的提交次数
map<string,int> count_team_submissions(vector<Submission>&submissions)
{
    map<string,int>result;
    for(const auto&item:submissions)
    {
        result[item.team_id]++;
    }
    return result;
}

//统计每个队伍作对题目的数量
map<string,int> count_team_solved_problems(vector<Submission>&submissions)
{
    map<string,set<string>>result;
    for(const auto &item:submissions)
    {
        if(item.status!="AC")continue;
        result[item.team_id].insert(item.problem_id);
    }
    map<string,int>result_final;
    for(const auto&item:result){
        result_final[item.first]=item.second.size();
    }
    return result_final;
}

//打印题目信息
void print_problem_stats(
    const map<string, int>& problem_counts,
    const map<string, int>& problem_accepted,
    const map<string, string>& first_ac_time
) {
    cout << "=== 题目统计 ===" << endl;

    for (const auto& pair : problem_counts) {
        string problem_id = pair.first;
        int submit_count = pair.second;

        int accepted_count = 0;
        if (problem_accepted.find(problem_id) != problem_accepted.end()) {
            accepted_count = problem_accepted.at(problem_id);
        }

        string first_time = "暂无通过";
        if (first_ac_time.find(problem_id) != first_ac_time.end()) {
            first_time = first_ac_time.at(problem_id);//更安全，如果键不存在，直接报错
        }

        cout << "题目 " << problem_id
             << ": 提交 " << submit_count
             << " 次, 通过 " << accepted_count
             << " 次, 首次通过时间 " << first_time << endl;
    }
}

//打印队伍信息
void print_team_stats(
    const map<string, int>& team_counts,
    const map<string, int>& team_solved
) {
    cout << endl << "=== 队伍统计 ===" << endl;

    for (const auto& pair : team_counts) {
        string team_id = pair.first;
        int submit_count = pair.second;

        int solved_count = 0;
        if (team_solved.find(team_id) != team_solved.end()) {
            solved_count = team_solved.at(team_id);
        }

        cout << "队伍 " << team_id
             << ": 提交 " << submit_count
             << " 次, 通过题数 " << solved_count << endl;
    }
}

int main()
{
    string file_path="sample_data/submissions.csv";

    vector<Submission> submissions=load_submissions(file_path);
    map<string,int>problem_counts=count_problem_submissions(submissions);
    map<string,int>problem_accepted=count_problem_accepted(submissions);
    map<string,string> first_ac_time=count_first_ac_time(submissions);
    map<string,int> team_counts=count_team_submissions(submissions);
    map<string,int>team_solved=count_team_solved_problems(submissions);

    print_problem_stats(problem_counts,problem_accepted,first_ac_time);
    print_team_stats(team_counts,team_solved);
    return 0;
}