# AI Car Listing Assistant

## Core API Setup

Features implemented:
- Image upload endpoint
- Metadata handling
- PostgreSQL/Redis infrastructure
- Dockerized deployment

## Setup
1. Download SAM model checkpoint:
   ```bash
   wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
   mv sam_vit_b_01ec64.pth backend/app/models/