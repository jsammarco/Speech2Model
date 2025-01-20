import speech_recognition as sr
import requests
import json, time, sys, os

api_key = "YOUR MESHY.AI KEY"
headers = {
  "Authorization": f"Bearer {api_key}"
}

main_prompt = """You are a 3D model prompt assistant. Take any vague elements and get creative with further supporting details. Wait for the user to explicitly state 'Create Model' when they are done describing their model. Only after hearing this phrase, generate a detailed 3D modeling prompt based on their input.

Include the text 'STARTING 3D MODELING' at the beginning of the generated prompt to signal the process is starting. Also keep the 3d model prompt to 300 characters or less.

Let's begin, *model_description*
Create Model."""

def generate_preview_model(
    api_key,
    prompt,
    negative_prompt="low quality, low resolution, low poly, ugly",
    art_style="realistic",
    should_remesh=True,
    poll_interval=5,
    output_file="preview_model.glb"
):
    """
    Generates a 3D preview model from a text prompt and downloads the result.

    Parameters:
        api_key (str): API key for authentication.
        prompt (str): Text prompt for the 3D model.
        negative_prompt (str): Text specifying what to avoid in the model.
        art_style (str): Art style for the 3D model (default: "realistic").
        should_remesh (bool): Whether to remesh the model (default: True).
        poll_interval (int): Time (in seconds) to wait between polling status (default: 5).
        output_file (str): File name for saving the downloaded model (default: "preview_model.glb").

    Returns:
        str: Path to the downloaded model file.
    """
    headers = {"Authorization": f"Bearer {api_key}"}

    # Step 1: Generate preview task
    generate_preview_request = {
        "mode": "preview",
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "art_style": art_style,
        "should_remesh": should_remesh,
    }

    generate_preview_response = requests.post(
        "https://api.meshy.ai/openapi/v2/text-to-3d",
        headers=headers,
        json=generate_preview_request,
    )

    generate_preview_response.raise_for_status()
    preview_task_id = generate_preview_response.json()["result"]
    print("Preview task created. Task ID:", preview_task_id)

    # Step 2: Poll task status
    while True:
        preview_task_response = requests.get(
            f"https://api.meshy.ai/openapi/v2/text-to-3d/{preview_task_id}",
            headers=headers,
        )

        preview_task_response.raise_for_status()
        preview_task = preview_task_response.json()

        if preview_task["status"] == "SUCCEEDED":
            print("Preview task finished.")
            break

        print(
            "Preview task status:", preview_task["status"],
            "| Progress:", preview_task["progress"],
            "| Retrying in", poll_interval, "seconds..."
        )
        time.sleep(poll_interval)

    # Step 3: Download the model
    preview_model_url = preview_task["model_urls"]["glb"]
    preview_model_response = requests.get(preview_model_url)
    preview_model_response.raise_for_status()

    with open(output_file, "wb") as f:
        f.write(preview_model_response.content)

    print("Preview model downloaded to:", output_file)
    return output_file


def clean_after_modeling(text, phrase="STARTING 3D MODELING"):
    """
    1. Removes everything up to and including 'phrase' (if found).
    2. Trims whitespace.
    3. Removes certain leading special characters (e.g., '-' or ':').
    4. Trims whitespace again.
    5. Truncates everything from the first double line break onward.
    """
    # 1. Find the phrase, remove everything before & including it
    index = text.find(phrase)
    if index != -1:
        text = text[index + len(phrase):]

    # 2. Trim leading/trailing whitespace
    text = text.strip()

    # 3. Remove certain leading special characters
    while text and text[0] in ("-", ":"):
        text = text[1:]

    # 4. Trim again
    text = text.strip()

    # 5. Truncate at the first double line break
    dbl_break_idx = text.find("\n\n")
    if dbl_break_idx != -1:
        text = text[:dbl_break_idx]

    return text

def query_ollama(prompt, model='granite3.1-dense'):
    """
    Sends the prompt to Ollama's web API using the specified model.
    Returns the final, concatenated response text.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "prompt": prompt,
        "model": model
    }
    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error communicating with Ollama: {e}"

    # Ollama streams its responses line by line.
    output_chunks = []
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            if "response" in data:
                output_chunks.append(data["response"])
            if data.get("done"):
                break

    return "".join(output_chunks)

def live_transcription():
    recognizer = sr.Recognizer()
    text_buffer = []  # Will collect transcribed text until "Create Model" is spoken

    with sr.Microphone() as source:
        sr.pause_threshold = 0.2
        sr.energy_threshold = 3000
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=4)
        print("Ready to transcribe. Speak now!\n")
        print("Once finished describing the 3D model say, 'Create Model'")
        try:
            while True:
                print("Listening...")
                audio = recognizer.listen(source)
                try:
                    transcription = recognizer.recognize_google(audio)
                    print(f"You said: {transcription}")
                    if "start over" in transcription.lower():
                        combined_text = ""
                        print("3D model description cleared. Please begin describing.")
                    # Once we hear "Create Model", we send everything to Ollama
                    if "create model" in transcription.lower():
                        # Join all buffered text into one prompt
                        combined_text = " ".join(text_buffer)
                        if combined_text.strip():
                            # print(f"\nSending combined text to Ollama:\n{combined_text}\n")
                            temp_prompt = main_prompt.replace("*model_description*", combined_text)
                            print("Full Prompt:", temp_prompt)
                            print("")
                            response_text = query_ollama(temp_prompt)
                            # print(f"Ollama response:\n{response_text}\n")
                            prompt_for_model = clean_after_modeling(response_text)
                            print("Adjusted 3D Model Prompt:")
                            print(prompt_for_model)
                            print("Sending 3D Model Prompt MESHY.AI")
                            file_name = "speech2model_"+str(time.time())+".glb"
                            generate_preview_model(
                                api_key,
                                prompt_for_model,
                                output_file=file_name
                            )
                            print("Finished! Opening 3D Model to View")
                            os.startfile(file_name) # Open 3D Model to View
                            time.sleep(5)
                        else:
                            print("No text to send. Buffer is empty.\n")

                        # Clear the buffer for next round of recording
                        text_buffer = []
                    else:
                        # Otherwise, just keep accumulating the recognized text
                        text_buffer.append(transcription)

                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand what you said. Try again.")
                except sr.RequestError as e:
                    print(f"Error with the speech recognition service: {e}")

        except KeyboardInterrupt:
            print("\nExiting live transcription...")

if __name__ == "__main__":
    live_transcription()
