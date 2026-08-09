"""
Laser Meltpool Camera Calibration Code Snippet

This production-grade Python script uses OpenCV to configure camera exposure parameters in real time. This calibration prevents high-intensity laser energy from overexposing the sensor pixels during an industrial metal printing run.
"""

import cv2
import sys

def initialize_industrial_sensor_exposure(device_index=0, target_exposure_us=45):
    """
    Configures low-level camera hardware parameters to prevent overexposure
    during high-intensity laser melting runs.
    """
    # Initialize connection to the system camera node
    cap = cv2.VideoCapture(device_index, cv2.CAP_V4L2)
    
    if not cap.isOpened():
        print(f"CRITICAL FAULT: Camera channel {device_index} unresolvable.")
        sys.exit(1)
        
    # 1. Disable automated automatic brightness adjustment routines
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # Value '1' locks configuration to Manual Mode
    
    # 2. Force low exposure duration window (value scale mapping depends on kernel driver)
    # Typically represented in logarithmic form or direct microsecond integers
    cap.set(cv2.CAP_PROP_EXPOSURE, target_exposure_us)
    
    # 3. Lock gain settings to nominal minimum limits to reduce thermal imaging whiteout noise
    cap.set(cv2.CAP_PROP_GAIN, 0)
    
    print(f"Hardware Calibration Applied: Exposure locked manually at {target_exposure_us} microseconds.")
    return cap

def stream_monitored_meltpool(cap):
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Telemetry error: Frame missing from camera link.")
                break
                
            # Convert incoming stream to single-channel grayscale data matrices
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Locate any overexposed hot-spots (pixels clipping at pure white)
            _, threshold_mask = cv2.threshold(gray_frame, 254, 255, cv2.THRESH_BINARY)
            clipped_pixel_count = cv2.countNonZero(threshold_mask)
            
            if clipped_pixel_count > 500:
                print(f"WARNING: Meltpool image overexposed. Whiteout count: {clipped_pixel_count} pixels.")
                
            # Display localized feedback loop windows to student technicians
            cv2.imshow("Calibrated Edge Meltpool Feed", gray_frame)
            
            # Break loop safely if user triggers 'q' console escape interrupt
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Target exposure configured to 45 microseconds to handle high-brightness laser plumes
    camera_connection = initialize_industrial_sensor_exposure(device_index=0, target_exposure_us=45)
    stream_monitored_meltpool(camera_connection)
