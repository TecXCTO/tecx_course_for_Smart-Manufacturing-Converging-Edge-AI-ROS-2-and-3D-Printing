"""
High-Speed OpenCV Exposure Calibration ScriptThis script overrides automatic camera settings via Video4Linux2 (V4L2) drivers. It sets low exposure limits to prevent image blooming caused by the high brightness of laser melting zones.
"""
import cv2
import sys

def initialize_industrial_sensor_exposure(device_index=0, target_exposure_us=45):
    """Configures low-level camera hardware parameters to prevent overexposure."""
    cap = cv2.VideoCapture(device_index, cv2.CAP_V4L2)
    
    if not cap.isOpened():
        print(f"CRITICAL FAULT: Camera channel {device_index} unresolvable.")
        sys.exit(1)
        
    # Lock configuration to Manual Mode
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    
    # Force low microsecond exposure duration window
    cap.set(cv2.CAP_PROP_EXPOSURE, target_exposure_us)
    
    # Minimize internal amplification gains to cut sensor noise
    cap.set(cv2.CAP_PROP_GAIN, 0)
    
    print(f"Hardware Calibration Applied: Exposure locked manually at {target_exposure_us} microseconds.")
    return cap

def stream_monitored_meltpool(cap):
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Locate any overexposed hot-spots (pixels clipping at pure white)
            _, threshold_mask = cv2.threshold(gray_frame, 254, 255, cv2.THRESH_BINARY)
            clipped_pixel_count = cv2.countNonZero(threshold_mask)
            
            if clipped_pixel_count > 500:
                print(f"WARNING: Meltpool image overexposed. Whiteout count: {clipped_pixel_count} pixels.")
                
            cv2.imshow("Calibrated Edge Meltpool Feed", gray_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_connection = initialize_industrial_sensor_exposure(device_index=0, target_exposure_us=45)
    stream_monitored_meltpool(camera_connection)
