# Smart Surveillance & Threat Assessment System

A real-time surveillance system that goes beyond simple recognition — it detects people, recognizes authorized users, analyzes suspicious behavior, computes a configurable threat score, and alerts the owner with visual evidence. Built with Django, OpenCV, YOLO, and face recognition.

## Overview

Traditional monitoring systems only record. This system *understands* what it sees. It combines motion detection, deep-learning object detection, face recognition, and behavior analysis into a single pipeline, then quantifies risk as a threat score (Low / Medium / High / Critical) and notifies the owner in real time so they can act.

The architecture is layered (frontend, backend, computer vision, AI logic, database, notifications) and the video input is abstracted, so a webcam can be swapped for a file or an IP camera without changing the core system.

## Key Features

**Detection & Recognition**
- Live webcam monitoring with a streaming dashboard
- Motion detection via frame differencing, with adjustable sensitivity
- Adaptive low-light enhancement (CLAHE) that only activates in dark scenes
- Human detection using YOLO (COCO-pretrained)
- Face detection and recognition against enrolled authorized users
- Automatic unknown-visitor detection

**Intelligent Behavior Analysis**
- Loitering detection (sustained presence beyond a threshold)
- Unknown-visitor detection (tracked person with no authorized face match)
- Unattended-object detection (bags with no nearby person)
- Centroid-based multi-object tracking with stable IDs

**Threat Assessment**
- Configurable weighted threat scoring engine
- Classification into Low / Medium / High / Critical
- Admin-adjustable thresholds and weights via a Settings page

**Notification & Evidence**
- Snapshot capture of the triggering frame for each event
- Real-time browser desktop notifications on high-severity threats
- Full event logging with a visual evidence trail

**Dashboard**
- Secure authentication with session management
- Modern, responsive dark-mode UI (Tailwind CSS)
- Sections: Overview, Live Monitoring, Alerts, Threat Analysis, Detection History, Authorized Users, Unknown Visitors, Analytics, Settings, System Logs

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django |
| Computer Vision | OpenCV |
| Object Detection | YOLO (Ultralytics) |
| Face Recognition | face_recognition (dlib) |
| Frontend | HTML, Tailwind CSS, JavaScript |
| Database | SQLite (development) |
| Data | NumPy |

## Architecture

The system uses a clean layered design so components stay decoupled:

- **Frontend** — Tailwind dashboard, live video stream, notifications
- **Backend** — Django views, URL routing, authentication, ORM
- **Computer Vision** — frame capture, motion, low-light enhancement
- **AI Logic** — YOLO detection, face recognition, behavior analysis, threat scoring
- **Database** — users, enrolled faces, events, snapshots, settings
- **Notifications** — browser desktop alerts on threats

The video source is abstracted behind a single class, so the input (webcam, file, or IP camera) can change without touching the rest of the system.

## How It Works

1. Frames are captured from the webcam and optionally contrast-enhanced in low light.
2. Motion detection flags movement; YOLO identifies people and objects.
3. A centroid tracker assigns stable IDs so the system can reason about *the same* person over time.
4. Face recognition compares detected faces against enrolled authorized users; unmatched faces are flagged unknown.
5. Behavior modules evaluate loitering, unknown visitors, and unattended objects.
6. A weighted threat engine combines these signals into a score and severity level.
7. Significant events are logged with a snapshot, and high-severity events trigger a browser notification to the owner.

## Setup

**Requirements:** Python 3.12 recommended (for prebuilt dlib wheels), a working webcam.

```bash
# Clone the repository
git clone https://github.com/Nimisha8/surveillance-threat-assessment.git
cd surveillance-threat-assessment

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Set up the database
python manage.py migrate

# Create an admin account
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and log in.

## Usage

1. **Enroll authorized users** — via the Django admin (`/admin/`), add an authorized user with a clear, front-facing photo. Their face embedding is computed automatically.
2. **Start monitoring** — open Live Monitoring to view the annotated live feed.
3. **Configure detection** — adjust sensitivity, dwell times, and threat weights on the Settings page.
4. **Review events** — Alerts, Detection History, and Analytics show logged events with snapshot evidence.
5. **Get notified** — allow browser notifications to receive real-time alerts on high-severity threats.

## Notes & Limitations

- Face recognition accuracy depends on enrollment photo quality and lighting.
- Unattended-object detection uses 2D image-space proximity, not true depth, so it works best with clearly visible objects under good conditions.
- The system is designed for local, on-premise deployment (processing runs on the machine attached to the camera), which mirrors how real surveillance systems are architected.
- Masked-face recognition and additional behavior modules are architected as future extensions.

## Future Work

- Additional behavior detectors (running, restricted zones, camera tampering)
- IP camera (RTSP) support for multi-camera deployments
- Migration to a production database (MySQL/PostgreSQL) and WSGI server
- Email / SMS / messaging integrations for remote alerting

## License

This project was developed for educational purposes.
