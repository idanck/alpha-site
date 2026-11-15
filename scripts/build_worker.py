#!/usr/bin/env python3
"""Build the Cloudflare Worker that serves index.html, and publish it.

The page is a single self-contained file, so the Worker simply embeds it and
returns it. Nothing is read from disk at request time and there is no build
step for the page itself.

Environment:
  CLOUDFLARE_API_TOKEN  required. Needs Workers Scripts:Edit and, for the
                        custom domain, Zone:Read + Workers Routes:Edit.
  CF_ACCOUNT_ID         required. The Cloudflare account that owns the Worker.
"""
import base64
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

WORKER_NAME = "alpha-site"
HOSTNAME = "alpha.idanck.com"
ZONE_NAME = "idanck.com"
API = "https://api.cloudflare.com/client/v4"

ROOT = pathlib.Path(__file__).resolve().parent.parent


def need(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"error: {name} is not set. Source your credentials file first.")
    return value


TOKEN = need("CLOUDFLARE_API_TOKEN")
ACCOUNT = need("CF_ACCOUNT_ID")


def api(method, path, data=None, headers=None, raw=False):
    head = {"Authorization": f"Bearer {TOKEN}"}
    head.update(headers or {})
    body = data
    if data is not None and not raw:
        body = json.dumps(data).encode()
        head["Content-Type"] = "application/json"
    request = urllib.request.Request(API + path, data=body, headers=head, method=method)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return json.loads(exc.read())


def build_worker(html: bytes) -> str:
    b64 = base64.b64encode(html).decode()
    return (
        f'const B64="{b64}";\n'
        'const BYTES=Uint8Array.from(atob(B64),c=>c.charCodeAt(0));\n'
        'const HTML=new TextDecoder("utf-8").decode(BYTES);\n'
        'export default{\n'
        '  async fetch(request){\n'
        '    const url=new URL(request.url);\n'
        '    if(request.method!=="GET"&&request.method!=="HEAD")\n'
        '      return new Response("Method not allowed",{status:405,headers:{allow:"GET, HEAD"}});\n'
        '    if(url.pathname!=="/"&&url.pathname!=="/index.html")\n'
        '      return Response.redirect(url.origin+"/"+url.hash,308);\n'
        '    return new Response(HTML,{headers:{\n'
        '      "content-type":"text/html; charset=utf-8",\n'
        '      "cache-control":"public, max-age=300",\n'
        '      "x-content-type-options":"nosniff",\n'
        '      "referrer-policy":"strict-origin-when-cross-origin"\n'
        '    }});\n'
        '  }\n'
        '};\n'
    )


def main() -> int:
    html = (ROOT / "index.html").read_bytes()
    worker = build_worker(html)
    print(f"page {len(html)} bytes -> worker {len(worker)} bytes")

    boundary = "----alphasiteboundary7f3a"
    metadata = json.dumps({"main_module": "worker.js", "compatibility_date": "2025-06-01"})
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="metadata"\r\n'
        f'Content-Type: application/json\r\n\r\n{metadata}\r\n'
        f'--{boundary}\r\nContent-Disposition: form-data; name="worker.js"; '
        f'filename="worker.js"\r\nContent-Type: application/javascript+module\r\n\r\n'
        f'{worker}\r\n--{boundary}--\r\n'
    ).encode()

    result = api(
        "PUT",
        f"/accounts/{ACCOUNT}/workers/scripts/{WORKER_NAME}",
        body,
        {"Content-Type": f"multipart/form-data; boundary={boundary}"},
        raw=True,
    )
    if not result.get("success"):
        for err in result.get("errors") or []:
            print("  upload error:", err)
        return 1
    print("worker uploaded")

    zones = api("GET", f"/zones?name={ZONE_NAME}")
    if not zones.get("result"):
        print("  could not resolve the zone; the custom domain was left unchanged")
        return 0
    domain = api(
        "PUT",
        f"/accounts/{ACCOUNT}/workers/domains",
        {
            "environment": "production",
            "hostname": HOSTNAME,
            "service": WORKER_NAME,
            "zone_id": zones["result"][0]["id"],
        },
    )
    print("custom domain:", "ok" if domain.get("success") else domain.get("errors"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
