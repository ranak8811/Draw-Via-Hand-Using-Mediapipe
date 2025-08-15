# Hand Drawing App Using MediaPipe

## 🎨 Overview

This project is a real-time interactive drawing application that allows users to draw on a virtual canvas using hand gestures. It leverages the power of **MediaPipe** for hand tracking and **OpenCV** for image processing and rendering. This application is designed to be beginner-friendly, providing a unique and intuitive way to create digital art without a mouse or stylus.

## ✨ Features

- **Hand Tracking:** Utilizes MediaPipe to accurately detect and track hand landmarks in real-time.
- **Gesture-Based Drawing:** Draw on the canvas by moving your right hand's index and thumb fingers closer together.
- **Dynamic Brush Size:** Adjust brush thickness by changing the distance between your left hand's index finger and thumb.
- **Color Palette:** Select from a vibrant range of colors (Red, Green, Blue, Yellow, Pink, Cyan) using UI buttons.
- **Eraser Functionality:** Clear mistakes with a dedicated eraser tool.
- **Canvas Control Gestures (Left Hand):**
  - **Open Palm (5 Fingers Up):** Triggers a fun particle animation on the screen.
  - **Fist (0 Fingers Up):** Clears the entire canvas.
  - **One Finger Up:** Cycles through different background colors for the canvas.
- **Interactive UI:** Simple on-screen buttons for color selection, eraser, and exiting the application.
- **Real-time Feedback:** Displays finger counts and brush size on the screen.

## 🚀 Getting Started

Follow these steps to set up and run the Hand Drawing App on your local machine.

### Prerequisites

Before you begin, ensure you have Python installed on your system. This project was developed and tested with Python 3.8+.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ranak8811/Draw-Via-Hand-Using-Mediapipe.git
    cd Draw-Via-Hand-Using-Mediapipe
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

### How to Run the Application

1.  **Activate your virtual environment** (if you haven't already):

    ```bash
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

2.  **Run the main application script:**

    ```bash
    python drawing_app.py
    ```

3.  **Allow Camera Access:** The application will require access to your webcam. Grant permission if prompted.

## 🖐️ How to Use

Once the application is running, you will see your webcam feed with an overlay of the drawing canvas and UI elements.

### Right Hand Controls (Drawing & Clicking)

- **Drawing:** Bring your **index finger and thumb close together** on your right hand. Move your hand to draw on the canvas.
- **Stopping Drawing:** Separate your index finger and thumb.
- **UI Interaction:** To select a color or the eraser, move your right hand's **index finger** over the desired button and bring your **middle finger and index finger close together** (as if making a "click" gesture).

### Left Hand Controls (Brush Size & Gestures)

- **Adjust Brush Size:** On your left hand, change the distance between your **index finger and thumb**. Moving them closer will decrease the brush size, and moving them further apart will increase it.
- **Clear Canvas:** Make a **fist** with your left hand (all fingers down).
- **Change Background:** Raise **one finger** (e.g., index finger) on your left hand.
- **Particle Animation:** Open your **palm** (all five fingers up) on your left hand.

### Exiting the Application

- Click the "EXIT" button on the UI with your right hand.
- Alternatively, press the `Esc` key on your keyboard.

## 📚 Libraries Used

This project relies on the following powerful libraries:

- **`opencv-python`**: A comprehensive library for computer vision tasks, used here for camera input, image manipulation, and displaying the output.
- **`mediapipe`**: Google's open-source framework for building multimodal applied ML pipelines, specifically used for its robust hand tracking capabilities.
- **`numpy`**: The fundamental package for scientific computing with Python, used for array operations and canvas management.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

## 📧 Contact

If you have any questions or feedback, please feel free to open an issue on this repository.
