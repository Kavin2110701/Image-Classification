from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from ultralytics import YOLO
import cv2
from PIL import Image
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load your models
model_bead = YOLO(
    "/Users/DP/Downloads/Sem6_project/Models/v18.pt"
)
model_stone = YOLO(
    "/Users/DP/Downloads/Sem6_project/Models/v13v9.pt"
)
model_tassel = YOLO(
    "/Users/DP/Downloads/Sem6_project/Models/v18.pt"
)

# Directory to store images
UPLOAD_DIRECTORY = "uploaded_images"
PREDICTED_DIRECTORY = "predicted_images"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(PREDICTED_DIRECTORY, exist_ok=True)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # Run predictions
    results_bead = model_bead.predict(source=file_location, imgsz=640, conf=0.5)
    results_stone = model_stone.predict(source=file_location, imgsz=640, conf=0.5)
    results_tassel = model_tassel.predict(source=file_location, imgsz=640, conf=0.5)

    image = cv2.imread(file_location)

    stone_color = (0, 255, 0)  # Green
    bead_color = (0, 0, 255)
    tassel_color = (255, 0, 0)

    for result in results_stone:
        boxes_stone = result.boxes
    
        if len(boxes_stone.cls[(boxes_stone.cls == 1)]) > 0:
            stone_indices = boxes_stone.cls == 1
            stone_xys = boxes_stone.xyxy[stone_indices]
            conf = boxes_stone.conf[stone_indices]
            print(conf)
            for i in range(len(stone_xys)):
                x1, y1, x2, y2 = stone_xys[i].cpu().numpy().astype(int)
                cv2.rectangle(image, (x1, y1), (x2, y2), stone_color, 2)
                cv2.putText(
                    image,
                    f"Stones {conf[i]:.2f}",
                    (int(x1), int(y1 - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    stone_color,
                    2,
                )

    for result in results_bead:
        boxes_bead = result.boxes
        if len(boxes_bead.cls[(boxes_bead.cls == 0)]) > 0:
            bead_indices = boxes_bead.cls == 0
            bead_xys = boxes_bead.xyxy[bead_indices]
            conf = boxes_bead.conf[bead_indices]
            for i in range(len(bead_xys)):
                x1, y1, x2, y2 = bead_xys[i].cpu().numpy().astype(int)
                cv2.rectangle(image, (x1, y1), (x2, y2), bead_color, 2)
                cv2.putText(
                    image,
                    f"Beads {conf[i]:.2f}",
                    (int(x1), int(y1 - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    bead_color,
                    2,
                )

    for result in results_tassel:
        boxes_tassel = result.boxes
        if len(boxes_tassel.cls[(boxes_tassel.cls == 2)]) > 0:
            tassel_indices = boxes_tassel.cls == 2
            tassel_xys = boxes_tassel.xyxy[tassel_indices]
            conf = boxes_tassel.conf[tassel_indices]
            for i in range(len(tassel_xys)):
                x1, y1, x2, y2 = tassel_xys[i].cpu().numpy().astype(int)
                cv2.rectangle(image, (x1, y1), (x2, y2), tassel_color, 2)
                cv2.putText(
                    image,
                    f"Tassels {conf[i]:.2f}",
                    (int(x1), int(y1 - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    tassel_color,
                    2,
                )

    predicted_image_path = f"{PREDICTED_DIRECTORY}/{file.filename}"
    cv2.imwrite(predicted_image_path, image)
    

    print(file_location,file.filename)
    return {
        "original_image_url": file_location,
        "predicted_image_url": file.filename,
    }


@app.get("/predict/{image_name}")
async def get_image(image_name: str):
    print(123,PREDICTED_DIRECTORY)
    return FileResponse(f"{PREDICTED_DIRECTORY}/{image_name}")

@app.get("/upload/{image_name}")
async def get_image(image_name: str):
    print(123,PREDICTED_DIRECTORY)
    return FileResponse(f"{UPLOAD_DIRECTORY}/{image_name}")


import uvicorn
uvicorn.run(app, host="127.0.0.1", port=7000)
# Import WebSocket dependencies


# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import FileResponse, StreamingResponse
# from fastapi.middleware.cors import CORSMiddleware
# import shutil
# import os
# from ultralytics import YOLO
# import cv2
# import time
# import numpy as np

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Update this with your React app's URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load your models
# model_bead = YOLO(
#     "/Users/DP/Downloads/Sem6_project/Models/v18.pt"
# )
# model_stone = YOLO(
#     "/Users/DP/Downloads/Sem6_project/Models/v13v9.pt"
# )
# model_tassel = YOLO(
#     "/Users/DP/Downloads/Sem6_project/Models/v10.pt"
# )

# # Directory to store images
# UPLOAD_DIRECTORY = "uploaded_images"
# PREDICTED_DIRECTORY = "predicted_images"

# os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
# os.makedirs(PREDICTED_DIRECTORY, exist_ok=True)


# def process_and_predict_image(file_location,output):
#     # Run predictions
#     results_bead = model_bead.predict(source=file_location, imgsz=640, conf=0.5)
#     results_stone = model_stone.predict(source=file_location, imgsz=640, conf=0.5)
#     results_tassel = model_tassel.predict(source=file_location, imgsz=640, conf=0.5)

#     image = cv2.imread(file_location)

#     for result in results_stone:
#         draw_boxes(image, result, 1, (0, 255, 0))  # Green for stones

#     for result in results_bead:
#         draw_boxes(image, result, 0, (0, 0, 255))  # Red for beads

#     for result in results_tassel:
#         draw_boxes(image, result, 2, (255, 0, 0))  # Blue for tassels

#     predicted_image_path = f"{PREDICTED_DIRECTORY}/{os.path.basename(file_location)}"
#     cv2.imwrite(predicted_image_path, image)

#     return output


# def draw_boxes(image, result, cls, color):
#     boxes = result.boxes
#     if len(boxes.cls[(boxes.cls == cls)]) > 0:
#         indices = boxes.cls == cls
#         xys = boxes.xyxy[indices]
#         conf = boxes.conf[indices]
#         for i in range(len(xys)):
#             x1, y1, x2, y2 = xys[i].cpu().numpy().astype(int)
#             cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
#             cv2.putText(
#                 image,
#                 f"Class {cls} {conf[i]:.2f}",
#                 (int(x1), int(y1 - 5)),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.5,
#                 color,
#                 2,
#             )


# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
#     with open(file_location, "wb+") as file_object:
#         shutil.copyfileobj(file.file, file_object)
#     predicted_image_path = process_and_predict_image(file_location,file.filename)
#     return {
#         "original_image_url": file_location,
#         "predicted_image_url": predicted_image_path,
#     }


# @app.get("/predict/{image_name}")
# async def get_image(image_name: str):
#     return FileResponse(f"{PREDICTED_DIRECTORY}/{image_name}")
# @app.get("/upload/{image_name}")
# async def get_image(image_name: str):
#     return FileResponse(f"{UPLOAD_DIRECTORY}/{image_name}")

# streaming_flag = True


# def predict_and_draw(frame):
#     # Run predictions
#     results_bead = model_bead.predict(source=frame, imgsz=640, conf=0.5)
#     results_stone = model_stone.predict(source=frame, imgsz=640, conf=0.5)
#     results_tassel = model_tassel.predict(source=frame, imgsz=640, conf=0.5)

#     image = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)

#     for result in results_stone:
#         draw_boxes(image, result, 1, (0, 255, 0))  # Green for stones

#     for result in results_bead:
#         draw_boxes(image, result, 0, (0, 0, 255))  # Red for beads

#     for result in results_tassel:
#         draw_boxes(image, result, 2, (255, 0, 0))  # Blue for tassels

#     _, img_encoded = cv2.imencode('.jpg', image)
#     return img_encoded.tobytes()


# def video_stream():
#     global streaming_flag
#     cap = cv2.VideoCapture(0)
#     while cap.isOpened() and streaming_flag:
#         ret, frame = cap.read()
#         if not ret:
#             # Handle the case where frame retrieval fails
#             continue

#         processed_frame = predict_and_draw(frame)

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + processed_frame + b'\r\n')

#         time.sleep(0.1)  # Adjust delay as needed to control frame rate

#     cap.release()



# @app.get("/video_feed")
# async def video_feed():
#     return StreamingResponse(video_stream(), media_type="multipart/x-mixed-replace;boundary=frame")


# @app.get("/stop_streaming")
# async def stop_streaming():
#     global streaming_flag
#     streaming_flag = False
#     return {"message": "Video streaming stopped."}
