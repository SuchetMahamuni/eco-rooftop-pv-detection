# AI-Powered Rooftop Solar PV Detection  
EcoInnovators Ideathon 2026

## Overview
This project implements a governance-ready, auditable pipeline to remotely verify rooftop solar PV installations using satellite imagery and computer vision.  
Given geographic coordinates (latitude, longitude), the system determines whether a rooftop solar system is present, estimates panel area, and generates audit-friendly visual and JSON outputs.

The solution is designed to support the PM Surya Ghar: Muft Bijli Yojana by enabling scalable, low-cost verification of subsidy claims.

---

## Key Features
- Satellite image retrieval using **Google Static Maps (Satellite)**
- Solar panel detection using **YOLOv8**
- Official **1200 / 2400 sq.ft buffer logic** as per challenge FAQ
- PV area estimation (pixel-to-meter approximation)
- Quality Control (QC) status assignment
- Audit artifacts (overlay images)
- Dockerized for reproducible evaluation

---

## Input Format
The system expects an Excel file (`.xlsx`) with the following columns:

| Column Name | Description |
|------------|-------------|
| sample_id  | Unique identifier for each site |
| latitude   | Latitude (WGS84) |
| longitude  | Longitude (WGS84) |

---

## Output Format
For each input site, a JSON record is generated with fields including:
- has_solar (true / false)
- confidence
- pv_area_sqm_est
- buffer_radius_sqft
- qc_status (VERIFIABLE / NOT_VERIFIABLE)
- bbox_or_mask
- image_metadata

Overlay images with bounding boxes and buffer visualization are also saved.

---

## Quality Control Logic
- **VERIFIABLE**: Clear evidence of presence or absence of solar panels
- **NOT_VERIFIABLE**: Low confidence detections or insufficient visual evidence

The system avoids hallucination and defaults to conservative decisions where uncertainty exists.

---

## Running the Pipeline (Docker)

### 1️⃣ Build Docker Image
```bash
docker build -t rooftop-pv .
