import base64, os, logging

class ImageData:
    name: str
    b64: str

    def __init__(self, b64: str, name: str):
        self.b64 = b64
        self.name = name
        
    def filename(self) -> str:
        return self.name + ".png"

def load_images() -> list[ImageData]:
    image_data: list[ImageData] = []
    try:
        for file in os.listdir(os.getenv("SAMPLES_PATH", "")):
            if not file.endswith(".png"):
                continue

            with open(os.path.join(os.getenv("SAMPLES_PATH", ""), file), "rb") as f:
                img = base64.b64encode(f.read()).decode('utf-8')
                image_name = file.split(".")[0]
                image_data.append(ImageData(b64=img,name=image_name))
    except Exception as e:
        logging.error(e)
    return image_data
