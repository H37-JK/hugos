import os
import shutil
import subprocess
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
NETLIFY_TOKEN = os.getenv("NETLIFY_TOKEN")
headers = {"Authorization": f"Bearer {NETLIFY_TOKEN}"}

sites = [
    {"name": "homecarees-ssulbis"},
    {"name": "recarees-semuns"},
    {"name": "fullcarees-sujuns"},
]
area_data = {
    "서울특별시": ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"],
    "경기도": ["가평군", "고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시", "양주시", "양평군", "여주시", "연천군", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시"],
    "인천광역시": ["강화군", "계양구", "미추홀구", "남동구", "동구", "부평구", "서구", "연수구", "옹진군", "중구"],
}

now = datetime.now()
today_str = now.strftime("%Y-%m-%dT%H:%M:%S+09:00") # 한국 시간대(+09:00) 포함

# "부산광역시": ["강서구", "금정구", "기장군", "남구", "동구", "동래구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
# "대구광역시": ["중구", "동구", "서구", "남구", "북구", "수성구", "달서구", "달성군"],
# "광주광역시": ["동구", "서구", "남구", "북구", "광산구"],
# "대전광역시": ["동구", "중구", "서구", "유성구", "대덕구"],
# "울산광역시": ["중구", "남구", "동구", "북구", "울주군"],
# "강원도": ["원주시", "춘천시", "강릉시", "동해시", "속초시", "삼척시", "홍천군", "태백시", "철원군", "횡성군", "평창군", "영월군", "정선군", "인제군", "고성군", "양양군", "화천군", "양구군"],
# "충청북도": ["청주시", "충주시", "제천시", "보은군", "옥천군", "영동군", "증평군", "진천군", "괴산군", "음성군", "단양군"],
# "충청남도": ["천안시", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군", "서천군", "청양군", "홍성군", "예산군", "태안군"],
# "경상북도": ["포항시", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", "경산시", "군위군", "의성군", "청송군", "영양군", "영덕군", "청도군", "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군"],
# "경상남도": ["창원시", "김해시", "진주시", "양산시", "거제시", "통영시", "사천시", "밀양시", "함안군", "거창군", "창녕군", "고성군", "하동군", "합천군", "남해군", "함양군", "산청군", "의령군"],
# "전라북도": ["전주시", "익산시", "군산시", "정읍시", "완주군", "김제시", "남원시", "고창군", "부안군", "임실군", "순창군", "진안군", "장수군", "무주군"],
# "전라남도": ["여수시", "순천시", "목포시", "광양시", "나주시", "무안군", "해남군", "고흥군", "화순군", "영암군", "영광군", "완도군", "담양군", "장성군", "보성군", "신안군", "장흥군", "강진군", "함평군", "진도군", "곡성군", "구례군"],
# "제주특별자치도": ["제주시", "서귀포시"]


# 변환 로직
with open('dong.txt.new', 'r', encoding='utf-8') as f:
    regions = [line.strip() for line in f if line.strip()]




# for sido, sigungu_list in area_data.items():
#     for sigungu in sigungu_list:
#         regions.append({
#             "name": sigungu,
#             "region": f"{sido} {sigungu}"
#         })


categories = [
    {"category": "변기막힘 작업"},
    {"category": "세면대 작업"},
    {"category": "수전 교체 작업"},
]

def clean_xml_file(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            xml_start_index = content.find('<?xml')

            if xml_start_index != -1:
                cleaned_content = content[xml_start_index:].strip()

                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    f.write(cleaned_content)
                print(f"🧹 {file_path} 공백 완벽 제거 완료!")
            else:
                print(f"⚠️ {file_path}에서 xml 선언문을 찾지 못했습니다.")

        except Exception as e:
            print(f"❌ {file_path} 처리 중 에러: {e}")


def prepare_content(num):
    if os.path.exists("content"):
        shutil.rmtree("content")
    os.makedirs("content")

    with open("content/_index.md", "w", encoding="utf-8") as f:
        region = '서울 특별시'
        category = '변기 막힘 작업'

        f.write(f''f'---\n'
                f'title: "{region}"\n'
                f'region: "{region}"\n'
                f'category: "{category}"\n'
                f'date: {today_str}\n'
                f'id: "0"\n'
                f'---\n')

    for i, region in enumerate(regions, start=1):
        category = categories[num - 1]['category']
        with open(f"content/{i}.md", "w", encoding="utf-8") as f:
            f.write(f''f'---\n'
                    f'title: "{region}"\n'
                    f'region: "{region}"\n'
                    f'category: "{category}"\n'
                    f'date: {today_str}\n'
                    f'id: "{i}"\n'
                    f'---\n')


def deploy_all():
    for i, site in enumerate(sites, start=1):
        site_name = site['name']
        print(site, site_name)
        site_url = f"https://{site_name}.netlify.app"

        print(f"\n--- 🚀 [{site_name}] 배포 프로세스 시작 ---")

        prepare_content(i)

        print(f"🔨 빌드 중: {site_url}")
        output_dir = f"public_{site_name}"
        cmd = f'hugo -b "{site_url}/" --destination {output_dir} --cleanDestinationDir'

        env = os.environ.copy()
        env["HUGO_BASEURL"] = f"{site_url}/" # 환경변수로 한 번 더 쐐기 박기

        subprocess.run(cmd, env=env, shell=True, check=True)

        # 3. 빌드된 사이트맵 청소 (새로 만든 폴더 안의 파일을 청소)
        sitemap_path = f"{output_dir}/sitemap.xml"
        clean_xml_file(sitemap_path)
        clean_xml_file(f"{output_dir}/index.xml")

        # res = requests.post("https://api.netlify.com/api/v1/sites", headers=headers, json={"name": site_name})
        #
        # if res.status_code == 200:
        #     site_id = res.json()['id']
        # else:
        #     res_list = requests.get("https://api.netlify.com/api/v1/sites", headers=headers)
        #     site_id = next(s['id'] for s in res_list.json() if s['name'] == site_name)
        #
        # print(f"📦 Netlify 배포 중...")
        # try:
        #     subprocess.run(
        #         ["netlify", "deploy", "--prod", "--dir", output_dir, "--site", site_id],
        #         shell=True, check=True
        #     )
        #     print(f"✅ {site_name} 배포 완료!")
        # except subprocess.CalledProcessError:
        #     print(f"❌ {site_name} 배포 실패. (Netlify 사이트 이름이 정확한지 확인하세요.)")


if __name__ == "__main__":
    deploy_all()
