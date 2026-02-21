from pytube import YouTube, streams, Stream
import validators
import os
# from moviepy.editor import VideoFileClip, AudioFileClip
# from pydub import AudioSegment

DEFAULT_DOWNLOAD_PATH = "/Users/lapyinho/YoutubeDownloader/YoutubeDownloads"
DEFAULT_TEMP_PATH = "/Users/lapyinho/YoutubeDownloader/TEMP"


def is_valid_url(url):
    return validators.url(url)

def download(yd, path=DEFAULT_DOWNLOAD_PATH) -> None:
    try:
        print("downloading...")
        custome_name = f"{yd.title}"
        while True:
            if os.path.exists(f"{path}/{custome_name}.{yd.mime_type[6:]}"):
                if custome_name.endswith(")"):
                    suffix = str(int(custome_name[-2]) + 1)
                    custome_name = custome_name[:-2] + suffix + ")"
                else:
                    custome_name += "(1)"
            else:
                break
        yd.download(output_path=path, filename=f"{custome_name}.{yd.mime_type[6:]}")
        print("")
        print(f"Download Finished: {yd.title}")
        print("")
    except Exception as e:
        print("Error:", str(e))
        

def select_stream(possible_streams):
    type_choice = input("'1' video-only, '2' audio-only, '3' video+audio: ").strip()
    print("")
    if type_choice == '1':
        # Select video stream
        video_streams = possible_streams.filter(mime_type="video/mp4", only_video=True)
        selected_stream = choose_resolution(video_streams)

    elif type_choice == '2':
        # Select audio stream
        audio_streams = possible_streams.filter(only_audio=True)
        selected_stream = choose_audio_quality(audio_streams)

    elif type_choice == '3':
        # Select video+audio stream
        video_audio_streams = possible_streams.filter(progressive=True)
        selected_stream = choose_resolution(video_audio_streams)

    else:
        print("Invalid choice.")
        return None

    return selected_stream

def choose_resolution(streams) -> Stream:
    # Implement logic to choose a resolution from the list of video streams
    # For example, you could print the available resolutions and let the user choose
    print("Available resolutions:")
    for i, stream in enumerate(streams):
        print(f"{i+1}. Resolution: {stream.resolution}  Type: {stream.mime_type}")
    print("")
    choice = input("Enter the number corresponding to your choice: ").strip()

    try:
        selected_index = int(choice) - 1
        selected_stream = streams[selected_index]
        return selected_stream
    except (ValueError, IndexError):
        print("Invalid choice. Exiting.")
        return None

def choose_audio_quality(streams) -> Stream:
    # Implement logic to choose audio quality from the list of audio streams
    # For example, you could print the available audio qualities and let the user choose
    print("Available audio qualities:")
    for i, stream in enumerate(streams):
        print(f"{i+1}. Audio quality: {stream.abr} kbps  Type: {stream.mime_type}")
    print("")
    choice = input("Enter the number corresponding to your choice: ").strip()

    try:
        selected_index = int(choice) - 1
        selected_stream = streams[selected_index]
        return selected_stream
    except (ValueError, IndexError):
        selected_stream = streams.get_audio_only()
        return selected_stream

# Example usage
# Assuming 'possible_streams' is a collection of available streams
# selected = select_stream(possible_streams)



def download_video(youtube_url):
    try:
        yt = YouTube(youtube_url)
        print("This is your seleted video")
        print("Title : ", yt.title)
        print("Author: ", yt.author)
        time = yt.length
        print(f"Length:  {time//60}:{time%60}")
        print("")
        if input("'A' for automatic download: ").strip().lower() == 'a':
            download(yt.streams.get_highest_resolution())
            return None
        
        streams = yt.streams
        while True:
            selected_stream = select_stream(streams)
            if selected_stream is not None:
                download(selected_stream)
                break
            else:
                print("")
                print("No stream is selected.")
                print("")
                user_choice = input("Select stream again ('Q' to quit): ").strip().lower()
                print("")
                if user_choice == 'q':
                    print("")
                    break
    except Exception as e:
        print("Error:", str(e))
        
        
if __name__ == "__main__":
    print("")
    print("Welcome to Youtube Downloader----")
    print("")
    while True:
        while True:
            url = input("Enter youtube URL (or 'Q' to quit): ")
            if url.strip().lower() == 'q':
                print("")
                break
            elif is_valid_url(url.strip()):
                print("")
                #download video
                download_video(url.strip())
            else:
                print("Invalid url")
                print("")
        
        #Exit
        while True:
            user_input = input("Do you want to quit? (Y/N): ").strip().lower()

            if user_input == 'n':
                print("")
                break
                # Your code for the continuation
            elif user_input == 'y':
                print("....")
                raise SystemExit  # Exit the loop
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")
                print("")

