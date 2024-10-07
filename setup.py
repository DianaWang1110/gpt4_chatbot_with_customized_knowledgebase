from setuptools import setup

setup(
    name='audio_video_summary',
    version='1.0',
    packages=['audio_video_summary'],
    url='https://github.com/PIpeIQ/audio-video-summary',
    license='',
    author='saigopinath',
    author_email='sai@pipeiq.ai',
    description='generate summaries and key takeaways from video or audio',
    install_requires=['setuptools', 'ffmpeg', 'openai', 'langchain', 'whisper'],
    long_description=open('README.md').read(),
)