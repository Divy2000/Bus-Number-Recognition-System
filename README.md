# Bus Number Detection System

This project is designed to detect and announce bus numbers for visually impaired users. It uses OpenCV and EasyOCR for number detection and integrates with Google Cloud for processing and real-time data retrieval.

## Project Overview

- **Bus Number Detection**: Identifies bus numbers using OpenCV and EasyOCR.
- **Google Cloud Integration**: Set up Google Cloud Compute to process images and communicate with an Arduino client.
- **Real-Time Data**: Fetches bus arrival data from the Singapore government API and announces bus arrivals.

## Prerequisites

- **Google Account**: Required for setting up Google Cloud.
- **Raspberry Pi**: For running the client-side scripts.
- **Arduino**: Integrated for capturing and sending data.
