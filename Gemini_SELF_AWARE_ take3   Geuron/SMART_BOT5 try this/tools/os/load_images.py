tool_type_for_TOOL_MANAGER="all"

load_images_short_description=""" Loads multiple images from the specified paths """

def load_images(image_paths: list) -> dict:
    """Loads multiple images from the specified paths."""
    loaded_images = []
    failed_paths = []
    try:
        import cv2
        for path in image_paths:
            image = cv2.imread(path)
            if image is not None:
                loaded_images.append({"image_data": image, "image_path": path})
            else:
                failed_paths.append(path)
        return {"status": "success", "loaded_images": loaded_images, "failed_paths": failed_paths}
    except Exception as e:
        return {"status": "failure", "message": f"Error loading images: {str(e)}"}