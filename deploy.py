import os
import shutil
import subprocess
import requests
from dotenv import load_dotenv
from datetime import datetime
import random

load_dotenv()
headers = {"Authorization": f"Bearer {os.getenv('NETLIFY_TOKEN')}"}

sites = [{"name": "homecarees-ssulbis"}, {"name": "recarees-semuns"}, {"name": "fullcarees-sujuns"}]
categories = [{"category": "변기"}, {"category": "세면대"}, {"category": "수전"}, {"category": "배관"}, {"category": "싱크대"}, {"category": "뚫음"}]
dos = ['막힘', '교체', '수리', '고장']

with open('dong.txt.new', 'r', encoding='utf-8') as f:
    regions = [line.strip() for line in f if line.strip()]

all_images = [f"/images/{i}.png" for i in range(1, 7)]

def get_random_category():
    return ", ".join([random.choice([c['category'] for c in categories]) + random.choice(dos) for _ in range(3)])

def generate_random_body(region, category):
    return f"{region} {category} 전문 업체입니다. 24시 신속 출동 및 정직한 비용으로 해결해 드립니다."

def generate_random_title(region, category):
    return f"{region} {category} 업체 가장 잘하는 곳"

today_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00")

def get_content_html(title, region, cat, body, naver_map, google_map):
    img = random.choice(all_images)
    return f'''{{{{< rawhtml >}}}}
<div style="border: 2px solid #3498db; padding: 20px; border-radius: 10px; background-color: #f9f9f9; text-align: center;">
    <h1 style="color: #2c3e50;">{title}</h1>
    <div style="margin: 20px 0;"><img src="{img}" alt="서비스" style="max-width: 100%; height: auto; border-radius: 10px;"></div>
    <div style="padding: 15px; background: #e1f5fe; border-left: 5px solid #03a9f4; margin: 15px 0;">
        <p><strong>주요 서비스:</strong> {cat}</p>
        <p><strong>지역:</strong> {region}</p>
        <p>{body}</p>
    </div>
    <div style="margin-top: 20px;">
        <a href="{naver_map}" target="_blank" style="background:#03c75a; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; margin:5px; display:inline-block;">네이버 지도</a>
        <a href="{google_map}" target="_blank" style="background:#4285f4; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; margin:5px; display:inline-block;">구글 지도</a>
    </div>
</div>
{{{{< /rawhtml >}}}}
'''

def prepare_content(num, images_str):
    if os.path.exists("content"): shutil.rmtree("content")
    os.makedirs("content")
    
    # 1. 메인 페이지 생성
    region = '서울 특별시'
    cat = get_random_category()
    unique_body = generate_random_body(region, cat)
    summary = f"{region} {cat} 전문 업체입니다. 24시 신속 출동 및 정직한 비용으로 해결해 드립니다."
    img_param = str(random.sample(all_images, 6)).replace("'", '"')
    
    with open("content/_index.md", "w", encoding="utf-8") as f:
        f.write(f'''---
title: "{region} {cat} 전문 업체 홈케어"
description: "{summary}"
region: "{region}"
category: "{cat}"
date: {today_str}
unique_body: "{unique_body}"
images: {img_param}
id: "0"
layout: "index"
---
{get_content_html(f"{region} {cat} 업체 가장 잘하는 곳", region, cat, unique_body, "#", "#")}
''')
        f.write("\n### 📍 추천 서비스 지역\n")
        for i, reg in enumerate(random.sample(regions, min(20, len(regions)))):
            f.write(f"[{reg}](/{regions.index(reg)+1}/)  \n")
    
    # 2. 상세 페이지 생성
    counter = 1
    for region in regions:
        category = get_random_category()
        summary = f"{region} {category} 전문 업체입니다. 24시 신속 출동 및 정직한 비용으로 해결해 드립니다."
        unique_title = generate_random_title(region, category)
        unique_body = generate_random_body(region, category)
        selected_imgs = random.sample(all_images, 6)
        img_param = str(selected_imgs).replace("'", '"')
        
        with open(f"content/{counter}.md", "w", encoding="utf-8") as f:
            f.write(f'''---
title: "{unique_title}"
description: "{summary}"
region: "{region}"
category: "{category}"
date: {today_str}
images: {img_param}
id: "{counter}"
unique_body: "{unique_body}"
---
{get_content_html(unique_title, region, category, unique_body, f"https://map.naver.com/v5/search/{region}", f"https://www.google.com/maps/search/{region}")}
''')
        counter += 1

def deploy_all():
    for i, site in enumerate(sites, start=1):
        site_name = site['name']
        print(f"\n--- 🚀 [{site_name}] 배포 프로세스 시작 ---")
        output_dir = f"public_{site_name}"
        prepare_content(i, "")
        subprocess.run(f'hugo -b "https://{site_name}.netlify.app/" --destination {output_dir} --cleanDestinationDir', shell=True, check=True)
        
        # sitemap 정리
        if os.path.exists(f"{output_dir}/sitemap.xml"):
            with open(f"{output_dir}/sitemap.xml", 'r', encoding='utf-8') as f: content = f.read()
            idx = content.find('<?xml')
            if idx != -1:
                with open(f"{output_dir}/sitemap.xml", 'w', encoding='utf-8') as f: f.write(content[idx:].strip())

        # Netlify 배포 로직 (복구 완료)
        try:
            res = requests.post("https://api.netlify.com/api/v1/sites", headers=headers, json={"name": site_name})
            site_id = res.json().get('id') if res.status_code == 200 else next(s['id'] for s in requests.get("https://api.netlify.com/api/v1/sites", headers=headers).json() if s['name'] == site_name)
            subprocess.run(["netlify", "deploy", "--prod", "--dir", output_dir, "--site", site_id], shell=True, check=True)
            print(f"✅ {site_name} 배포 완료!")
        except Exception as e:
            print(f"❌ 배포 실패: {e}")

if __name__ == "__main__":
    deploy_all()
