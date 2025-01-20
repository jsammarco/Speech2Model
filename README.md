# Speech2Model

![Speech2Model](https://github.com/jsammarco/Speech2Model/blob/13e88f3e0675b5322017eece348ce243f1dfab02/Speech2Model.jpg)

Welcome to the **Speech2Model** project! This program converts spoken descriptions into detailed 3D models using the Meshy.ai API and a custom speech-to-text pipeline.

## Overview
The application enables you to:
1. Transcribe your speech using a microphone.
2. Generate detailed 3D modeling prompts with the help of a language model.
3. Create and download 3D models directly from Meshy.ai.
4. View the generated models immediately.

## Features
- **Live Transcription**: Use your microphone to describe the 3D model.
- **Intelligent Prompt Generation**: Automatically enhance vague descriptions into detailed prompts for 3D modeling.
- **Real-time Feedback**: Generate and download your 3D models in real time.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8 or later
- Required Python libraries (install via pip):
  ```bash
  pip install speechrecognition requests
  ```

### Clone the Repository
```bash
git clone https://github.com/jsammarco/Speech2Model.git
cd Speech2Model
```

### Setup
1. Obtain your Meshy.ai API key.
2. Replace `YOUR MESHY.AI KEY` in the code with your actual API key.

## Usage

### Running the Application
Run the script to start the live transcription:
```bash
python speech2model.py
```

### How It Works
1. **Describe Your Model**: Speak into your microphone to describe the 3D model.
2. **Initiate Model Creation**: Say "Create Model" when you're done describing.
3. **Prompt Generation**: The program generates a detailed modeling prompt.
4. **Model Download**: The 3D model is created and saved as a `.glb` file.
5. **View the Model**: The model opens automatically with your system's default viewer.

### Example Workflow
- Say: "A futuristic car with sleek design and neon lights."
- Say: "Create Model."
- The program processes your input and generates the model.

## File Structure
- `speech2model.py`: Main program file.
- `.glb`: Generated 3D model files will be saved here.

## Configuration
Modify the following parameters as needed:
- **Meshy.ai API key**: Replace in the `api_key` variable.
- **Polling Interval**: Adjust `poll_interval` for checking model status.
- **Default Output File**: Change `output_file` to specify where models are saved.

## Troubleshooting
- Ensure your microphone is working and permissions are granted.
- Verify your Meshy.ai API key is valid.
- Check your internet connection for API requests.

## Contributing
Feel free to fork this repository and submit pull requests to contribute improvements.

## License
This project is licensed under the MIT License.

## Contact
For any questions or issues, please reach out via the GitHub repository: [Speech2Model](https://github.com/jsammarco/Speech2Model)
