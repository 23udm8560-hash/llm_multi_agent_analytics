def response_to_text(response) -> str:
    content = getattr(response, "content", response)
    if isinstance(content, str):
        return content
    return str(content)
