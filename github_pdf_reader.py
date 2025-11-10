# github_pdf_reader.py
import base64, requests, fitz
from urllib.parse import quote

def read_pdf_from_github(repo_owner, repo_name, branch, file_path, filename, github_token=None):
    # Build repo path and quote segments (preserve /)
    path = f"{file_path.strip('/')}/{filename}".strip('/')
    quoted = "/".join(quote(seg, safe="") for seg in path.split("/"))

    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{quoted}"
    raw_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{quote(branch, safe='')}/{quoted}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    # Try API (works for private repos)
    r = requests.get(api_url, headers=headers, params={"ref": branch}, timeout=15)
    if r.status_code == 200:
        data = r.json()
        pdf_bytes = base64.b64decode(data["content"])
    else:
        # Fallback to raw (public repos)
        r2 = requests.get(raw_url, headers=headers, timeout=15)
        if r2.status_code == 200:
            pdf_bytes = r2.content
        else:
            # Helpful error showing attempted URLs and statuses
            raise Exception(
                f"Not found.\nAPI URL: {api_url} -> {r.status_code}\nRaw URL: {raw_url} -> {r2.status_code}"
            )

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    meta = doc.metadata or {}
    pages = doc.page_count
    doc.close()
    return {"num_pages": pages, "metadata": meta}
