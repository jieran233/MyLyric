def parse_lrc(lrc: str):
    parsed_lyrics = {}
    for i, line in enumerate(lrc.splitlines(), start=0):  # Use enumerate to keep track of line numbers
        if ']' not in line:
            continue  # Skip lines without ']'
        parts = line.strip().split(']')
        for part in parts[:-1]:
            time_str = part[1:]
            if line.split(']', 1)[1].strip() == '':
                continue  # Skip lines with empty lyric content
            try:
                time_parts = time_str.split(':')
                minutes = int(time_parts[0])
                seconds = float(time_parts[1])
                total_seconds = minutes * 60 + seconds
                if total_seconds not in parsed_lyrics:
                    parsed_lyrics[total_seconds] = []
                parsed_lyrics[total_seconds].append(i)  # Append line number instead of lyric text
            except ValueError:
                # Ignore lines with incorrect time format
                pass
    return parsed_lyrics


def get_lyric_at_time(lyrics, time_point):
    filtered_times = [t for t in lyrics.keys() if
                      t <= time_point]  # Filter out times that are not before or at the given time
    if filtered_times:  # Check if there are any times left after filtering
        closest_time = max(filtered_times)  # Choose the closest time that is not ahead of the given time
        return lyrics.get(closest_time)
    else:
        return [0]  # Return None if there are no lyrics before or at the given time
