def nav_items(request):
    return {
        'nav_items': [
            ('dashboard', 'Overview', '▤'),
            ('live', 'Live Monitoring', '◉'),
            ('alerts', 'Alerts', '⚠'),
            ('threats', 'Threat Analysis', '⬢'),
            ('history', 'Detection History', '⧗'),
            ('authorized', 'Authorized Users', '✔'),
            ('unknown', 'Unknown Visitors', '?'),
            ('analytics', 'Analytics', '▦'),
            ('settings', 'Settings', '⚙'),
            ('logs', 'System Logs', '≣'),
        ]
    }