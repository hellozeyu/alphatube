from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled
from deepmultilingualpunctuation import PunctuationModel


def download_transcript(video_id, model):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except NoTranscriptFound:
        # If there is no manual transcript, we will look for auto-generated transcript and translate it to English
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = list(transcript_list._generated_transcripts.values())[0]
        transcript = transcript.translate('en').fetch()
    except TranscriptsDisabled:
        # Sometimes the video transcript is being disabled
        return ""

    formatter = TextFormatter()
    txt_formatted = formatter.format_transcript(transcript)
    try:
        txt_formatted = model.restore_punctuation(txt_formatted.replace('\n', ' '))
    except:
        return ""

    return txt_formatted


def download_channel_transcript(service, channel_id, testing=False):

    response_list = []

    if testing:
        MAX_RESULTS = 10
        request = service.search().list(
            part='id,snippet',
            channelId=channel_id,
            type='video',
            maxResults=MAX_RESULTS
        )
        response = request.execute()
        response_list.append(response)
    else:
        MAX_RESULTS = 5000
        while request:

            request = service.search().list(
                part='id,snippet',
                channelId=channel_id,
                type='video',
                maxResults=MAX_RESULTS
            )
            response = request.execute()
            response_list.append(response)
            request = service.search().list_next(request, response)

    punc_model = PunctuationModel("oliverguhr/fullstop-punctuation-multilang-large")
    videos = []
    for response in response_list:
        for d in response['items']:
            video_id = d['id']['videoId']
            transcript = download_transcript(video_id, punc_model)
            if transcript == "":
                continue
            source_url = f"https://www.youtube.com/watch?v={video_id}"
            source_ts = d['snippet']['publishedAt']
            video = {"source_url": source_url,
                     "source_ts": source_ts,
                     "transcript": transcript}
            videos.append(video)
    return videos
