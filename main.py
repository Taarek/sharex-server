import secrets
from os.path import splitext

import toml
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse


# Use custom expection handler so we can send JSON,
# instead of the default text in body.
async def http_exception(request, exc):
    return JSONResponse(
        {"message": exc.detail, "status_code": exc.status_code},
        status_code=exc.status_code,
    )


exception_handlers = {HTTPException: http_exception}

# Using None here to disable the docs pages,
# so we don't reveal any 'secret' endpoints.
app = FastAPI(
    title="ShareX Server",
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
    exception_handlers=exception_handlers,
)


# Load our toml config file.
with open("config.toml", "r") as file:
    app.config = toml.load(file)

# Function to handle invalid Authorization tokens in a pretty way.
async def verify_auth(authorization: str = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=400, detail="Authorization header missing..")

    if authorization != app.config["authentication"]["token"]:
        raise HTTPException(status_code=401, detail="Invalid authorization token..")


@app.post("/upload", dependencies=[Depends(verify_auth)])
async def upload_file(request: Request):

    # This is a multipart/form-data content-type.
    # A form-data field is used so we can have sharex,
    # feed us information of the filetype and name,
    # so we don't have to figure that out on our own.
    body = await request.form()

    content_type = body["file"].content_type
    file = await body["file"].read()

    original_name = splitext(body["file"].filename)[0]
    file_extension = splitext(body["file"].filename)[1]

    if app.config["general"]["retain_name"]:
        filename = original_name
    else:
        filename = secrets.token_urlsafe(app.config["general"]["file_name_length"])

    # Check the file type to determine where the file should go.
    if "image" in content_type:
        folder = app.config["paths"]["image"]
    elif "audio" in content_type:
        folder = app.config["paths"]["audio"]
    elif "video" in content_type:
        folder = app.config["paths"]["video"]
    else:
        folder = app.config["paths"]["general"]

    with open(f"{folder}{filename}{file_extension}", "wb") as newfile:
        newfile.write(file)

    return {"filename": filename, "extension": file_extension, "folder": folder}
