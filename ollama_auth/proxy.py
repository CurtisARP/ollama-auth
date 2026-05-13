import requests
from flask import request, Response


def build_upstream_headers(original_headers):
    headers = {}
    for name, value in original_headers.items():
        lower_name = name.lower()
        if lower_name in {"host", "authorization", "x-api-key"}:
            continue
        headers[name] = value
    headers["Accept"] = original_headers.get("Accept", "application/json")
    return headers


def proxy_request(upstream_url: str, timeout: float):
    path = request.full_path if request.query_string else request.path
    url = f"{upstream_url.rstrip('/')}{path}"

    headers = build_upstream_headers(request.headers)
    method = request.method
    data = request.get_data() or None
    json_data = None
    if request.is_json:
        json_data = request.get_json(silent=True)

    response = requests.request(
        method,
        url,
        headers=headers,
        params=request.args,
        json=json_data,
        data=data if json_data is None else None,
        timeout=timeout,
        stream=True,
    )

    excluded_headers = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    response_headers = [
        (name, value)
        for name, value in response.headers.items()
        if name.lower() not in excluded_headers
    ]

    return Response(response.iter_content(chunk_size=8192), status=response.status_code, headers=response_headers)
