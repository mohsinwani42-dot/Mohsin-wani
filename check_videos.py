import urllib.request
urls = [
    'https://cdn.coverr.co/videos/coverr-futuristic-technological-sphere-5203/1080p.mp4',
    'https://cdn.coverr.co/videos/coverr-futuristic-circuit-board-1565/1080p.mp4',
    'https://cdn.coverr.co/videos/coverr-glowing-robotics-core-4906/1080p.mp4',
    'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4'
]
for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(u, resp.status, resp.getheader('Content-Type'), resp.getheader('Content-Length'))
    except Exception as e:
        print(u, 'ERROR', e)
