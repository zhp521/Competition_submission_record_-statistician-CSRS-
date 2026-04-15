#!/bin/bash

DEFAULT_CPP_FILE="main.cpp"
SOURCE_FILE=""

if [ -n "$1" ];then
    SOURCE_FILE="$1"
else
    CPP_FILES=(*.cpp)

    if [ -e "${CPP_FILES[0]}" ];then
        count=${#CPP_FILES[@]}

        if [ "$count" -eq 1 ];then
            SOURCE_FILE="${CPP_FILES[0]}"
            echo "🔍 未指定文件，自动检测到唯一文件: $SOURCE_FILE"
        else
            cho "️当前目录有 $count 个 .cpp 文件，无法自动选择。"
            echo "文件列表: ${CPP_FILES[*]}"

            if [ -f "$DEFAULT_CPP_FILE" ];then
                echo "💡 检测到默认文件 '$DEFAULT_CPP_FILE'，将直接使用它。"
                echo "   (按回车确认，或输入其他文件名)"
                read -p "👉 确认使用 $DEFAULT_CPP_FILE? [Y/n] 或直接输入新文件名: " user_input

                if [ -z "$user_input" ] || [ "$user_input" =~ ^[Yy]$ ];then
                    SOURCE_FILE="$DEFAULT_CPP_FILE"
                else
                    SOURCE_FILE="$user_input"
                fi
            else
                echo "⚠️ 未找到默认文件 '$DEFAULT_CPP_FILE'。"
                read -p "👉 请输入你要运行的文件名 (例如 day2.cpp): " SOURCE_FILE
            fi
        fi
    else 
        echo "⚠️ 当前目录下没有找到任何 .cpp 文件。"
        read -p "👉 请输入你要运行的文件名 (例如 main.cpp): " SOURCE_FILE
    fi
fi

if [ -z "$SOURCE_FILE" ];then
    echo "❌ 错误：未指定文件名。"
    exit 1
fi

if [ ! -f "$SOURCE_FILE" ];then
    echo "❌ 错误：文件 '$SOURCE_FILE' 不存在！"
    exit 1
fi

# 4. 设置输出文件名 (去掉 .cpp 后缀)
OUTPUT_FILE="./${SOURCE_FILE%.cpp}.exe"
echo "🔨 正在编译 $SOURCE_FILE -> $OUTPUT_FILE"
# 5. 编译
g++ -finput-charset=UTF-8 -fexec-charset=GBK "$SOURCE_FILE" -o "$OUTPUT_FILE"
if [ $? -eq 0 ];then
    echo "✅ 编译成功，运行中..."
    echo "-----------------------------------"
    "$OUTPUT_FILE"
else
    echo "❌ 编译失败。"
    exit 1
fi