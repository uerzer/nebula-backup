import httpx
import json
import asyncio
from datetime import datetime, timezone

headers = {
    'User-Agent': 'OpportunityScanner/1.0 (research bot)'
}

async def fetch_reddit_rising():
    async with httpx.AsyncClient(timeout=15, headers=headers, follow_redirects=True) as client:
        try:
            resp = await client.get('https://www.reddit.com/r/popular/rising.json?limit=25')
            if resp.status_code == 200:
                data = resp.json()
                posts = []
                for child in data.get('data', {}).get('children', []):
                    d = child.get('data', {})
                    posts.append({
                        'title': d.get('title'),
                        'subreddit': d.get('subreddit'),
                        'score': d.get('score'),
                        'num_comments': d.get('num_comments'),
                        'upvote_ratio': d.get('upvote_ratio'),
                        'url': d.get('url'),
                        'created_utc': d.get('created_utc'),
                        'permalink': 'https://reddit.com' + d.get('permalink', '')
                    })
                return {'source': 'reddit_rising', 'status': 'success', 'posts': posts}
            return {'source': 'reddit_rising', 'status': 'error_' + str(resp.status_code), 'posts': []}
        except Exception as e:
            return {'source': 'reddit_rising', 'status': 'error: ' + str(e), 'posts': []}

async def fetch_reddit_top():
    async with httpx.AsyncClient(timeout=15, headers=headers, follow_redirects=True) as client:
        try:
            resp = await client.get('https://www.reddit.com/r/all/top.json?t=day&limit=25')
            if resp.status_code == 200:
                data = resp.json()
                posts = []
                for child in data.get('data', {}).get('children', []):
                    d = child.get('data', {})
                    posts.append({
                        'title': d.get('title'),
                        'subreddit': d.get('subreddit'),
                        'score': d.get('score'),
                        'num_comments': d.get('num_comments'),
                        'upvote_ratio': d.get('upvote_ratio'),
                        'url': d.get('url'),
                        'created_utc': d.get('created_utc'),
                        'permalink': 'https://reddit.com' + d.get('permalink', '')
                    })
                return {'source': 'reddit_top', 'status': 'success', 'posts': posts}
            return {'source': 'reddit_top', 'status': 'error_' + str(resp.status_code), 'posts': []}
        except Exception as e:
            return {'source': 'reddit_top', 'status': 'error: ' + str(e), 'posts': []}

async def fetch_reddit_tech_trends():
    subreddits = ['technology', 'startups', 'SaaS', 'artificial', 'cryptocurrency', 'Entrepreneur', 'sideproject']
    all_posts = []
    async with httpx.AsyncClient(timeout=15, headers=headers, follow_redirects=True) as client:
        for sub in subreddits:
            try:
                resp = await client.get('https://www.reddit.com/r/' + sub + '/hot.json?limit=10')
                if resp.status_code == 200:
                    data = resp.json()
                    for child in data.get('data', {}).get('children', []):
                        d = child.get('data', {})
                        all_posts.append({
                            'title': d.get('title'),
                            'subreddit': d.get('subreddit'),
                            'score': d.get('score'),
                            'num_comments': d.get('num_comments'),
                            'upvote_ratio': d.get('upvote_ratio'),
                            'url': d.get('url'),
                            'created_utc': d.get('created_utc'),
                            'permalink': 'https://reddit.com' + d.get('permalink', '')
                        })
                await asyncio.sleep(1)
            except Exception as e:
                print('Error fetching r/' + sub + ': ' + str(e))
    return {'source': 'reddit_tech', 'status': 'success', 'posts': all_posts}

async def fetch_hackernews():
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        try:
            resp = await client.get('https://hacker-news.firebaseio.com/v0/topstories.json')
            if resp.status_code == 200:
                story_ids = resp.json()[:30]
                stories = []
                for sid in story_ids:
                    try:
                        sresp = await client.get('https://hacker-news.firebaseio.com/v0/item/' + str(sid) + '.json')
                        if sresp.status_code == 200:
                            s = sresp.json()
                            stories.append({
                                'id': s.get('id'),
                                'title': s.get('title'),
                                'score': s.get('score'),
                                'by': s.get('by'),
                                'url': s.get('url', ''),
                                'descendants': s.get('descendants', 0),
                                'time': s.get('time'),
                                'hn_url': 'https://news.ycombinator.com/item?id=' + str(sid)
                            })
                    except:
                        pass
                return {'source': 'hackernews', 'status': 'success', 'stories': stories}
            return {'source': 'hackernews', 'status': 'error_' + str(resp.status_code), 'stories': []}
        except Exception as e:
            return {'source': 'hackernews', 'status': 'error: ' + str(e), 'stories': []}

async def fetch_hn_best():
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        try:
            resp = await client.get('https://hacker-news.firebaseio.com/v0/beststories.json')
            if resp.status_code == 200:
                story_ids = resp.json()[:20]
                stories = []
                for sid in story_ids:
                    try:
                        sresp = await client.get('https://hacker-news.firebaseio.com/v0/item/' + str(sid) + '.json')
                        if sresp.status_code == 200:
                            s = sresp.json()
                            stories.append({
                                'id': s.get('id'),
                                'title': s.get('title'),
                                'score': s.get('score'),
                                'by': s.get('by'),
                                'url': s.get('url', ''),
                                'descendants': s.get('descendants', 0),
                                'time': s.get('time'),
                                'hn_url': 'https://news.ycombinator.com/item?id=' + str(sid)
                            })
                    except:
                        pass
                return {'source': 'hn_best', 'status': 'success', 'stories': stories}
            return {'source': 'hn_best', 'status': 'error_' + str(resp.status_code), 'stories': []}
        except Exception as e:
            return {'source': 'hn_best', 'status': 'error: ' + str(e), 'stories': []}

async def main():
    reddit_rising, reddit_top, hn_top, hn_best = await asyncio.gather(
        fetch_reddit_rising(),
        fetch_reddit_top(),
        fetch_hackernews(),
        fetch_hn_best()
    )
    reddit_tech = await fetch_reddit_tech_trends()
    
    return {
        'reddit_rising': reddit_rising,
        'reddit_top': reddit_top,
        'reddit_tech': reddit_tech,
        'hn_top': hn_top,
        'hn_best': hn_best
    }

results = asyncio.run(main())

for key, val in results.items():
    if 'posts' in val:
        print(key + ': ' + val['status'] + ' - ' + str(len(val['posts'])) + ' items')
    elif 'stories' in val:
        print(key + ': ' + val['status'] + ' - ' + str(len(val['stories'])) + ' items')

import os
os.makedirs('/home/user/files/data', exist_ok=True)
with open('/home/user/files/data/raw_trend_data_20260310.json', 'w') as f:
    json.dump(results, f, indent=2)
print('\nRaw data saved successfully')