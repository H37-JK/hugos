import os
import shutil
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()
NETLIFY_TOKEN = os.getenv("NETLIFY_TOKEN")
headers = {"Authorization": f"Bearer {NETLIFY_TOKEN}"}

sites = [
    {"name": "ohang-home-1"},
    {"name": "ohang-home-2"},
]

regions = [
    {"name": "대화동"},
    {"name": "마두동"},
]


def prepare_content():
    if os.path.exists("content"):
        shutil.rmtree("content")
    os.makedirs("content")

    for i, region in enumerate(regions, start=1):
        region_name = region['name']
        with open(f"content/{i}.md", "w", encoding="utf-8") as f:
            f.write(f''f'---\n'
                    f'title: "{region_name} 작업"\n'
                    f'---\n'
                    f'{{{{<'f'contact >}}}}')


def deploy_all():
    for site in sites:
        site_name = site['name']
        site_url = f"https://{site_name}.netlify.app/"

        print(f"\n--- 🚀 [{site_name}] 배포 프로세스 시작 ---")

        prepare_content()

        print(f"🔨 빌드 중: {site_url}")
        result = subprocess.run(
            ["hugo", "--cleanDestinationDir", "-b", site_url],
            capture_output=True, text=True, encoding="utf-8"
        )
        
        if result.returncode != 0:
            print(f"❌ 빌드 에러 ({site_name}):\n{result.stderr}")
            continue

        res = requests.post("https://api.netlify.com/api/v1/sites", headers=headers, json={"name": site_name})

        if res.status_code == 200:
            site_id = res.json()['id']
        else:
            res_list = requests.get("https://api.netlify.com/api/v1/sites", headers=headers)
            print(res_list)
            site_id = next(s['id'] for s in res_list.json() if s['name'] == site_name)

        print(f"📦 Netlify 배포 중...")
        try:
            subprocess.run(["netlify", "deploy", "--prod", "--dir", "public", "--site", site_id], check=True, shell=True)
            print(f"✅ {site_name} 배포 완료!")
        except subprocess.CalledProcessError:
            print(f"❌ {site_name} 배포 실패. (Netlify 사이트 이름이 정확한지 확인하세요)")


if __name__ == "__main__":
    deploy_all()
