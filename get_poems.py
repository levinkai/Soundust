'''
Date: 2025-06-28 15:58:42
LastEditors: LevinKai
LastEditTime: 2025-06-28 15:58:46
FilePath: \\Work\\Soundust\\get_poems.py
'''
import requests
import re

def extract_poems_by_regex(html):
    """使用正则表达式提取诗词数据（标题与作者均支持容错，内容多行）"""
    poems = []
    
    poem_block_re = re.compile(
        r'<div id="zhengwen[^"]*">.*?'
        r'<a[^>]*?>(.*?)</a>.*?'  # 标题部分
        r'<p class="source">.*?'
        r'<a[^>]*?>(.*?)</a>.*?'      # 作者
        r'<a[^>]*?>〔(.*?)〕</a>.*?'   # 朝代
        r'<div class="contson"[^>]*?>(.*?)</div>',  # 内容
        re.DOTALL
    )

    def parse_title(raw_title):
        b_match = re.search(r'<b>(.*?)</b>', raw_title)
        if b_match:
            title = b_match.group(1).strip()
        else:
            img_match = re.search(r'<img[^>]+alt="([^"]+)"', raw_title)
            if img_match:
                title = img_match.group(1).strip()
            else:
                title = re.sub('<.*?>', '', raw_title).strip()
        return title

    def parse_author(raw_author):
        img_match = re.search(r'<img[^>]+alt="([^"]+)"', raw_author)
        if img_match:
            return img_match.group(1).strip()
        author = re.sub('<.*?>', '', raw_author)
        if '-' in author:
            author = author.split('-')[0].strip()
        author = author.strip(' \n\r-')
        return author

    def parse_content(raw_content):
        # 替换 <br> 或 <br /> 为特殊行分隔符
        html = raw_content.replace('<br />', '\n').replace('<br/>', '\n').replace('<br>', '\n')
        # 去除其它标签和多余空格
        html = re.sub(r'<.*?>', '', html)
        # 将全角空格替换为空格
        html = html.replace('　　', '')
        # 保留每一行
        lines = [line.strip() for line in html.split('\n')]
        # 丢弃空行
        return [line for line in lines if line]

    for match in poem_block_re.finditer(html):
        raw_title, raw_author, dynasty, raw_content = match.groups()
        title = parse_title(raw_title)
        author = parse_author(raw_author)
        content = parse_content(raw_content)
        
        poems.append({
            "title": title,
            "author": author,
            "dynasty": dynasty.strip(),
            "content": content
        })
    
    return poems

def get_gushiwen_poems():
    """获取古诗词网数据"""
    url = "https://www.gushiwen.cn/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return extract_poems_by_regex(response.text)
    except Exception as e:
        print(f"获取数据失败: {e}")
        return []

if __name__ == "__main__":
    poems = get_gushiwen_poems()
    if poems:
        print(f"提取到 {len(poems)} 首诗词，示例：")
        for i, poem in enumerate(poems[:3], 1):
            print(f'题目:{poem["title"]}')
            print(f'作者：{poem["author"]}')
            print(f'朝代：{poem["dynasty"]}')
            print(f'内容：{poem["content"]}')
    else:
        print("未能提取诗词数据")