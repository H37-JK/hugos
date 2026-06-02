import os

regions = [
    {"id": "daehwa", "name": "대화동", "service": "변기막힘/누수"},
    {"id": "juyeop", "name": "주엽동", "service": "싱크대역류/수리"}
]
CONTENT_DIR = "regions_data"


def create_region_pages():
    for region in regions:
        region_path = "regions_data"
        file_name = f"{region['id']}.md"

        if not os.path.exists(region_path):
            os.makedirs(region_path)
            print(f"Directory created: {region_path}")

        region_name = region['name']
        service_name = region['service']

        lines = [
            "---",
            f'title: "{region_name} {service_name}"',
            f'region: "{region_name}"',
            f'service: "{service_name}"',
            "---",
            f"# {region_name} 현장 사례입니다.",
            f"저희는 {region_name}에서 {service_name}를 전문으로 합니다.",
            "{{< contact >}}"
        ]
        content = "\n".join(lines)

        file_path = os.path.join(region_path, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"File created: {file_path}")


if __name__ == "__main__":
    create_region_pages()
