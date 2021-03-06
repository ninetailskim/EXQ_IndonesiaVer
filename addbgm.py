import moviepy.editor as mpe
from moviepy.editor import VideoFileClip
import argparse

def main(args):
    my_clip = VideoFileClip(args.video)
    audio_clip = mpe.AudioFileClip(args.bgm)
    videolen = my_clip.duration
    audiolen = audio_clip.duration
    while audiolen < videolen:
        audio_clip = mpe.concatenate_audioclips([audio_clip,audio_clip])
        audiolen = audiolen * 2

    final_clip = my_clip.set_audio(audio_clip).subclip(0, videolen)
    final_clip.write_videofile(args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str)
    parser.add_argument("--bgm", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    main(args)