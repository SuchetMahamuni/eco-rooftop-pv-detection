## Model Overview
Model Type: YOLOv8 (object detection)
Task: Detection of rooftop solar photovoltaic (PV) panels
Output: Bounding boxes with confidence scores
Classes: 1 (solar_panel)
Use Case: Remote verification of rooftop solar installations under PM Surya Ghar: Muft Bijli Yojana

## Intended Use
This model is intended to support government agencies, DISCOMs, and auditors in remotely verifying the presence of rooftop solar installations using satellite imagery.
It assists in subsidy validation by providing evidence-based detection but does not replace physical inspections in ambiguous or low-confidence cases.

## Training Data
Primary Dataset: Roboflow annotated rooftop solar panel dataset
Number of Images: Approximately 700 labeled satellite images
Image Resolution: Resized to 640×640 pixels
Geographic Diversity: Urban and semi-urban rooftops
Annotations: Bounding boxes around visible solar panels

## Training Setup
Approach: Transfer learning
Base Weights: YOLOv8 pretrained on the COCO dataset
Epochs: 8
Input Size: 640×640
Hardware: NVIDIA RTX 4050 GPU (6GB VRAM)
Frameworks: Ultralytics YOLOv8, PyTorch

## Performance
Validation F1 Score: Approximately 0.77
Precision: Approximately 0.87
Recall: Approximately 0.69

## Strengths:
High precision on clearly visible rooftop solar installations
Performs well on standard urban rooftop layouts
Conservative predictions suitable for governance and subsidy verification

## Limitations and Failure Modes
Dense shadows and tree cover may hide panels
Blue or dark-painted roofs and rooftop water tanks may cause false positives
Low-resolution rural imagery can reduce detection accuracy
Very small or partially occluded installations may be missed

## Assumptions
Solar panels appear as dark, rectangular, grid-like patterns
Satellite imagery is recent and sufficiently clear
Google Static Maps satellite imagery is used during inference

## Quality Control Policy
Clear detections with sufficient confidence are marked as VERIFIABLE
Ambiguous cases such as low confidence, occlusion, or poor image quality are marked as NOT_VERIFIABLE
Conservative thresholds are used to minimize false subsidy approvals

## Ethical and Governance Considerations
No personal or sensitive data is used
Only permissible satellite imagery is utilized
Known biases such as urban versus rural performance differences are documented
Manual review is recommended for non-verifiable cases

## Reproducibility
Model training and inference are reproducible using the provided codebase
Dependencies are documented in requirements.txt
Trained model weights and inference scripts are included in the repository